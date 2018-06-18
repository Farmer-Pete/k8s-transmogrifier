import plugins

from . import AbstractLayout, DEFAULT_TEMPLATE_NAME

from lib.decorators import classproperty

TEMPLATE_PATH = plugins.resource_file(
    __file__,
    DEFAULT_TEMPLATE_NAME
)

EXT_2_CODE_HIGHLIGHT_CLASS = {
    '.xml': 'xml',
    '.yaml': 'ruby',
    '.json': 'json',
    '.properties': 'perl'
}


class WebLayout(AbstractLayout):

    @property
    def template(self):
        with open(TEMPLATE_PATH) as tpl:
            return tpl.read()

    @classproperty
    def name(self):
        return 'web'

    @property
    def description(self):
        return 'A full-featured HTML report that can be published'

    def render(self, **kwargs):
        return super(WebLayout, self).render(
            ext_2_highlight=EXT_2_CODE_HIGHLIGHT_CLASS,
            **kwargs
        )

