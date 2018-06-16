import copy
import time
import itertools
import datetime

import plugins.transmogrifiers

from lib.decorators import classproperty
from ... import transmogrifiers


class ReportTransmogrifier(transmogrifiers.AbstractTransmogrifier):
    ''' Implementes report file generation '''

    def __init__(self, args):
        import plugins.transmogrifiers.report.layouts

        super(ReportTransmogrifier, self).__init__(args, deserialize=False)
        self._layout = plugins.transmogrifiers.report.layouts.get(args.web_layout)

    @classproperty
    def name(cls):
        return 'report'

    @classproperty
    def description(cls):
        return 'Generates reports'

    @classproperty
    def arggroup(cls):
        __import__('plugins.transmogrifiers.report.layouts')  # so th children cmdline args will appear
        return 'Report Generation'

    def transmogrify(self):

        invalid_files = {
            'configmaps': [],
            'secrets': [],
            'pods': []
        }

        for podname, podfiles in self.configs.pods.items():
            for filename, _, is_valid in podfiles:
                if not is_valid:
                    invalid_files['pods'].append((podname, filename))

        with open(self.args.report_file, 'w') as report:

            now = (datetime.datetime.now()
                   .strftime('%A, %B %d, %Y %I:%M.%S %p ') + '/'.join(time.tzname))

            report.write(
                self.layout.render(
                    configmaps_list=self._config_smash(self.configs.configmaps, invalid_files['configmaps']),
                    secrets_list=self._config_smash(self.configs.secrets, invalid_files['secrets']),
                    pods_list=sorted(self.configs.pods.items()),
                    timestamp=now,
                    invalid_files=invalid_files,
                    pod_files_matrix=self._pods_2_files_matrix(
                        self.configs.pods,
                        list(self.configs.configmaps.keys()) + list(self.configs.secrets.keys())
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
                self.EXT_2_CODE_HIGHLIGHT_CLASS[ext],
                self.configs.rpods[filename]
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

