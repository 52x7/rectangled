from PIL import Image
import github3
import git

REPO_NAME = "52x7"  # TODO: add this to config

class Rectangler(object):
    def __init__(self, username, password, image):
        '''username: your github username
        password: your github password
        image: path to an image, preferrably 52:7 aspect ratio'''

        self.username = username
        self.password = password
        self.hub = github3.login(username, password=password)

        self.image = Image.open(image)
        # convert to grayscale for github (greenscale?)
        self.image = self.image.convert("L")
        # and resize to 52x7
        self.image.thumbnail((52,7), Image.ANTIALIAS)
        
        # check to see if this is the first run
        # if there's no repo on github, chances are this hasn't been run yet
        repo = self.hub.repository(self.hub.user().login, REPO_NAME)
        if not repo:  # set up everything
            self._setup_repo(REPO_NAME)

    def _setup_repo(self, name):
        self.repo = self.hub.create_repo(name, has_issues=False,
                                         has_wiki=False, has_downloads=False)
        github_uri = new_repo.clone_url.split("https://")[1]  # bad, i know...
        clone_url = "https://{0}:{1}@{2}".format(self.username, self.password,
                                                 github_uri)
        self.local_repo = Repo.clone_from(clone_url,
                                          "/tmp/{}".format(REPO_NAME))

