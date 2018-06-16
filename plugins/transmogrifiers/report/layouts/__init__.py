import jinja2

import plugins
import lib.cmdline

from lib.decorators import classproperty

DEFAULT_TEMPLATE_NAME = 'Report.html.template'


class AbstractLayout(object):

    def __init__(self):
        self._template = jinja2.Template(self.template)

    @classproperty
    def name(cls):
        raise NotImplementedError(lib.errmsg.not_implemented(cls))

    @property
    def description(self):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    @property
    def template(self):
        raise NotImplementedError(lib.errmsg.not_implemented(self.__class__))

    def render(self, **kwargs):
        return self._template.render(**kwargs)


def get(name):
    for layout in AbstractLayout.__subclasses__():
        if layout.name == name:
            return layout


def __onload():
    plugins.import_att('plugins.transmogrifiers.report.layouts', __file__)

    from ... import report

    lib.cmdline.add(
        report.ReportTransmogrifier.arggroup,
        '--report-layout',
        help='layout to use for report generation',
        choices=[
            subclass.name
            for subclass in AbstractLayout.__subclasses__()
        ]
    )


__onload()

