import plugins
import lib.errmsg

from lib.decorators import classproperty


class AbstractFilePlguin(object):

    def validate(self, content):
        try:
            self.parse(content)
        except Exception as e:
            return e
        return True

    @classproperty
    def extension(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    def parse(self, content):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))


def validate(content, extension):
    for cls in AbstractFilePlguin.__subclasses__():
        if cls.extension == extension:
            return cls().validate(content)


def parse(content, extension):
    for cls in AbstractFilePlguin.__subclasses__():
        if cls.extension == extension:
            return cls().parse(content)
    raise ValueError(
        'No handler available for file type: %s' % (extension,)
    )


plugins.import_att('plugins.files', __file__)

