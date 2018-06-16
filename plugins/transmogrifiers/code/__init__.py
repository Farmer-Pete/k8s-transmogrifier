import os
import re
import glob
import itertools

import lib.core
import plugins.transmogrifiers
import plugins.languages

from lib.decorators import classproperty


class CodeTransmogrifier(plugins.transmogrifiers.AbstractTransmogrifier):
    ''' Implementes code generation '''

    def __init__(self, args):
        super(CodeTransmogrifier, self).__init__(args)
        self._language = plugins.languages.get(args.code_language)

    @classproperty
    def name(self):
        return 'code'

    @classproperty
    def description(self):
        return 'Generates code to load configurations, supports several languages'

    def _split_file_name(self, file_name):
        # Don't retun the last component as that is the file extension
        return file_name.replace('-', '.').split('.')[:-1]

    def _make_config_class_name(self, file_name_parts):
        # file_name_parts is assumed to contain the output of _split_file_name()
        cls = ''
        for part in file_name_parts:
            if type(part) in (list, tuple):
                cls += self._make_config_class_name(part)
            else:
                cls += part.title()

        return cls

    def _prettify(self, file_name):
        with open(file_name, 'r') as fptr:
            code = fptr.read()

        with open(file_name, 'w') as fptr:
            fptr.write(
                # Delete extra whitespace
                re.sub(r'^\s+$', '', code, flags=re.MULTILINE)
            )

    def _find_longest_prefix(self, needle, haystack):

        longest = []

        for item in haystack:

            zipper = zip(needle, item)

            prefix_pairs = itertools.takewhile(
                lambda pair: pair[0] == pair[1],
                zipper
            )

            prefix = [pair[0] for pair in prefix_pairs]

            if prefix != needle and len(prefix) > len(longest):
                longest = prefix

        if len(longest) > 1:
            _longest = list()
            _longest.append((longest[0], longest[1]))
            _longest.extend(longest[2:])
            return _longest

        return longest

    def _find_common_config(self, configs):
        common_names = set.intersection(
            *map(set, configs)  # Turns all key lists into sets
        )

        return {
            name: configs[0][name]
            for name in common_names
        }

    def hierarchize_config(self, config_dict):
        ''' Discovers possible base classses '''

        haystack = {
            tuple(self._split_file_name(file_name)): [file_name, config]
            for file_name, (config, _, _), in config_dict.items()
        }

        hierarchy = dict()

        # Phase one: determine the prefixes
        for file_parts, (file_name, config) in haystack.items():
            prefix = self._find_longest_prefix(file_parts, haystack)

            if not prefix:
                raise ValueError('Unable to find prefix for: %s' % file_name)

            parent = None

            for index in range(1, len(prefix)):
                prefix_slice = tuple(prefix[0:index])
                hierarchy.setdefault(
                    prefix_slice,
                    {'parent': parent, 'configs': []}
                )
                hierarchy[prefix_slice]['configs'].append(config)
                parent = prefix_slice

            haystack[file_parts].append(parent)

        # Phase two: yield the base classes
        for prefix, metadata in hierarchy.items():

            yield {
                'file_parts': prefix,
                'file_type': os.path.splitext(file_name)[-1],
                'file_name': 'Abstract-' + self._make_config_class_name(prefix),
                'config': self._find_common_config(metadata['configs']),
                'is_abstract': True,
                'parent': metadata['parent']
            }

        # Phase three: yield the config
        for file_parts, (file_name, config, parent) in haystack.items():
            yield {
                'file_parts': file_parts,
                'file_type': os.path.splitext(file_name)[-1],
                'file_name': file_name,
                'config': config,
                'is_abstract': False,
                'parent': parent
            }

    def generate_config_objs(self, file_name, file_type, file_parts, config,
                             parent=None, is_abstract=False, is_secret=False):
        ''' Generates the Java config classes '''

        variables = list()
        class_name = self._make_config_class_name(file_parts)

        if file_type not in ('.yaml', '.json'):
            return

        if is_abstract:
            class_name = 'Abstract' + class_name

        _type = type(config)

        if _type == dict:
            for name, value in sorted(config.items()):

                var = ''.join(part[0].upper() + part[1:]
                              for part in name.split('_'))

                variables.append({
                    'name': name,
                    'var': var,
                    'Var': var[0].upper() + var[1:],
                    'type': self._language.get_type(name, value),
                    'root_type': self._language.get_root_type(name, value),
                    'init': self._language.get_init(name, value)
                })

        if not variables and not is_abstract:
            return

        target = os.path.join(self._args.output, class_name + self._language.extension)

        with open(target, 'w') as code:
            code.write(
                self.template_config.render(
                    variables=variables,
                    class_name=class_name,
                    config_file=file_name,
                    is_secret=is_secret,
                    is_abstract=is_abstract,
                    parent=self._make_config_class_name(
                        ['abstract'] + list(parent)
                    ) if parent else None
                )
            )

        self._prettify(target)

    def generate_pod_objs(self, pod_type, files):
        ''' Generates the Java pod classes '''

        configs = [filename for filename, filetype, _ in files if filetype == lib.core.K8SConfigs.CONFIGTYPE_CONFIGMAP]
        secrets = [filename for filename, filetype, _ in files if filetype == lib.core.K8SConfigs.CONFIGTYPE_SECRET]

        class_name = 'POD-%s-CONFIG' % pod_type
        class_name = ''.join(part.title() for part in class_name.split('-'))

        objects = set()

        objects.update(
            self._make_config_class_name(
                self._split_file_name(config)) for config in configs)
        objects.update(
            self._make_config_class_name(
                self._split_file_name(secret)) for secret in secrets)

        for obj in list(objects):
            if not os.path.exists(os.path.join(self.args.output, obj + self._language.extension)):
                objects.remove(obj)

        target = os.path.join(self.args.output, class_name + self._language.extension)

        with open(target, 'w') as code:
            code.write(
                self.template_pod.render(
                    pod_type=pod_type,
                    class_name=class_name,
                    configs=sorted(configs),
                    secrets=sorted(secrets),
                    objects=sorted(objects)
                )
            )

        self._prettify(target)

    def transmogrify(self):

        paths = glob.glob(
            os.path.join(
                self._args.output, '*' + self._language.extension
            )
        )

        for path in paths:
            os.unlink(path)

        for metadata in self.hierarchize_config(self.configs.configmaps):
            self.generate_config_objs(**metadata)

        for metadata in self.hierarchize_config(self.configs.secrets):
            self.generate_config_objs(is_secret=True, **metadata)

        for pod_type, files in self.configs.pods.items():
            self.generate_pod_objs(pod_type, files)

