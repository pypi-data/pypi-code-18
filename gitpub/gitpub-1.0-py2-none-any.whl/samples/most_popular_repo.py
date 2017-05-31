from ..gitpub import gitpub


def sort_repos(repo_list):
    """
    Sort the repo_list using quicksort
    Parameters
    ----------------------------------
    repo_list : [gitpub.Repository()]
        Array of friends (loaded from the input file)
    =================================================
    Returns:
    -----------------------------------
    repo_list : [gitpub.Repository()]
    List of repositories sorted by number of stars
    """
    if repo_list == []:
        return []
    else:
        pivot = repo_list[0]
        lesser = sort_repos([repo for repo in repo_list[1:] if repo.stargazers_count < pivot.stargazers_count])
        greater = sort_repos([repo for repo in repo_list[1:] if repo.stargazers_count >= pivot.stargazers_count])
        return lesser + [pivot] + greater


def main(username='defunkt'):
    """
    Main module to put it all together
    Loading Profile > Fetch public repos > Generating sorted list of repos
    Parameters
    ----------------------------------------------------------------------
    filename : str
        Input file with friend details
    ==================================
    Returns
    ---------------------------------------------------
    sorted_repos : [gitpub.Repository()]
        Array of repositories sorted by number of stars
    """

    profile = gitpub.Profile()
    profile.load_gh_profile(username)
    profile.get_public_repos()

    sorted_repos = reversed(sort_repos(profile.public_repos))
    print ("%s(%s)'s most popular repositories by stargazers count are:" % (profile.name, profile.username))
    for repo in sorted_repos:
        print ("%s (%d stars)" % (repo.name, repo.stargazers_count))
    return sorted_repos

if __name__ == '__main__':
    sorted_repos = main()
