import jinjia2

import plugins
import lib.cmdline

from lib.decorators import classproperty

DEFAULT_TEMPLATE_NAME = 'Report.html.template'


class AbstractLayout(object):

    def __init__(self):
        self._template = jinjia2.Template(self.template)

    @classproperty
    def name(self):
        raise NotImplementedError()

    @property
    def description(self):
        raise NotImplementedError()

    @property
    def template(self):
        raise NotImplementedError()

    def render(self, **kwargs):
        return self._template.render(**kwargs)


def get(name):
    for layout in AbstractLayout.__subclasses__():
        if layout.name == name:
            return layout


plugins.import_att('plugins.transmogrifiers', __file__)


lib.cmdline.command_line_parser.add_argument(
    '--report-layout', 'the layout to use for report generation',
    choices=[
        subclass.name
        for subclass in AbstractLayout.__subclasses__()
    ]
)

