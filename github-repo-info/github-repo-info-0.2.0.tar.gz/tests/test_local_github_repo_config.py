import pytest
from pytest_git import GitRepo as FixtureGitRepo

from github_repo_info.github_repo_info import GitHubRepo


@pytest.fixture
def empty_repo(request):
    with FixtureGitRepo() as fixture_repo:
        yield fixture_repo


@pytest.fixture
def empty_repo_with_http_remote(request):
    with FixtureGitRepo() as fixture_repo:
        fixture_repo.api.create_remote('origin', 'https://github.com/techdragon/python-github-repo-info.git')
        yield fixture_repo


@pytest.fixture
def empty_repo_with_ssh_remote(request):
    with FixtureGitRepo() as fixture_repo:
        fixture_repo.api.create_remote('origin', 'git@github.com:techdragon/python-github-repo-info.git')
        yield fixture_repo


def test_empty_repo(empty_repo):
    git_repo = GitHubRepo(path=empty_repo.workspace)
    assert git_repo
    assert not git_repo.is_github_repository


def test_on_empty_repo_with_ssh_remote(empty_repo_with_ssh_remote):
    github_repo = GitHubRepo(path=empty_repo_with_ssh_remote.workspace)
    assert github_repo
    assert github_repo.is_github_repository
    assert github_repo.github_username == 'techdragon'
    assert github_repo.github_repo_name == 'python-github-repo-info'


def test_class_instantiation_on_empty_repo_with_http_remote(empty_repo_with_http_remote):
    github_repo = GitHubRepo(path=empty_repo_with_http_remote.workspace)
    assert github_repo
    assert github_repo.is_github_repository
    assert github_repo.github_username == 'techdragon'
    assert github_repo.github_repo_name == 'python-github-repo-info'
