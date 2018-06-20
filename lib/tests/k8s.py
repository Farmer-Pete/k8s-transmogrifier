import os
import unittest
from lib.k8s import K8SConfigs


class __K8SConfigs_Test_Base(unittest.TestCase):

    _tempdir = None

    @classmethod
    def tearDownClass(cls, kwargs=None):
        import shutil
        if cls._tempdir:
            shutil.rmtree(cls._tempdir)

    @classmethod
    def _write(cls, directory, content):
        for key, value in content.items():
            if '.' in key:
                with open(os.path.join(directory, key), 'w') as f:
                    f.write(value)
            else:
                newdir = os.path.join(directory, key)
                os.makedirs(newdir)
                cls._write(newdir, value)


class __K8SConfigs_Test(__K8SConfigs_Test_Base):

    DIRECTORY_SOURCE = {
        K8SConfigs.DIR_NAME_CONFIGMAPS: {
            'config_map_1.json': '{"key_c1_1": "${VAR_CM_1}", "key_c1_2": "value_c1_2"}',
            'config_map_2.json': '{"key_c2_1": "value_c2_1", "key_c2_2": "${VAR_CM_2}"}',
        }, K8SConfigs.DIR_NAME_SECRETS: {
            'secret_1.json': '{"key_s1_1": "${VAR_SEC_1}", "key_s1_2": "value_s1_2"}',
            'secret_2.json': '{"key_s2_1": "value_21_1", "key_s2_2": "${VAR_SEC_2}"}',
        }, K8SConfigs.DIR_METADATA: {
            K8SConfigs.FILE_METADATA_PODS: (
                'POD1, config_map_1.json, cm\n'
                'POD1, secret_1.json, sec\n'
                'POD2, config_map_2.json, cm\n'
                'POD2, secret_2.json, sec\n'
            )
        }
    }

    DIRECTORY_OUT_OBJ = {
        K8SConfigs.DIR_NAME_CONFIGMAPS: {
            'config_map_1.json': ({"key_c1_1": "${VAR_CM_1}", "key_c1_2": "value_c1_2"}, '.json', ['VAR_CM_1'], True),
            'config_map_2.json': ({"key_c2_1": "value_c2_1", "key_c2_2": "${VAR_CM_2}"}, '.json', ['VAR_CM_2'], True)
        }, K8SConfigs.DIR_NAME_SECRETS: {
            'secret_1.json': ({"key_s1_1": "${VAR_SEC_1}", "key_s1_2": "value_s1_2"}, '.json', ['VAR_SEC_1'], True),
            'secret_2.json': ({"key_s2_1": "value_21_1", "key_s2_2": "${VAR_SEC_2}"}, '.json', ['VAR_SEC_2'], True),
        }, K8SConfigs.DIR_METADATA: {
            K8SConfigs.FILE_METADATA_PODS: {
                'POD1': [
                    ['config_map_1.json', 'cm', True],
                    ['secret_1.json', 'sec', True]
                ], 'POD2': [
                    ['config_map_2.json', 'cm', True],
                    ['secret_2.json', 'sec', True]
                ],
            },
            'reverse_pods': {
                'config_map_1.json': ['POD1'],
                'config_map_2.json': ['POD2'],
                'secret_1.json': ['POD1'],
                'secret_2.json': ['POD2']
            }
        }
    }

    DIRECTORY_OUT_STR = {
        K8SConfigs.DIR_NAME_CONFIGMAPS: {
            'config_map_1.json': ('{"key_c1_1": "${VAR_CM_1}", "key_c1_2": "value_c1_2"}', '.json', ['VAR_CM_1'], True),
            'config_map_2.json': ('{"key_c2_1": "value_c2_1", "key_c2_2": "${VAR_CM_2}"}', '.json', ['VAR_CM_2'], True)
        }, K8SConfigs.DIR_NAME_SECRETS: {
            'secret_1.json': ('{"key_s1_1": "${VAR_SEC_1}", "key_s1_2": "value_s1_2"}', '.json', ['VAR_SEC_1'], True),
            'secret_2.json': ('{"key_s2_1": "value_21_1", "key_s2_2": "${VAR_SEC_2}"}', '.json', ['VAR_SEC_2'], True),
        }, K8SConfigs.DIR_METADATA: DIRECTORY_OUT_OBJ[K8SConfigs.DIR_METADATA]
    }

    @classmethod
    def setUpClass(cls, kwargs=None):
        import tempfile
        cls._tempdir = tempfile.mkdtemp()
        cls._write(cls._tempdir, cls.DIRECTORY_SOURCE)

    def test_k8s_deserialize(self):
        config = K8SConfigs(self._tempdir, True)

        self.assertTrue(
            dict(config.configmaps),
            self.DIRECTORY_OUT_OBJ[K8SConfigs.DIR_NAME_CONFIGMAPS]
        )

        self.assertEqual(
            dict(config.secrets),
            self.DIRECTORY_OUT_OBJ[K8SConfigs.DIR_NAME_SECRETS]
        )

        self.assertEqual(
            dict(config.pods),
            self.DIRECTORY_OUT_OBJ[K8SConfigs.DIR_METADATA][K8SConfigs.FILE_METADATA_PODS]
        )

        self.assertEqual(
            dict(config.rpods),
            self.DIRECTORY_OUT_OBJ[K8SConfigs.DIR_METADATA]['reverse_pods']
        )

        with open(os.path.join(self._tempdir, K8SConfigs.DIR_METADATA, K8SConfigs.FILE_METADATA_VARS)) as f:
            self.assertEqual(
                f.read().strip(),
                (
                    'config_map_1.json,VAR_CM_1,\n'
                    'config_map_2.json,VAR_CM_2,\n'
                    'secret_1.json,VAR_SEC_1,\n'
                    'secret_2.json,VAR_SEC_2,'
                )
            )

    def test_k8s_no_deserialize(self):
        config = K8SConfigs(self._tempdir, False)

        self.assertTrue(
            dict(config.configmaps),
            self.DIRECTORY_OUT_STR[K8SConfigs.DIR_NAME_CONFIGMAPS]
        )

        self.assertEqual(
            dict(config.secrets),
            self.DIRECTORY_OUT_STR[K8SConfigs.DIR_NAME_SECRETS]
        )

        self.assertEqual(
            dict(config.pods),
            self.DIRECTORY_OUT_STR[K8SConfigs.DIR_METADATA][K8SConfigs.FILE_METADATA_PODS]
        )

        self.assertEqual(
            dict(config.rpods),
            self.DIRECTORY_OUT_STR[K8SConfigs.DIR_METADATA]['reverse_pods']
        )


