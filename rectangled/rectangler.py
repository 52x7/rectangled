import github3
import git

import imagehelp


REPO_NAME = "52x7"  # TODO: add this to config
REPO_PATH = "/tmp/{}".format(REPO_NAME)


class Rectangler(object):
    def __init__(self, username, password, image_path):
        '''username: your github username
        password: your github password
        image_path: path to an image, preferrably 52:7 aspect ratio
        '''

        self.username = username
        self.password = password
        self.hub = github3.login(username, password=password)

        self.image = imagehelp.open_image(image)

        # check to see if this is the first run
        # if there's no repo on github, chances are this hasn't been run yet
        repo = self.hub.repository(self.hub.user().login, REPO_NAME)
        if not repo:  # set up everything
            self._setup_repo(REPO_NAME)
        else:
            self.repo = repo
            self.local_repo = Repo(REPO_PATH, odbt=git.GitCmdObjectDB)

    def _setup_repo(self, name):
        '''Create remote and local repositories for the picture.'''

        self.repo = self.hub.create_repo(name, has_issues=False,
                                         has_wiki=False, has_downloads=False)
        github_uri = new_repo.clone_url.split("https://")[1]  # bad, i know...
        clone_url = "https://{0}:{1}@{2}".format(self.username, self.password,
                                                 github_uri)
        self.local_repo = Repo.clone_from(clone_url, REPO_PATH,
                                          odbt=git.GitCmdObjectDB)

