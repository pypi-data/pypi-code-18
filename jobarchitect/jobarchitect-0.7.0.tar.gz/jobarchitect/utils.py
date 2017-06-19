"""Utilities for jobarchitect."""

import os
import errno

from dtoolcore import DataSet


def mkdir_parents(path):
    """Create the given directory path.

    This includes all necessary parent directories. Does not raise an error if
    the directory already exists.

    :param path: path to create
    """

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


def split_iterable(iterable, nchunks):
    """Return generator yielding lists derived from the iterable.

    :param iterable: an interable
    :param nchunks: number of chunks the iterable should be split into
    :returns: generator yielding lists from the iterable
    """

    num_items = len(iterable)
    chunk_size = num_items // nchunks
    left_over_items = num_items % nchunks
    index = 0
    for n in range(nchunks, 0, -1):
        chunk = []
        for i in range(chunk_size):
            chunk.append(iterable[index])
            index += 1
        if n <= left_over_items:
            chunk.append(iterable[index])
            index += 1
        yield chunk


def output_path_from_hash(dataset_path, hash_str, output_root):
    """Return absolute output path for a dataset item.

    A.k.a. the absolute path to which output data should be written for the
    datum specified by the given hash.

    This function is not responsible for creating the directory.

    :param dataset_path: path to input dataset
    :param hash_str: dataset item identifier as a hash string
    :param output_root: path to output root
    :raises: KeyError if hash string identifier is not in the dataset
    :returns: absolute output path for a dataset item specified by the
              identifier
    """

    dataset_path = os.path.abspath(dataset_path)
    dataset = DataSet.from_path(dataset_path)

    item = dataset.item_from_identifier(hash_str)
    return os.path.join(output_root, item["path"])


def are_identifiers_in_dataset(dataset_path, identifiers):
    """Return True if all identifiers are in the suppplied dataset. If the list
    of identifiers is empty, also return True.

    :param dataset_path: path to dataset
    :param identifiers: list of identifiers to test
    :returns: True if all identifiers in dataset, False otherwise.
    """

    all_dataset_identifiers = DataSet.from_path(dataset_path).identifiers

    return set(identifiers).issubset(all_dataset_identifiers)
