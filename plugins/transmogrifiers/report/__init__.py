import copy
import time
import itertools
import datetime

import lib.cmdline

from lib.decorators import classproperty
from .. import AbstractTransmogrifier, ArgExtra


class ReportTransmogrifier(AbstractTransmogrifier):
    ''' Implementes report file generation '''

    def __init__(self, args):
        from . import layouts
        super(ReportTransmogrifier, self).__init__(args)

        self._layout = layouts.get(args.report_layout)
        self._configs = None

        if not self._layout:
            lib.cmdline.usage('Either missing or invalid report layout provided')

    @classproperty
    def name(cls):
        return 'report'

    @classproperty
    def description(cls):
        return 'generates reports'

    @classproperty
    def deserialize_flag(cls):
        return False

    @classproperty
    def arggroup(cls):
        __import__('plugins.transmogrifiers.report.layouts')  # so th children cmdline args will appear
        return 'Report Generation'

    @classproperty
    def argmeta(cls):
        return 'FILE'

    @classproperty
    def argextras(cls):
        return [
            ArgExtra(
                flag='title',
                description='title displayed on report',
                options={'default': 'Configuration Report'}
            )
        ]

    def transmogrify(self, configs, output):

        invalid_files = {
            'configmaps': [],
            'secrets': [],
            'pods': []
        }

        self._configs = configs

        for podname, podfiles in configs.pods.items():
            for filename, _, is_valid in podfiles:
                if not is_valid:
                    invalid_files['pods'].append((podname, filename))

        with open(output, 'w') as report:

            now = (datetime.datetime.now()
                   .strftime('%A, %B %d, %Y %I:%M.%S %p ') + '/'.join(time.tzname))

            report.write(
                self._layout.render(
                    title=self._args.report_title,
                    configmaps_list=self._config_smash(
                        configs.configmaps, invalid_files['configmaps']),
                    secrets_list=self._config_smash(configs.secrets, invalid_files['secrets']),
                    pods_list=sorted(configs.pods.items()),
                    timestamp=now,
                    invalid_files=invalid_files,
                    pod_files_matrix=self._pods_2_files_matrix(
                        configs.pods,
                        list(configs.configmaps.keys()) + list(configs.secrets.keys())
                    )
                )
            )

    def _config_smash(self, config, invalid_files_ptr):
        smashed = []

        for filename, (content, ext, is_valid) in sorted(config.items()):

            if not is_valid:
                invalid_files_ptr.append(filename)

            smashed.append([
                filename,
                content,
                is_valid,
                ext,
                self._configs.rpods[filename]
            ])

        return smashed

    def _pods_2_files_matrix(self, pods, files):
        counter = itertools.count()

        filedict = {
            filename: next(counter)
            for filename in files
        }

        blankrow = [
            [filename, False] for filename in files
        ]

        matrix = {}

        for podname, podfiles in pods.items():
            matrix[podname] = copy.deepcopy(blankrow)
            for configfile, _, _ in podfiles:
                try:
                    fileindex = filedict[configfile]
                except KeyError:
                    continue

                matrix[podname][fileindex][-1] = True

        return sorted(matrix.items())

