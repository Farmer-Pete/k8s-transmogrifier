import os
import jinja2

import plugins
import lib.cmdline

from . import AbstractLanguage

from lib.decorators import classproperty


class JavaLanaguage(AbstractLanguage):

    def __init__(self, args):
        super(JavaLanaguage, self).__init__(args)
        self._package = args.code_java_package

        if not self._package:
            lib.cmdline.usage('Package definition is required for Java')

        with open(plugins.resource_file(__file__, 'TransmogrifierFileProxy.java.template')) as tpl:
            self._template_fileproxy = jinja2.Template(
                tpl.read()
            )

    @classproperty
    def name(self):
        return "java"

    @property
    def extension(self):
        return ".java"

    @property
    def template_config(self):
        with open(plugins.resource_file(__file__, 'Config.java.template')) as tpl:
            return tpl.read()

    @property
    def template_pod(self):
        with open(plugins.resource_file(__file__, 'Pod.java.template')) as tpl:
            return tpl.read()

    @classproperty
    def argextras(cls):
        from plugins.transmogrifiers import ArgExtra

        return [
            ArgExtra('package', 'package name of the generated files')
        ]

    @property
    def _type_map(self):
        return {
            int: 'Integer',
            float: 'Double',
            str: 'String',
            bool: 'Boolean',
            list: lambda this, name, value: 'List<%s>' % (
                this.get_type(name, value[0])
            ),
            dict: lambda this, name, value: 'Map<%s, %s>' % (
                this.get_type(name, next(iter(value.keys()))),
                this.get_type(name, next(iter(value.values())))
            ),
        }

    @property
    def _root_map(self):
        return {
            int: 'Integer',
            float: 'Double',
            str: 'String',
            bool: 'Boolean',
            list: 'List',
            dict: 'Map'
        }

    @property
    def _init_map(self):
        return {
            int: '0',
            float: '0.0',
            str: '""',
            bool: 'false',
            list: 'new ArrayList<>()',
            dict: 'new HashMap<>()'
        }

    def prepare(self, configs, target_dir):
        target = os.path.join(target_dir, 'TransmogrifierFileProxy.java')

        with open(target, 'w') as fptr:
            fptr.write(
                self._template_fileproxy.render(package=self._package)
            )

    def _prerender_config(self, kwargs):
        kwargs['package'] = self._package

    def _prerender_pod(self, kwargs):
        self._prerender_config(kwargs)

