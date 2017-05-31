"""
Module to interact with public github API (https://developer.github.com/guides/getting-started/)
"""
import requests

# For disabling the InsecurePlatForm warnings (arises when using requests in python 2.x)
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


class Repository(object):
    """Class to represent a Github Repository"""

    def __init__(self, name=None, html_url=None, stargazers_count=None,
                 description=None, home_page=None):
        """
        Initializes a `Repository` object
        Parameters
        -------------------------------------------
        name : str
            Contains name of the repository
        html_url : str
            Contains link to the repository
        stargazers_count : int
            Shows number of stars to the repository
        description : str
            Contains repository description
        home_page : str
            link to the home_page of repository
        """

        self.name = name
        self.html_url = html_url
        self.stargazers_count = stargazers_count
        self.description = description
        self.home_page = home_page


class Profile(object):
    """Class to represent a Github Profile"""

    def __init__(self, username=None, name=None, location=None, email=None,
                 followers_count=None, repos_url=None, public_repos=None, public_repo_count=None):
        """
        Initializes a `Profile` object
        Parameters
        ---------------------------------
        username : str
            Contains username of the user
        name : str
            Contains name of the user
        location : str
            Contains location of the user
        email : str
            Contains email-id of the user
        followers_count : int
            Total number of followers
        repos_url : str
            Link to the repository details of user
        public_repos : [github.Repository objects]
            List containing details of all the repositories of user
        public_repo_count : int
            Total public repositories of the user
        """

        self.username = username
        self.name = name
        self.location = location
        self.email = email
        self.followers_count = followers_count
        self.repos_url = repos_url
        self.public_repos = public_repos
        self.public_repo_count = public_repo_count

    def load_gh_profile(self, username):
        """
        Loads `name`, 'location', `email`, `followers_count`, `repos_url` &
        `public_repo_count` into a github.Profile object given a `username`
        Parameters
        --------------------------------------------------------------------
        username : str
            Username of the person whose profile details to be loaded
        """

        self.username = username

        # build api url for the user
        gh_api_url = 'https://api.github.com/users/' + username
        try:
            # start requests session
            sess = requests.session()
            profile_req = sess.get(gh_api_url, timeout=50)
            profile_req.raise_for_status()
            profile = profile_req.json()
        except requests.Timeout:
            return ("Connection Timed out while loading profile for %s" % username)
        except requests.ConnectionError:
            return ("Error in Connection while loading profile for %s" % username)
        except requests.HTTPError as e:
            return ("HTTPError while sending requesting while loading profile for %s" % username)
        except ValueError:
            return "No JSON found in the request"

        # fill details
        self.name = profile['name']
        self.location = profile['location']
        self.email = profile['email']
        self.followers_count = profile['followers']
        self.repos_url = profile['repos_url']
        self.public_repo_count = profile['public_repos']
        print ("Loaded Github profile of %s" % self.username)

    def get_public_repos(self):
        """
        Fetches all the public repository details of a user & stores as an array
        of github.Repository objects in the `public_repos` attribute of a
        github.Profile object
        ------------------------------------------------------------------------
        Parameters: None
        """

        # if no profile loaded
        if self.username is None:
            return "No Github profile has been loaded yet. Please load a Github Profile first to get a list of their public repositories"

        gh_repo_url = self.repos_url
        repos_count = 0  # number of repos whose details are fetched

        # start requests session
        sess = requests.session()

        repos = []  # array to store fetched `Repository`
        page_number = 1  # to account pagination in the api

        while repos_count <= self.public_repo_count:
            if repos_count == self.public_repo_count:
                break
            try:
                url = gh_repo_url + '?page=' + str(page_number)
                repos_req = sess.get(url, timeout=50)
                repos_req.raise_for_status()

                # get details of repos on the current page
                repos_on_page = repos_req.json()
                repos += repos_on_page
            except requests.Timeout:
                return ("Connection Timed out while loading public repos of %s" % self.username)
            except requests.ConnectionError:
                return ("Error in Connection while loading  public repos of %s" % self.username)
            except requests.HTTPError as e:
                return ("HTTPError while sending requesting while loading  public repos of %s" % self.username)
            except ValueError:
                return "No JSON found in the request"

            repos_count += len(repos_on_page)
            page_number += 1

        print ("Found %s repositories.\nFetching repo details..." % repos_count)

        self.public_repos = []

        # fill fetched repo details
        for idx, _ in enumerate(repos):
            repo = Repository()
            repo.name = repos[idx]['name']
            repo.html_url = repos[idx]['html_url']
            repo.stargazers_count = repos[idx]['stargazers_count']
            repo.description = repos[idx]['description']
            repo.home_page = repos[idx]['homepage']
            self.public_repos.append(repo)
        print ("Loaded all repositories for %s" % (self.username))
