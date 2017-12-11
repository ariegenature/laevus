"""Tests about homepage."""

import unittest

from mock import patch

from . import TEST_CONFIG
import laevus  # noqa: used in patch('flask.templating.render_template')


class TestContributeAnonymous(unittest.TestCase):
    """Check homepage as anonymous user."""

    def setUp(self):
        super(TestContributeAnonymous, self).setUp()
        self.app = laevus.create_app(laevus.read_config(TEST_CONFIG))
        self.client = self.app.test_client()

    def test_contribute_page(self):
        with patch('laevus.views.contribute.render_template', return_value=None) as fake_func:
            str(self.client.get('/contribute').data)
        fake_func.assert_called_once_with('vue/index.html')

    def test_contribute_asset(self):
        with patch('laevus.views.contribute.render_template', return_value=None) as fake_func:
            str(self.client.get('/contribute/static/vue/foo.js').data)
        fake_func.assert_called_once_with('static/vue/foo.js')
