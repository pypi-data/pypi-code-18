"""The driver and CLI argument parser for classifying and sorting images."""

import os
import sys
import argparse
import logging
import numpy as np
import tensorflow as tf
import ntpath
from functools import reduce
from .util import *
from .tfutil import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

ERROR_DIR = 'error'

confidence_intervals = [0.9, 0.7, 0.5, 0.0]
confidence_dirs = ['high confidence', 'confident', 'low confidence', 'negative']

def sort_multiclass(img, predictions, labels, directory):
  """Sort an image based on it's top predicted class.

  Parameters
  ----------
  img : str
    A path to the classified image
  predictions : list
    A list of the predicted values, where indices correspond to labels
  labels: list
    A list of the classes considered, where indices correspond to predictions
  directory: str
    The parent directory to sort the image into.
  """
  # Take precitions
  # Move image to top scoring label
  idx = np.argmax(predictions)
  animal = labels[idx]
  animal_dir = os.path.join(directory, animal)
  mv(img, animal_dir)

def sort_singleclass(img, predictions, target, labels, confidence_thresh, directory):
  """Sort an image based on the confidence that the image matches target classification.

  Parameters
  ----------

  img : str
    A path to the classified image
  predictions : list
    A list of the predicted values, where indices correspond to labels
  target : str
    The target classification, corresponding to a value in labels
  labels: list
    A list of the classes considered, where indices correspond to predictions
  confidence_thresh: list
    A list of thresholds for us in sorting.
  directory: str
    The parent directory to sort the image into
  """
  global confidence_dirs

  idx = labels.index(target)
  prob = predictions[idx]

  expanded_dirs = [os.path.join(directory, d) for d in confidence_dirs]

  ## Assumes decreasing order
  for i in range(len(confidence_thresh)):
    if prob > confidence_thresh[i]:
      mv(img, expanded_dirs[i])
      break

def run(unsorted_imgs, csv, singleclass, multiclass, model_file, labels_file, confidence_thresh, output_dir):
  """Run classification and sorting."""
  create_graph(model_file)
  imgs = ls(unsorted_imgs)

  with open(labels_file) as f:
    labels = f.read().splitlines()

  if csv:
    csv_file = open(csv, 'w')
    csv_file.write(stringify(labels))

  if singleclass:
    setup_dirs(confidence_dirs + [ERROR_DIR], output_dir)

  if multiclass:
    setup_dirs(labels + [ERROR_DIR], output_dir)

  for img in imgs:
    try:
      predictions = classify(img)
    except:
      error_path = os.path.join(output_dir, ERROR_DIR)
      mv(img, error_path)
      logger.error("There was a problem classifying %s.  It has been moved to the directory %s" % (img, error_path))
      continue

    if csv:
      write_csv_line(csv_file, predictions)

    if singleclass:
      sort_singleclass(img, predictions, singleclass, labels, confidence_thresh, output_dir)
    elif multiclass:
      sort_multiclass(img, predictions, labels, output_dir)

  if csv:
    csv_file.close()

def main():
  """A command line driver for running sorting and classification."""
  global confidence_intervals
  parser = argparse.ArgumentParser(description='Classifies images using a tensorflow based classifier')

  parser.add_argument("unsorted", type=str)
  parser.add_argument("--model-dir", help="The directory that contains the model you want to use.  Defaults to `model`", type=str)
  parser.add_argument("--confidence-thresholds", help="A comma seperated list of thresholds for use with singleclass classifications.  Defaults to '0.9,0.7,0.5'", type=str)
  parser.add_argument("--csv", help="When classifying the images writes the results to a given csv file", type=str)
  parser.add_argument("--singleclass", help="This is the default Sorting Scheme. Performs binary classification on the images as the specified class. The results are tiered into folders based on confidence of result. You must choose multiclass or singleclass but not both.", type=str)
  parser.add_argument("--multiclass", help="Performs multiclass classification, sorting the input directory into the most likely class. You must choose multiclass or singleclass but not both.", action='store_true')
  parser.add_argument("--output-dir", help="The directory to output single or multiclass sorting. Defaults to 'classifications'", type=str)
  parser.add_argument("--verbose", help="Enables verbose logging.", action='store_true')

  args = parser.parse_args()

  model_file = os.path.join(args.model_dir, 'output_graph.pb')
  labels_file = os.path.join(args.model_dir, 'output_labels.txt')
  output_dir = args.output_dir if args.output_dir else 'classifications'

  if args.singleclass and args.multiclass:
    logger.critical("Please use singleclass or multiclass, but not both.  See --help for details on available options.")
    sys.exit(1)

  if args.verbose:
    logger.setLevel(logging.DEBUG)

  if args.confidence_thresholds:
    confidence_thresh = list(map(float, args.confidence_thresholds.split(',')))
  else:
    confidence_thresh = confidence_intervals

  run(args.unsorted, args.csv, args.singleclass, args.multiclass, model_file, labels_file, confidence_thresh, output_dir)
