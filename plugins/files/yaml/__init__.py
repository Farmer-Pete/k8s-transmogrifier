import plugins.files


try:
    from io import StringIO
except ImportError:
    # Fallback for python 2
    from SringIO import StringIO


class YamlFilePlugin(plugins.files.AbstractFilePlguin):

    @property
    def extension(self):
        return '.yaml'

    def parse(self, content):
        import yaml
        return yaml.safe_load(StringIO(content))

