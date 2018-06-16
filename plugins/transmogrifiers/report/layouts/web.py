import os

from plugins.transmogrifiers.report import layouts

from lib.decorators import classproperty

TEMPLATE_PATH = os.path.join(
    __file__, layouts.DEFAULT_TEMPLATE_NAME
)

EXT_2_CODE_HIGHLIGHT_CLASS = {
    '.xml': 'xml',
    '.yaml': 'ruby',
    '.json': 'json',
    '.properties': 'perl'
}


class WebLayout(layouts.AbstractLayout):

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

