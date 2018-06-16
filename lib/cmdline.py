import argparse

command_line_parser = argparse.ArgumentParser(
    description=(
        'Transmogrifier: Reads K8S configmaps and secrets '
        'and generates all kinds of useful things'
    )
)

command_line_parser.add_argument(
    'configdir', metavar='CONFIG_DIR',
    help='The directory to the k8s config files'
)

