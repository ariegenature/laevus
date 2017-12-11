# This file is part of Laevus.
#
# Laevus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Laevus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Laevus. If not, see <http://www.gnu.org/licenses/>.

"""Laevus blueprint to allow contributions about wild life collisions."""

import mimetypes

from flask import Blueprint, make_response, render_template


contribute_bp = Blueprint('contribute', __name__, static_folder='templates/static',
                          template_folder='templates')


@contribute_bp.route('/contribute')
def index():
    return render_template('vue/index.html')


@contribute_bp.route('/contribute/static/<path:fpath>')
def sign_static(fpath):
    resp = make_response(render_template('static/{0}'.format(fpath)))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp
