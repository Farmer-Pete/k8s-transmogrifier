import sys
import argparse
import collections

import lib.testing


__parser = argparse.ArgumentParser(
    description=(
        'Transmogrifier: Reads Kubernetes configmaps and secrets, '
        'generating all kinds of useful things'
    ),
)

__parser.add_argument(
    'configdir', metavar='CONFIG_DIR',
    help='the directory to the k8s config files'
)

__parser_buffer = collections.defaultdict(list)


def add(group, flag, **kwargs):
    __parser_buffer[group].append([flag, kwargs])


def usage(message=None):
    __parser.error(message=message)


def build():
    for group in sorted(__parser_buffer):
        group_parser = __parser.add_argument_group(group)

        for flag, kwargs in sorted(__parser_buffer[group], key=lambda item: item[0]):
            group_parser.add_argument(flag, **kwargs)


def parse():

    if '--test' in sys.argv:
        lib.testing.test()
        sys.exit(0)

    return __parser.parse_args()

