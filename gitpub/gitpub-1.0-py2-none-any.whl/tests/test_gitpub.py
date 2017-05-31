import pytest
from ..gitpub import gitpub


def test_load_gh_profile():
    """
    Tests gitpub.Profile.load_gh_profile() by loading details of the user `demfier`
    ------------------------------------------------------------------------------
    Parameters: None
    """

    test_username = 'demfier'
    # define the validation Profile
    correct = gitpub.Profile(username="demfier", name="Gaurav",
                             location="Kharagpur, West Bengal",
                             email=None, followers_count=10,
                             repos_url="https://api.github.com/users/Demfier/repos",
                             public_repo_count=14)

    profile = gitpub.Profile()
    # load github profile of the user
    profile.load_gh_profile('demfier')

    # validations
    assert profile.username == correct.username
    assert profile.name == correct.name
    assert profile.email == correct.email


def test_get_public_repos():
    """
    Tests gitpub.Profile.get_public_repos() by loading public repository details
    of the user `demfier`
    ----------------------------------------------------------------------------
    Parameters: None
    """

    test_username = 'demfier'
    # define the validation Profile
    correct = gitpub.Profile(username="demfier", name="Gaurav",
                             location="Kharagpur, West Bengal",
                             email="sahu.gaurav719@gmail.com", followers_count=10,
                             repos_url="https://api.github.com/users/Demfier/repos",
                             public_repo_count=14)

    # get public repos for the validation Profile
    correct.get_public_repos()

    profile = gitpub.Profile()
    profile.load_gh_profile('demfier')
    profile.get_public_repos()

    # validations
    for idx, _ in enumerate(profile.public_repos):
        assert profile.public_repos[idx].name == correct.public_repos[idx].name
