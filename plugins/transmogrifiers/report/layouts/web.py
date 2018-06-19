import plugins
import unittest

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
    def name(cls):
        return 'web'

    @property
    def description(self):
        return 'A full-featured HTML report that can be published'

    def render(self, **kwargs):
        return super(WebLayout, self).render(
            ext_2_highlight=EXT_2_CODE_HIGHLIGHT_CLASS,
            **kwargs
        )


class __WebLayout_Test(unittest.TestCase):

    def test_render(self):

        class __WebLayout(WebLayout):

            @property
            def template(self):
                return '<body>{{content}}</body>'

        layout = __WebLayout()

        self.assertEqual(
            layout.render(content='Hello World'),
            '<body>Hello World</body>'
        )

