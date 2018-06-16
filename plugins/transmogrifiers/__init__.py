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
    def name(self):
        raise NotImplementedError()

    @classproperty
    def description(self):
        raise NotImplementedError()

    def transmogrify(self):
        ''' The main entry point of the class '''
        raise NotImplementedError()


def execute(args):
    """ Executes all transmogrifiers specified """

    for subclass in AbstractTransmogrifier.__subclasses__():
        if hasattr(args, subclass.name):
            subclass(args).transmogrify()


plugins.import_att('plugins.transmogrifiers', __file__)

for subclass in AbstractTransmogrifier.__subclasses__():
    lib.cmdline.command_line_parser.add_argument(
        '--' + subclass.name, subclass.description
    )

