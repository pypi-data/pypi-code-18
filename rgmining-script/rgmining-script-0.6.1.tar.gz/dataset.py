#!/usr/bin/env python
#
# dataset.py
#
# Copyright (c) 2017 Junpei Kawamoto
#
# This file is part of rgmining-script.
#
# rgmining-script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-script. If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=wrong-import-position,invalid-name,no-member,import-error
"""Analyze and handle datasets.
"""
from __future__ import absolute_import
import datetime
import logging
from os import path
import sys

from common.writer import JSONWriter, CSVWriter
import dataset_io
import dsargparse
import ria
import numpy as np

import helper


# Input type
def file_or_list(value):
    """Argument type for dsargparse.

    If argument is a file, it will be opened and passed as an iterator.
    If argument is a string, it will be treated as a comma-separated list.

    Args:
      value: Argument value.

    Yield:
      each line in the file if the given value points a file, otherwise,
      each item in the given collection.
    """
    if path.exists(value):
        with open(value) as fp:
            for line in fp:
                yield line
    else:
        for item in value.split(","):
            yield item


#------------------------------------------------
# Reviewer
#------------------------------------------------
def retrieve_reviewers(graph, output, target):
    """Output the ID of reviewers who review at least one of the given products.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
      target: a list of target product ids.
    """
    target_ids = {s.strip() for s in target}
    for reviewer in graph.reviewers:
        for product in graph.retrieve_products(reviewer):
            if product.name in target_ids:
                output.write(reviewer.name)
                output.write("\n")
                break


def active_reviewers(graph, output, threshold=2):
    """Output the ID of reviewers who review at least threshold items.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
      threshold: the threshold (default: 2).
    """
    for reviewer in graph.reviewers:
        if len(graph.retrieve_products(reviewer)) >= threshold:
            output.write(reviewer.name)
            output.write("\n")


def reviewer_size(graph, output, target, csv_format=False):
    """Output the number of reviews of each reviewer who reviews target products.

    Compute the number of reviews of each reviewer who reviews at least one
    product in the given target products.

    The default output format is JSON and the scheme as::

        {
          "reviewer": <Reviewer ID>,
          "size": <The number of reviews the reviewer posts>,
          "product": <Product ID which the reviewer reviews in the targets>
        }

    In the outputs, one line represents one JSON object.

    CSV format is also supported to output results.
    In this option, the first line shows a header.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
      target: a list of target object IDs.
      csv_format: If True, outputs will be formatted in CSV format.
    """
    if csv_format:
        writer = CSVWriter(output, ("reviewer", "size", "product"))
    else:
        writer = JSONWriter(output)

    targets = {name for name in target}
    for r in graph.reviewers:
        products = graph.retrieve_products(r)
        for p in products:
            if p.name in targets:
                writer.write({
                    "size": len(products),
                    "reviewer": r.name,
                    "product": p.name
                })


def filter_reviewers(graph, output, target, csv_format=False):
    """Output reviews posted by reviewers whose IDs match the given set of IDs.

    The output format is JSON and the scheme as::

        {
            "member_id": <Reviewer ID>,
            "product_id": <Product ID>,
            "rating": <Rating score>,
            "date": <Date the review posted>
        }

    In the outputs, one line represents one JSON object.

    CSV format is also supported to output results.
    In this option, the first line shows a header.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
      target: a list of target reviewer ids.
      csv_format: If True, outputs will be formatted in CSV format.
    """
    if csv_format:
        writer = CSVWriter(output, ("member_id", "product_id", "rating", "date"))
    else:
        writer = JSONWriter(output)

    targets = {name for name in target}
    for r in graph.reviewers:
        if r.name in targets:
            for p in graph.retrieve_products(r):
                review = graph.retrieve_review(r, p)
                date = review.date
                if date:
                    date = datetime.datetime.strptime(
                        str(review.date), "%Y%m%d").strftime("%Y-%m-%d")
                writer.write({
                    "member_id": r.name,
                    "product_id": p.name,
                    "rating": review.score,
                    "date": date
                })


