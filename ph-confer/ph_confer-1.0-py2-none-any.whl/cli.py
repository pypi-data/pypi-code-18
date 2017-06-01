import argparse
import time
import traceback

import key_value_bridge
import template_manager
from within_template_config import confer_instance
from .exceptions import ConfigException


def main():
  main_parser = argparse.ArgumentParser(description='PH Confer')
  main_parser.add_argument('templates', nargs='+')
  main_parser.add_argument('--onetime', action='store_true')
  main_parser.add_argument('--auto-add-watches', action='store_false')
  main_parser.add_argument('--watch-period', type=int, default=60)
  main_parser.add_argument(
      '--kv-endpoints', type=str, default='localhost:2379,localhost:2380'
  )

  args = main_parser.parse_args()
  endpoints = tuple([
    (s.split(':', 1)[0], int(s.split(':')[1]))
    for s in args.kv_endpoints.split(',')
  ])
  while True:
    all_listen_keys = set()
    for d in args.templates:
      print('Rendering template {}...'.format(d))
      try:
        key_value_bridge.setinstance(
            watch_timeout=args.watch_period,
            auto_add_watches=args.auto_add_watches,
            endpoints=endpoints
        )
        template_changed = template_manager.run_template(d)
        if template_changed:
          print('Template {} changed.'.format(d))
      except ConfigException:
        traceback.print_exc()
      all_listen_keys.update(confer_instance.watched_keys)
    if args.onetime:
      return
    print('Waiting for {} seconds or for a watched key to change.'
      .format(args.watch_period))
    if all_listen_keys:
      key_value_bridge.watch_keys(all_listen_keys)
    else:
      time.sleep(args.watch_period)
