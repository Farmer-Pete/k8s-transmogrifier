import plugins

from .. import languages

from lib.decorators import classproperty


class JavaLanaguage(languages.AbstractLanguage):

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