#------------------------------------------------
# Product
#------------------------------------------------
def rating_average(graph, output, csv_format=False):
    """Output average rating scores of each product.

    The output format is JSON and the scheme as::

        {
            "product_id": <Product ID>,
            "summary": <Average rating score>
        }

    In the outputs, one line represents one JSON object.

    CSV format is also supported to output results.
    In this option, the first line shows a header.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
      csv_format: If True, outputs will be formatted in CSV format.
    """
    if csv_format:
        writer = CSVWriter(output, ("product_id", "summary"))
    else:
        writer = JSONWriter(output)

    for p in graph.products:
        avg = np.mean([
            graph.retrieve_review(r, p).score for r in graph.retrieve_reviewers(p)
        ])
        writer.write({
            "product_id": p.name,
            "summary": avg
        })


def distinct_product(graph, output):
    """Output distinct product IDs.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
    """
    for p in graph.products:
        output.write(p.name)
        output.write("\n")


def popular_products(graph, output, threshold=2):
    """Output ID of products of which the number of reviews >= threshold.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
      threshold: the threshold (default: 2).
    """
    for p in graph.products:
        if len(graph.retrieve_reviewers(p)) >= threshold:
            output.write(p.name)
            output.write("\n")


def filter_product(graph, output, target, csv_format=False):
    """Output reviews posted to products of which IDs match the given set of IDs.

    The output format is JSON and the scheme as::

        {
            "member_id": <Reviewer ID>,
            "product_id": <Product ID>,
            "rating": <Rating score>,
            "date": <Date the review posted>
        }

    In the outputs, one line represents one JSON object.

    CSV format is also supported to output results.
    In this option, the first line shows a header.

    Args:
      graph: Graph instance to which the target dataset is loaded.
      output: a writable object.
      target: a list of target product IDs.
      csv_format: If True, outputs will be formatted in CSV format.
    """
    if csv_format:
        writer = CSVWriter(output, ("member_id", "product_id", "rating", "date"))
    else:
        writer = JSONWriter(output)

    targets = {name for name in target}
    for p in graph.products:
        if p.name in targets:
            for r in graph.retrieve_reviewers(p):
                review = graph.retrieve_review(r, p)
                date = review.date
                if date:
                    date = datetime.datetime.strptime(
                        str(review.date), "%Y%m%d").strftime("%Y-%m-%d")
                writer.write({
                    "member_id": r.name,
                    "product_id": p.name,
                    "rating": review.score,
                    "date": date
                })


def review_variance(graph, output, target=None, csv_format=False):
    """Output variances of reviews for each product.

    Each line of the output will be formatted as a JSON document,
    of which schema is as::

        {
          "product_id": <Product ID>,
          "size": <number of reviews>,
          "variance": <variance of reviews>
        }

    In the outputs, one line represents one JSON object.

    CSV format is also supported to output results.
    In this option, the first line shows a header.

    If target is supplied, only products of which id is in the target will be
    outputted.

    Args:
      data: a readable object containing reviews.
      output: a writable object to be outputted results.
      target: an iterable of target product ids (default: None).
      csv_format: If True, outputs will be formatted in CSV format.
    """
    if csv_format:
        writer = CSVWriter(output, ("member_id", "product_id", "rating", "date"))
    else:
        writer = JSONWriter(output)

    if target:
        target_ids = {s.strip() for s in target}
    else:
        target_ids = None

    for p in graph.products:

        if target_ids and p.name not in target_ids:
            continue

        reviews = [
            graph.retrieve_review(r, p).score
            for r in graph.retrieve_reviewers(p)
        ]

        if len(reviews) == 0:
            continue

        writer.write({
            "product_id": p.name,
            "size": len(reviews),
            "variance": np.var(reviews)
        })


