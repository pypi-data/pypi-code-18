# -*- coding: utf-8 -*-

import yaml, argparse, argcomplete

def load_yaml(path):
  with open(path, "r") as stream:
    return yaml.safe_load(stream)

def main():

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  doc = load_yaml("/tmp/sytssh-projectname.yaml")

  for key, value in doc.items():
    project_arg = subparsers.add_parser(key)

  argcomplete.autocomplete(parser)
  args = parser.parse_args()


if __name__ == "__main__":
    main()
