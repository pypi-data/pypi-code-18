import pytest
from pytest_git import GitRepo as FixtureGitRepo

from git_repo_info.git_repo_info import GitRepo


@pytest.fixture
def empty_repo(request):
    with FixtureGitRepo() as fixture_repo:
        yield fixture_repo


@pytest.fixture
def empty_repo_with_http_remote(request):
    with FixtureGitRepo() as fixture_repo:
        fixture_repo.api.create_remote('origin', 'https://github.com/techdragon/python-git-repo-info.git')
        yield fixture_repo


@pytest.fixture
def empty_repo_with_ssh_remote(request):
    with FixtureGitRepo() as fixture_repo:
        fixture_repo.api.create_remote('origin', 'git@github.com:techdragon/python-git-repo-info.git')
        yield fixture_repo


def test_empty_repo(empty_repo):
    git_repo = GitRepo(path=empty_repo.workspace)
    assert git_repo
    assert not git_repo.is_dirty
    assert len(git_repo.remotes) == 0


def test_on_empty_repo_with_ssh_remote(empty_repo_with_ssh_remote):
    git_repo = GitRepo(path=empty_repo_with_ssh_remote.workspace)
    assert git_repo
    assert not git_repo.is_dirty
    assert len(git_repo.remotes) == 1


def test_class_instantiation_on_empty_repo_with_http_remote(empty_repo_with_http_remote):
    git_repo = GitRepo(path=empty_repo_with_http_remote.workspace)
    assert git_repo
    assert not git_repo.is_dirty
    assert len(git_repo.remotes) == 1
