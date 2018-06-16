import plugins
import lib.cmdline

from lib.decorators import classproperty

NAME_TYPE_MAPPING = {
    'port': int()  # TODO: Eventually move this to onfiguration file
}


class AbstractLanguage(object):

    _deserialize_config = True

    def __init__(self, args):
        self._args = args
        self.__get_type_map = {}
        self.__get_root_map = {}
        self.__get_init_map = {}

        self.__init_map(self.__get_type_map, self._type_map)
        self.__init_map(self.__get_root_map, self._root_map)
        self.__init_map(self.__get_init_map, self._init_map)

    @classproperty
    def name(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    @property
    def extension(self):
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
        for key, value in kwargs.items:

            if not hasattr(value, '__call__'):
                _value = value

                def value(this, name, value):
                    return str(_value)

            self._get_value_map[key] = value

    def __get_handler_from_map(self, data, key):

        handler = None

        if isinstance(key, int):
            handler = data.get(int)
        elif isinstance(key, float):
            handler = data.get(int)
        elif isinstance(key, str):
            handler = data.get(str)
        elif isinstance(key, bool):
            handler = data.get(bool)
        elif isinstance(key, list):
            handler = data.get(list)
        elif isinstance(key, dict):
            handler = data.get(dict)
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
            value
        )
        return handler(self, name, value)

    def get_root_type(self, name, value):
        handler = self.__get_handler_from_map(
            self.__get_root_map,
            value
        )
        return handler(self, name, value)

    def get_init(self, name, value, get_root=False):
        handler = self.__get_handler_from_map(
            self.__get_init_map,
            value
        )
        return handler(self, name, value)


def get(name):
    for subclass in AbstractLanguage.__subclasses__:
        if subclass.name == name:
            return subclass


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

