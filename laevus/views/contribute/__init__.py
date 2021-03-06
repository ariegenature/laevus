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

import glob
import mimetypes
import os
import tempfile
import zipfile

from fiona.crs import from_epsg
from flask import Blueprint, abort, jsonify, make_response, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from shapely.geometry import mapping
from shapely.wkt import loads as geom_from_wkt
from six import text_type
from wtforms import (BooleanField, DateTimeField, IntegerField, StringField,
                     TextField)
from wtforms.validators import DataRequired, Email, NumberRange
import fiona

from laevus.extensions import login_manager
from laevus.model import Contribution, User, db


contribute_bp = Blueprint('contribute', __name__, static_folder='templates/static',
                          template_folder='templates')


@login_manager.user_loader
def load_user(username):
    try:
        return User.query.get(username)
    except Exception:
        return None


class ContributeForm(FlaskForm):
    """Flask contribution form."""

    date_time = DateTimeField('Date and time', format='%Y-%m-%dT%H:%M:%S.%fZ',
                              validators=[DataRequired()])
    group_id = StringField('Group', validators=[DataRequired()])
    specie_id = IntegerField('Species')
    count_accuracy_id = StringField('Accuracy', validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired(), NumberRange(min=1)])
    is_alive = BooleanField('Is Alive ?')
    comments = TextField('Comments')
    first_name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    geometry = StringField('Point', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Laevus login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

    def validate(self):
        validity = super().validate()
        if not validity:
            return False
        user = User.query.get(self.username.data)
        if not user or not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True


@contribute_bp.route('/contribute', methods=['GET', 'POST'])
def index():
    form = ContributeForm()
    if form.validate_on_submit():
        contribution = Contribution()
        form.populate_obj(contribution)
        db.session.add(contribution)
        db.session.commit()
        return jsonify({'id': contribution.id}), 201
    errors = ['{field}: {msg}'.format(
        field=field.label.text,
        msg=', '.join(map(lambda err: text_type(err), field.errors))
    ) for field in form if field.errors]
    if errors:
        msg = u'After checking, the following problem(s) were found: {0}.'.format(
            u'; '.join('({i}) {msg}'.format(i=i, msg=msg) for i, msg in enumerate(errors, 1))
        )
        return jsonify({'message': msg}), 409
    return render_template('vue/index.html')


@contribute_bp.route('/full-contribution')
@login_required
def full_contribution():
    return render_template('vue/index.html')


@contribute_bp.route('/full-contribution/download/<file_format>')
@login_required
def download_contributions(file_format='shp'):
    if file_format != 'shp':
        abort(404)
    txt_accuracy_map = {'=': '=', '&cong;': '~', '&ge;': '>'}
    with tempfile.TemporaryDirectory() as tmpdirname:
        bname = 'laevus'
        shpname = os.path.join(tmpdirname, '{0}.shp'.format(bname))
        zipname = os.path.join(tmpdirname, '{0}.zip'.format(bname))
        schema = {'geometry': 'Point',
                  'properties': {
                      'id': 'int',
                      'date': 'date',
                      'time': 'str',
                      'group_name': 'str',
                      'taxref_id': 'int',
                      'sci_name': 'str',
                      'cnames': 'str',
                      'accuracy': 'str',
                      'count': 'int',
                      'is_alive': 'str:1',
                      'comments': 'str',
                      'first_name': 'str',
                      'surname': 'str',
                      'email': 'str',
                  }}
        rows = db.engine.execute('select * from full_report')
        with fiona.open(shpname, 'w', driver='ESRI Shapefile', encoding='utf-8', schema=schema,
                        crs=from_epsg(2154)) as shp:
            for row in rows:
                shp.write({'geometry': mapping(geom_from_wkt(row.geometry)),
                           'properties': {
                               'id': row.id,
                               'date': row.date_time.strftime('%Y-%m-%d'),
                               'time': row.date_time.strftime('%H:%M'),
                               'group_name': row.group_name,
                               'taxref_id': row.taxref_id,
                               'sci_name': row.scientific_name,
                               'cnames': row.common_names,
                               'accuracy': txt_accuracy_map[row.count_accuracy],
                               'count': row.count,
                               'is_alive': row.is_alive,
                               'comments': row.comments,
                               'first_name': row.first_name,
                               'surname': row.surname,
                               'email': row.email,
                           }})
        with zipfile.ZipFile(zipname, 'w') as shpzip:
            for fname in glob.glob('{0}.*'.format(os.path.join(tmpdirname, bname))):
                if not fname.endswith('.zip'):
                    shpzip.write(fname, arcname=os.path.basename(fname))
        with open(zipname, 'rb') as shpzip:
            resp = make_response(shpzip.read())
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(zipname)
    resp.headers['Content-Disposition'] = ('attachment; '
                                           'filename={0}'.format(os.path.basename(zipname)))
    return resp


@contribute_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    if form.validate_on_submit():
        user = User.query.get(username)
        login_user(user)
        return jsonify({'id': username}), 200
    if form.username.errors:
        msg = u'{0}. '.format('Login failed')
        msg += u', '.join(map(lambda err: text_type(err), form.username.errors))
        return jsonify({'message': msg}), 401
    return render_template('vue/index.html')


@contribute_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('contribute.index'))


@contribute_bp.route('/contribute/static/<path:fpath>')
def sign_static(fpath):
    resp = make_response(render_template('static/{0}'.format(fpath)))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp
