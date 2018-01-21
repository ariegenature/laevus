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

from flask import Blueprint, jsonify, make_response, render_template
from flask_wtf import FlaskForm
from six import text_type
from wtforms import (BooleanField, DateTimeField, IntegerField, StringField,
                     TextField)
from wtforms.validators import DataRequired, Email, NumberRange

from laevus.model import Contribution, User, db


contribute_bp = Blueprint('contribute', __name__, static_folder='templates/static',
                          template_folder='templates')


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


@contribute_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'OK', 200
    return render_template('vue/index.html')


@contribute_bp.route('/contribute/static/<path:fpath>')
def sign_static(fpath):
    resp = make_response(render_template('static/{0}'.format(fpath)))
    resp.headers['Content-Type'], resp.headers['Content-Encoding'] = mimetypes.guess_type(fpath)
    return resp
