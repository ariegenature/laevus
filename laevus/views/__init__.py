"""laevus package for views and blueprints."""

from laevus.views.contribute import contribute_bp
from laevus.views.api import api_bp


blueprints = [contribute_bp, api_bp]


def home():
    """laevus homepage."""
    return 'laevus homepage'
