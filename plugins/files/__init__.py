class AbstractFilePlguin(object):

    def validate(self, content):
        try:
            self.parse(content)
        except Exception as e:
            return e
        return True

    @property
    def extension(self):
        raise NotImplementedError()

    def parse(self, content):
        raise NotImplementedError()


def validate(content, extension):
    for cls in AbstractFilePlguin.__subclasses__():
        if cls.extension == extension:
            return cls().validate(content)


def parse(content, extension):
    for cls in AbstractFilePlguin.__subclasses__():
        if cls.extension == extension:
            return cls().parse(content)