def _dispatch(cmd, dataset, dataset_param, additional, **kwargs):
    """Dispatch command to be run.
    """
    graph = helper.load(ria.one_graph(), dataset, dataset_param)
    for item in additional:
        with open(item) as fp:
            dataset_io.load(graph, fp)

    logging.info("Start analyzing.")
    cmd(graph=graph, **kwargs)


def main():
    """The main function.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    parser = dsargparse.ArgumentParser(main=main)
    parser.add_argument(
        "--output", default=sys.stdout, type=dsargparse.FileType("w"),
        help="Output file (default: stdout).")
    parser.add_argument(
        "dataset", choices=
        helper.DATASETS.keys(),
        help=(
            "choose one dataset to be analyzed.\n"
            "If choose `file`, give a file path via dataset-param with file key\n"
            "i.e. --dataset-param file=<path>."))
    parser.add_argument(
        "--dataset-param", action="append", default=[], dest="dataset_param",
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))
    parser.add_argument(
        "--additional-dataset", action="append", default=[], dest="additional",
        help=(
            "add an additional dataset file to be loaded.\n"
            "This option can be set multiply."))

    subparsers = parser.add_subparsers()

    # Reviewer
    reviewer_cmd = subparsers.add_parser(
        name="reviewer", help="analyze reviewer information").add_subparsers()

    retrieve_reviewers_cmd = reviewer_cmd.add_parser(
        retrieve_reviewers, name="retrieve")
    retrieve_reviewers_cmd.add_argument(
        "target", type=dsargparse.FileType("r"),
        help="a file containing target product IDs.")

    active_reviewer_cmd = reviewer_cmd.add_parser(
        active_reviewers, name="active")
    active_reviewer_cmd.add_argument("--threshold", type=int, default=2)

    size_cmd = reviewer_cmd.add_parser(reviewer_size)
    size_cmd.add_argument(
        "target", type=dsargparse.FileType("r"))
    size_cmd.add_argument(
        "--csv", action="store_true", dest="csv_format",
        help="Outputs will be formatted in CSV format.")

    filter_reviewer_cmd = reviewer_cmd.add_parser(
        filter_reviewers, name="filter")
    filter_reviewer_cmd.add_argument(
        "target", type=dsargparse.FileType("r"),
        help="a file containing target reviewer IDs.")
    filter_reviewer_cmd.add_argument(
        "--csv", action="store_true", dest="csv_format",
        help="Outputs will be formatted in CSV format.")

    # Product
    product_cmd = subparsers.add_parser(
        name="product", help="analyze product information").add_subparsers()

    rating_average_cmd = product_cmd.add_parser(rating_average, name="average")
    rating_average_cmd.add_argument(
        "--csv", action="store_true", dest="csv_format",
        help="Outputs will be formatted in CSV format.")

    product_cmd.add_parser(distinct_product, name="distinct")

    popular_products_cmd = product_cmd.add_parser(
        popular_products, name="popular")
    popular_products_cmd.add_argument("--threshold", type=int, default=2)

    filter_product_cmd = product_cmd.add_parser(filter_product, name="filter")
    filter_product_cmd.add_argument(
        "target", type=dsargparse.FileType("r"),
        help="a file containing target product IDs.")
    filter_product_cmd.add_argument(
        "--csv", action="store_true", dest="csv_format",
        help="Outputs will be formatted in CSV format.")

    review_variance_cmd = product_cmd.add_parser(
        review_variance, name="variance")
    review_variance_cmd.add_argument(
        "--target", type=dsargparse.FileType("r"),
        help="a file consisting of a list of product ids.")
    review_variance_cmd.add_argument(
        "--csv", action="store_true", dest="csv_format",
        help="Outputs will be formatted in CSV format.")

    try:
        _dispatch(**vars(parser.parse_args()))
    except KeyboardInterrupt:
        return "Canceled"
    except Exception as e:  # pylint: disable=broad-except
        logging.exception("Untracked exception occurred.")
        return e.message
    finally:
        logging.shutdown()


if __name__ == "__main__":
    main()