class __K8SConfigs_Error_Test(__K8SConfigs_Test_Base):

    DIRECTORY_ERR_SOURCE = {
        K8SConfigs.DIR_NAME_CONFIGMAPS: {
            'config_map_good.json': '{"key_c1_1": "value_c1_1", "key_c1_2": "value_c1_2"}',
            'config_map_error.json': 'this is a bad config',
        }, K8SConfigs.DIR_NAME_SECRETS: {
            'secret_good.json': '{"key_s1_1": "value_s1_1", "key_s1_2": "value_s1_2"}',
            'secret_error.json': 'this is a bad secret',
        }, K8SConfigs.DIR_METADATA: {
            K8SConfigs.FILE_METADATA_PODS: (
                'POD1, config_map_good.json, cm\n'
                'POD1, secret_good.json, sec\n'
                'POD2, config_map_error.json, cm\n'
                'POD2, secret_error.json, sec\n'
                'ERR_POD, does_not_exist.json, cm'
            )
        }
    }

    DIRECTORY_OUT_ERR_STR = {
        K8SConfigs.DIR_NAME_CONFIGMAPS: {
            'config_map_good.json': ('{"key_c1_1": "value_c1_1", "key_c1_2": "value_c1_2"}', '.json', [], True),
            'config_map_error.json': ('this is a bad config', '.json', False)
        }, K8SConfigs.DIR_NAME_SECRETS: {
            'secret_good.json': ('{"key_s1_1": "value_s1_1", "key_s1_2": "value_s1_2"}', '.json', [], True),
            'secret_error.json': ('this is a bad secret', '.json', [], False),
        }, K8SConfigs.DIR_METADATA: {
            K8SConfigs.FILE_METADATA_PODS: {
                'POD1': [
                    ['config_map_good.json', 'cm', True],
                    ['secret_good.json', 'sec', True]
                ], 'POD2': [
                    ['config_map_error.json', 'cm', True],
                    ['secret_error.json', 'sec', True]
                ], 'ERR_POD': [
                    ['does_not_exist.json', 'cm', False]
                ]
            },
            'reverse_pods': {
                'config_map_good.json': ['POD1'],
                'config_map_error.json': ['POD2'],
                'secret_good.json': ['POD1'],
                'secret_error.json': ['POD2'],
                'does_not_exist.json': ['ERR_POD']
            }
        }
    }

    @classmethod
    def setUpClass(cls, kwargs=None):
        import tempfile
        cls._tempdir = tempfile.mkdtemp()
        cls._write(cls._tempdir, cls.DIRECTORY_ERR_SOURCE)

    def test_k8s_no_deserialize_errors(self):
        config = K8SConfigs(self._tempdir, deserialize=False)

        self.assertTrue(
            dict(config.configmaps),
            self.DIRECTORY_OUT_ERR_STR[K8SConfigs.DIR_NAME_CONFIGMAPS]
        )

        self.assertEqual(
            dict(config.secrets),
            self.DIRECTORY_OUT_ERR_STR[K8SConfigs.DIR_NAME_SECRETS]
        )

        self.assertEqual(
            dict(config.pods),
            self.DIRECTORY_OUT_ERR_STR[K8SConfigs.DIR_METADATA][K8SConfigs.FILE_METADATA_PODS]
        )

        self.assertEqual(
            dict(config.rpods),
            self.DIRECTORY_OUT_ERR_STR[K8SConfigs.DIR_METADATA]['reverse_pods']
        )

