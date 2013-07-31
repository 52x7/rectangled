import time
from cStringIO import StringIO
import logging
import datetime
import os.path

import github3
import git
from gitdb import IStream

import imagehelp
import datehelp
import savestate


class Rectangler(object):
    def __init__(self, username, email, password, image_path,
                 repo_name="52x7", repo_dir="/tmp", repo_file="data",
                 log=logging.WARNING, log_file=None):
        '''username: your github username
        password: your github password
        image_path: path to an image, preferrably 52:7 aspect ratio
        log: enable debug logging?
        '''

        self.username = username
        self.email = email
        self.password = password
        self.hub = github3.login(username, password=password)

        self.image = imagehelp.open_image(image_path)

        self.state = None  # we'll get it later
        self.schedule = Scheduler()

        self.repo_name = repo_name
        self.repo_path = os.path.join(repo_dir, self.repo_name)
        self.repo_file = os.path.join(self.repo_path, repo_file)

        self.log = logging.getLogger("rectangled")
        self.log.setLevel(log)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            self.log.addHandler(file_handler)

    def start(self):
        # check to see if this is the first run
        # if there's no repo on github, chances are this hasn't been run yet
        repo = self.hub.repository(self.hub.user().login, self.repo_name)

        if not repo:  # first time, set up everything
            self.log.debug("first time running")
            self.log.debug("setting up repo and making initial commits")

            self.github_repo, self.repo = self._setup_repo(self.repo_name)
            self._setup_picture()

            # create new save state
            self.state = savestate.State(start_date=datetime.datetime.now(),
                                         week=0)
            self.state.save_to_disk()

        else:  # this ain't our first rodeo, cowboy
            self.repo = git.Repo(self.repo_path, odbt=git.GitCmdObjectDB)
            self.github_repo = repo

            self.state = State.load_from_disk()
            self._update_pictue

    def _setup_repo(self, name):
        '''Create remote and local repositories for the picture.'''

        github_repo = self.hub.create_repo(name, has_issues=False,
                                           has_wiki=False,
                                           has_downloads=False,
                                           auto_init=True,
                                           gitignore_template="C")
        github_uri = github_repo.clone_url.split("https://")[1]
        clone_url = "https://{0}:{1}@{2}".format(self.username, self.password,
                                                 github_uri)
        repo = git.Repo.clone_from(clone_url, self.repo_path,
                                   odbt=git.GitCmdObjectDB)

        with open(self.repo_file, "w") as repo_file:
            pass  # just creating the file

        return github_repo, repo

    def _setup_picture(self):
        '''Create commits for all pixels and push them'''

        week = 0
        today = datetime.datetime.now()

        self._pull_changes()
        while (week < 52):
            week_colors = imagehelp.colors_for_column(week, self.image, today)

            self.log.debug(week_colors)

            for date, color in week_colors.iteritems():
                self._commit_changes(color, date)
            week += 1

        self._push_changes()

    def _update_pictue(self):
        '''Tiles the picture every week (runs on saturdays)'''

        week = self.state.last_week
        self.log.info("Updating picture on week {}".format(week))

        start_date = self.state.start_date
        start_saturday = datehelp.find_end(start_date)
        today = datetime.datetime.now()
        # figure out what week we are in based on the start date
        current_week = (today - start_saturday).days() / 7

        self._pull_changes()

        while (week <= current_week):
            week_colors = imagehelp.colors_for_column(week, self.image,
                                                      start_date)
            for date, color in week_colors.iteritems():
                self._commit_changes(color, date)

            week += 1
            self.state.last_week = week  # done with this week, next

        self._push_changes()

        if week > 51:  # check to see if it's been a year
            self.state.start_date += datetime.timedelta(years=1)
            self.state.week = 52 - week
        self.state.save_to_disk()  # save changes

    def _commit_changes(self, count, date):
        '''Commit a change on the repo.
        count: number of changes to commit.
        date: date the commits should be set to.
        '''

        def __make_commit(repo, email):
            '''Creates and makes a commit.
            repo: the repo object we're committing too'''

            # write a change (append a number to the repo's file)
            with open(self.repo_file, "a") as data_input:
                data_input.write("%d" % count)

            repo.index.add(["data"])  # stage the file

            # ...copied from a stackoverflow
            # make all of the commit details
            message = "Rectangle commit message"
            tree = repo.index.write_tree()
            parents = [repo.head.commit]
            committer = git.Actor(name="Rectangle", email=email)
            author = committer
            commit_time = int(date.strftime("%s"))
            offset = time.altzone

            conf_encoding = "UTF-8"

            commit = git.Commit(repo, git.Commit.NULL_BIN_SHA, tree,
                                author, commit_time, offset, committer,
                                commit_time, offset, message, parents,
                                conf_encoding)

            # do some bullshit to make a hash
            stream = StringIO()
            commit._serialize(stream)
            streamlen = stream.tell()
            stream.seek(0)
            istream = repo.odb.store(IStream(git.Commit.type, streamlen,
                                     stream))
            commit.binsha = istream.binsha

            self.log.debug("making commit: %r" % commit)

            # and set the commit as HEAD
            repo.head.set_commit(commit, logmsg="commit: %s" % message)

        i = 0
        while (i < count):
            __make_commit(self.repo, self.email)
            i += 1

        self.log.debug("committed %d changes on %r" % (count, date))

    def _pull_changes(self):
        self.log.debug("pulling changes")
        origin = self.repo.remotes.origin
        info = origin.pull()

    def _push_changes(self):
        self.log.debug("pushing changes")
        origin = self.repo.remotes.origin
        info = origin.push()
