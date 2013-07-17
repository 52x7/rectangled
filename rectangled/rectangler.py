import time
from cStringIO import StringIO
import logging

import github3
import git

import imagehelp

REPO_NAME = "52x7"  # TODO: add this to config
REPO_PATH = "/tmp/{}".format(REPO_NAME)


class Rectangler(object):
    def __init__(self, username, password, image_path, log=False):
        '''username: your github username
        password: your github password
        image_path: path to an image, preferrably 52:7 aspect ratio
        '''

        self.username = username
        self.password = password
        self.hub = github3.login(username, password=password)

        self.image = imagehelp.open_image(image)

        if log:
            logging.basicConfig(level=logging.debug)
        else:
            logging.basicConfig(level=logging.warning)

        # check to see if this is the first run
        # if there's no repo on github, chances are this hasn't been run yet
        repo = self.hub.repository(self.hub.user().login, REPO_NAME)

        if not repo:  # set up everything
            logging.debug("first time running")
            logging.debug("setting up repo and making initial commits")

            self.github_repo, self.repo = _setup_repo(REPO_NAME)
        else:
            self.repo = git.Repo(REPO_PATH, odbt=git.GitCmdObjectDB)
            self.github_repo = repo

        logging.debug("repo: %r" % self.repo)

    def _setup_repo(self, name):
        '''Create remote and local repositories for the picture.'''

        github_repo = self.hub.create_repo(name, has_issues=False,
                                         has_wiki=False, has_downloads=False)
        github_uri = self.repo.clone_url.split("https://")[1]  # bad, i know...
        clone_url = "https://{0}:{1}@{2}".format(self.username, self.password,
                                                 github_uri)
        repo = Repo.clone_from(clone_url, REPO_PATH,
                               odbt=git.GitCmdObjectDB)

        return github_repo, repo

    def _setup_picture(self, name):
        '''Create commits for all pixels and push them'''    

        week = 0
        while (week < 52):
            week_colors = imagehelp.colors_for_column(week, self.image)

            self.pull_changes()            
            for date, color in week_colors.iteritems():
                self.commit_changes(color, date)
            self.push_changes()

            week += 1

    def commit_changes(self, count, date):
        '''Commit a change on the repo.
        count: number of changes to commit.
        date: date the commits should be set to.
        '''

        def make_commit(repo):
            '''Creates and makes a commit.
            repo: the repo object we're committing too'''
            # i think you can make a commit without any actual change, not sure
            # ...copied from a stackoverflow

            # make all of the commit details
            message = "Rectangle commit message"
            tree = repo.index.write_tree()
            parents = [repo.head.commit]
            committer = git.Actor(name="Rectangle", email=None)
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

            logging.debug("making commit: %r" % commit)

            # and set the commit as HEAD
            repo.head.set_commit(commit, logmsg="commit: %s" % message)

        i = 0
        while (i < count):
            make_commit(self.repo)
            i += 1

        logging.debug("committed %d changes on %r" % (count, date))

    def pull_changes(self):
        logging.debug("pulling changes")
        origin = self.repo.remotes.origin
        info = origin.pull()

    def push_changes(self, count, date):
        logging.debug("pushing changes")
        origin = self.repo.remotes.origin
        info = origin.push()
