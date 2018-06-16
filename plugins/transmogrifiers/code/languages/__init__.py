import jinja2

import plugins
import lib.cmdline

from lib.decorators import classproperty

NAME_TYPE_MAPPING = {
    'port': int  # TODO: Eventually move this to onfiguration file
}


class AbstractLanguage(object):

    _deserialize_config = True

    def __init__(self):
        self.__get_type_map = {}
        self.__get_root_map = {}
        self.__get_init_map = {}

        self.__init_map(self.__get_type_map, self._type_map)
        self.__init_map(self.__get_root_map, self._root_map)
        self.__init_map(self.__get_init_map, self._init_map)

        self._template_config = jinja2.Template(self.template_config)
        self._template_pod = jinja2.Template(self.template_pod)

    @classproperty
    def name(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    @property
    def extension(self):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    @classproperty
    def argextras(cls):
        return []

    @property
    def template_config(self, **kwargs):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    @property
    def template_pod(self, **kwargs):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    @property
    def _type_map(self):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    @property
    def _root_map(self):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    @property
    def _init_map(self):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    def __init_map(self, map, kwargs):
        for key, value in kwargs.items():

            if not hasattr(value, '__call__'):

                def wrapper(_value):
                    def inner(this, name, value):
                        return str(_value)
                    return inner
                value = wrapper(value)

            map[key] = value

    def __get_handler_from_map(self, data, field, key):

        handler = None

        if field in NAME_TYPE_MAPPING:
            handler = data.get(NAME_TYPE_MAPPING[field])
        elif isinstance(key, str):
            handler = data.get(str)
        elif isinstance(key, bool):
            handler = data.get(bool)
        elif isinstance(key, list):
            handler = data.get(list)
        elif isinstance(key, dict):
            handler = data.get(dict)
        elif isinstance(key, int):
            handler = data.get(int)
        elif isinstance(key, float):
            handler = data.get(float)
        else:
            raise ValueError('Unhandled type; value=%s' % (key,))

        if handler is None:
            raise NotImplementedError(
                'Child (%s) failed to implement handler for type: %s' % (self.__class__.__name__, type(key))
            )

        return handler

    def get_type(self, name, value):
        handler = self.__get_handler_from_map(
            self.__get_type_map,
            name,
            value
        )
        return handler(self, name, value)

    def get_root_type(self, name, value):
        handler = self.__get_handler_from_map(
            self.__get_root_map,
            name,
            value
        )
        return handler(self, name, value)

    def get_init(self, name, value, get_root=False):
        handler = self.__get_handler_from_map(
            self.__get_init_map,
            name,
            value
        )
        return handler(self, name, value)

    def render_config(self, **kwargs):
        return self._template_config.render(**kwargs)

    def render_pod(self, **kwargs):
        return self._template_pod.render(**kwargs)


def get(name):
    for subclass in AbstractLanguage.__subclasses__():
        if subclass.name == name:
            return subclass()


def argextras():
    from plugins.transmogrifiers import ArgExtra

    yield ArgExtra(
        flag='loader',
        description='Generated stub interface to grab and parse files',
        group='Code Generation Options'
    )

    for subclass in AbstractLanguage.__subclasses__():
        for argextra in subclass.argextras:
            yield ArgExtra(
                flag=subclass.name + '-' + argextra.flag,
                description=argextra.description,
                options=argextra.options,
                group='Code Generation Options'
            )


def __onload():

    from ... import code

    plugins.import_att('plugins.transmogrifiers.code.languages', __file__)

    lib.cmdline.add(
        code.CodeTransmogrifier.arggroup,
        '--code-language',
        help='target language for code generation',
        choices=[
            subclass.name
            for subclass in AbstractLanguage.__subclasses__()
        ]
    )


__onload()

