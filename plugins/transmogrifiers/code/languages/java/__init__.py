import os
import jinja2

import plugins.languages

from lib.decorators import classproperty

TEMPLATE_NAME_CONFIG = 'Config.java.template'
TEMPLATE_NAME_POD = 'Pod.java.template'


class JavaLanaguage(plugins.languages.AbstractLanguage):

    def __init__(self, args):
        super(JavaLanaguage, self).__init__(args)

        with open(os.path.join(self._args.templates, self.TEMPLATE_NAME_CONFIG)) as tpl:
            self.template_config = jinja2.Template(tpl.read())

        with open(os.path.join(self._args.templates, self.TEMPLATE_NAME_POD)) as tpl:
                self.template_pod = jinja2.Template(tpl.read())

    @classproperty
    def name(self):
        return "java"

    @property
    def extension(self):
        return ".java"

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

