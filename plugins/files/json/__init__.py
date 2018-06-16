import plugins.files


class JsonFilePlugin(plugins.files.AbstractFilePlguin):

    @property
    def extension(self):
        return '.json'

    def parse(self, content):
        import json
        return json.loads(content)

