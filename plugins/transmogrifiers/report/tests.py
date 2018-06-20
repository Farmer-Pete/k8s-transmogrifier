import unittest
import tempfile

from . import ReportTransmogrifier


class _ReportTransmogrifier(ReportTransmogrifier):

    def __init__(self, args):
        self._args = args


class _Mock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class _Mock_Layout(object):

    def __init__(self):
        self._kwargs = {}

    def render(self, **kwargs):
        self._kwargs = kwargs
        return str(kwargs)


class __Report_Test(unittest.TestCase):

    def test_transmogrify(self):
        config = _Mock(
            configmaps={
                'file1.json': ('{"key1": "value1"}', '.json', ['var1'], True),
                'file2.json': ('{"key2": "value2"}', '.json', ['var2'], True),
            },
            secrets={
                'secret1.json': ('{"secret1": "password1"}', '.json', ['var3'], True),
                'secret2.json': ('{"secret2": "password2"}', '.json', [], True),
            },
            pods={
                'POD1': [
                    ['file1.json', 'cm', True],
                    ['secret1.json', 'sec', True]
                ], 'POD2': [
                    ['file2.json', 'cm', True],
                    ['secret2.json', 'sec', True]
                ],
            },
            rpods={
                'file1.json': ['POD1'],
                'secret1.json': ['POD1'],
                'file2.json': ['POD2'],
                'secret2.json': ['POD2']
            },
            variables={
                'var1': ['file1.json'],
                'var2': ['file2.json'],
                'var3': ['file3.json']
            }

        )

        report = _ReportTransmogrifier(_Mock(report_title="My Title"))
        report._layout = _Mock_Layout()

        with tempfile.NamedTemporaryFile() as f:
            report.transmogrify(config, f.name)

        kwargs = report._layout._kwargs

        self.assertEqual(kwargs['title'], 'My Title')
        self.assertEqual(kwargs['configmaps_list'], [
            ['file1.json', '{"key1": "value1"}', ['var1'], True, '.json', ['POD1']],
            ['file2.json', '{"key2": "value2"}', ['var2'], True, '.json', ['POD2']]
        ])
        self.assertEqual(kwargs['secrets_list'], [
            ['secret1.json', '{"secret1": "password1"}', ['var3'], True, '.json', ['POD1']],
            ['secret2.json', '{"secret2": "password2"}', [], True, '.json', ['POD2']]
        ])
        self.assertEqual(
            kwargs['pods_list'], [(
                'POD1',
                [['file1.json', 'cm', True],
                 ['secret1.json', 'sec', True]]
            ), (
                'POD2',
                [['file2.json', 'cm', True],
                 ['secret2.json', 'sec', True]]
            )]
        )
        self.assertEqual(
            kwargs['invalid_files'],
            {'configmaps': [], 'secrets': [], 'pods': []}
        )
        self.assertEqual(kwargs['pod_files_matrix'], [
            (
                'POD1',
                [['file1.json', True], ['file2.json', False],
                 ['secret1.json', True], ['secret2.json', False]]
            ), (
                'POD2',
                [['file1.json', False], ['file2.json', True],
                 ['secret1.json', False], ['secret2.json', True]]
            )
        ])

    def test_transmogrify_invalid_files(self):
        config = _Mock(
            configmaps={
                'file1.json': ('{"key1": "value1"}', '.json', [], False),
                'file2.json': ('{"key2": "value2"}', '.json', [], False),
            },
            secrets={
                'secret1.json': ('{"secret1": "password1"}', '.json', [], False),
                'secret2.json': ('{"secret2": "password2"}', '.json', [], False),
            },
            pods={
                'POD1': [
                    ['file_bad1.json', 'cm', False],
                    ['secret_bad1.json', 'sec', False]
                ], 'POD2': [
                    ['file_bad2.json', 'cm', False],
                    ['secret_bad2.json', 'sec', False]
                ],
            },
            variables={},
            rpods={
                'file_bad1.json': ['POD1'],
                'secret_bad1.json': ['POD1'],
                'file_bad2.json': ['POD2'],
                'secret_bad2.json': ['POD2']
            }

        )

        report = _ReportTransmogrifier(_Mock(report_title="My Title"))
        report._layout = _Mock_Layout()

        with tempfile.NamedTemporaryFile() as f:
            report.transmogrify(config, f.name)

        kwargs = report._layout._kwargs

        self.assertEqual(kwargs['title'], 'My Title')
        self.assertEqual(kwargs['configmaps_list'], [
            ['file1.json', '{"key1": "value1"}', [], False, '.json', []],
            ['file2.json', '{"key2": "value2"}', [], False, '.json', []]
        ])
        self.assertEqual(kwargs['secrets_list'], [
            ['secret1.json', '{"secret1": "password1"}', [], False, '.json', []],
            ['secret2.json', '{"secret2": "password2"}', [], False, '.json', []]
        ])
        self.assertEqual(
            kwargs['pods_list'], [(
                'POD1',
                [['file_bad1.json', 'cm', False],
                 ['secret_bad1.json', 'sec', False]]
            ), (
                'POD2',
                [['file_bad2.json', 'cm', False],
                 ['secret_bad2.json', 'sec', False]]
            )]
        )
        self.assertEqual(
            kwargs['invalid_files'],
            {
                'configmaps': ['file1.json', 'file2.json'],
                'secrets': ['secret1.json', 'secret2.json'],
                'pods': [
                    ('POD1', 'file_bad1.json'),
                    ('POD1', 'secret_bad1.json'),
                    ('POD2', 'file_bad2.json'),
                    ('POD2', 'secret_bad2.json')
                ]
            }
        )
        self.assertEqual(kwargs['pod_files_matrix'], [
            (
                'POD1',
                [['file1.json', False], ['file2.json', False],
                 ['secret1.json', False], ['secret2.json', False]]
            ), (
                'POD2',
                [['file1.json', False], ['file2.json', False],
                 ['secret1.json', False], ['secret2.json', False]]
            )
        ])

