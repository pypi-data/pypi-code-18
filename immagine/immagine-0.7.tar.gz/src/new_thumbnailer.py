# We do a breadth first search through the directories.

'''---

For every directory we find, we try to pick one image from it and take the
other images in the same directory as as low priority candidates for the next
picks. Then we iterate over all the subdirectories.

'''

import os
from collections import deque

from file_utils import get_files_in_dir


def sparse_iterator(items, num_steps):
    '''Sparse iteration over `items`. Every element of the list `items` is
    returned exactly once, but with a different order which can be tweaked by
    changing `num_steps`. The i-th invocation of the iterator roughly returns
    items[i*len(items)//num_steps].
    '''
    assert num_steps >= 1
    items = list(items)
    idx = 0
    while items:
        if idx >= len(items):
            idx = idx % len(items)
        yield items[idx]
        items.pop(idx)
        idx += len(items) // num_steps

def pick_files(path, num_picks=4, follow_links=False,
               smooth=2, dig_strength=5, **kwargs):
    '''Traverse the `path` and its subdirectories with the aim of picking
    `num_picks` files as sparsely as possible. `follow_links` decides whether
    symlinks should be followed or ignored in the directory traversal.
    Keyword arguments in `kwargs` are passed to `get_files_in_dir` and can
    be used to restrict the file extensions, provide a cancel check, decide
    the sort order or whether hidden files should be ignored or not.

    `dig_strength` determines how deep the search for images should be. A big
    value (e.g. 10 or 20) causes the function to search deep into the
    subdirectories, even when the parent directories contain files which are
    not images. A small value (e.g. 2 or 5) causes the function to stop when
    looking into directories that contain mostly files that are not images.
    '''

    # We try to pick one file per location, but if we don't find more files
    # in other locations we may go back to locations from which we picked
    # some files already. We use this queue to remember those.
    remaining_file_iters = deque()

    # visited_already ensures we don't end up following circular symlinks.
    visited_already = set()

    # Do a breadth first search starting from the given directory.
    paths_to_visit = deque()
    if os.path.isdir(path):
        paths_to_visit.append((0, path))

    while paths_to_visit:
        score, p = paths_to_visit.popleft()
        out = {}
        entries = get_files_in_dir(p, out=out, **kwargs)
        files = [name for is_dir, name in entries if not is_dir]
        dirs = [name for is_dir, name in entries if is_dir]

        # Update the score for this directory. Skip this directory if its
        # score is above the threshold.
        n = out['num_skipped'] + smooth
        score += (10 * out['num_skipped'] + n) // (len(files) + n)
        print('num_skipped={} len={}'.format(out['num_skipped'], len(files)))
        print('{}: {}'.format(p, score))
        if score > dig_strength:
            continue

        # Pick one file from this location and save the iterator in case we
        # later needs to pick more files.
        file_iter = sparse_iterator(files, num_picks)
        candidate = next(file_iter, None)
        if candidate is not None:
            yield candidate
        remaining_file_iters.append(file_iter)

        # Append other directories in a sparse order so that we can continue
        # to explore the hierarchy.
        for dir_name in sparse_iterator(dirs, num_picks):
            rp = os.path.realpath(dir_name)
            if rp not in visited_already:
                if rp == dir_name or follow_links:
                    paths_to_visit.append((score, dir_name))
                    visited_already.add(rp)

    # We get here when we didn't manage to pick all the files from different
    # locations. So here we go back to the previous locations to pick more
    # files.
    while remaining_file_iters:
        file_iter = remaining_file_iters.popleft()
        candidate = next(file_iter, None)
        if candidate is not None:
            yield candidate
            remaining_file_iters.append(file_iter)


if __name__ == '__main__':
    import sys
    candidates = []
    for candidate in pick_files(sys.argv[1], show_hidden_files=False):
        candidates.append(candidate)
        if len(candidates) == 4:
            break
    print(candidates)
