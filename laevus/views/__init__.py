"""laevus package for views and blueprints."""

from flask import redirect, url_for

from laevus.views.contribute import contribute_bp
from laevus.views.api import api_bp


blueprints = [contribute_bp, api_bp]


def home():
    """laevus homepage."""
    return redirect(url_for('contribute.index'))
