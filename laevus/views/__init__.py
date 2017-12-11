"""laevus package for views and blueprints."""

from laevus.views.contribute import contribute_bp


blueprints = [contribute_bp]


def home():
    """laevus homepage."""
    return 'laevus homepage'
