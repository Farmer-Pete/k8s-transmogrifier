import plugins
import lib.k8s
import lib.cmdline

from lib.decorators import classproperty


class AbstractTransmogrifier(object):
    ''' The base class '''

    def __init__(self, args):
        self._args = args
        self.configs = lib.k8s.K8SConfigs(
            args.configdir,
            self.deserialize_config
        )

    @classproperty
    def name(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    @classproperty
    def description(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    @classproperty
    def arggroup(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    def transmogrify(self):
        ''' The main entry point of the class '''
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))


def execute(args):
    """ Executes all transmogrifiers specified """

    for subclass in AbstractTransmogrifier.__subclasses__():
        if hasattr(args, subclass.name):
            subclass(args).transmogrify()


def __onload():
    plugins.import_att('plugins.transmogrifiers', __file__)

    for subclass in AbstractTransmogrifier.__subclasses__():
        lib.cmdline.add(
            subclass.arggroup,
            '--' + subclass.name,
            help=subclass.description,
            action='store_true'
        )


__onload()

