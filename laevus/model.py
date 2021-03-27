from crypt import METHOD_SHA512, crypt, mksalt
from hmac import compare_digest as compare_hash
import re

from flask_login import AnonymousUserMixin
from geoalchemy2 import types as geo_types
from sqlalchemy import CheckConstraint

from laevus.extensions import db


CRYPT_REGEXP = re.compile(r'(\$\d\$[^$]+\$)')


class Contribution(db.Model):
    """An animal's observation around a road."""

    __tablename__ = 'contribution'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_time = db.Column(db.DateTime, nullable=False)
    group_id = db.Column(db.Text, db.ForeignKey('group.id'), nullable=False)
    specie_id = db.Column(db.Integer, db.ForeignKey('taxon.id'))
    count_accuracy_id = db.Column(db.Enum('=', '&cong;', '&ge;', name='count_accuracy_type'),
                                  nullable=False)
    count = db.Column(db.Integer, nullable=False)
    is_alive = db.Column(db.Boolean, nullable=False)
    comments = db.Column(db.Text)
    first_name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    geometry = db.Column(geo_types.Geometry(geometry_type='POINT', srid=4326),
                         nullable=False)
    group = db.relationship('WildLifeGroup', backref='observed_in', foreign_keys=[group_id])
    specie = db.relationship('Taxon', backref='observed_in', foreign_keys=[specie_id])


class WildLifeGroup(db.Model):
    """A group of species to help user identify observed animal."""

    __tablename__ = 'group'
    __table_args__ = (CheckConstraint("id ~* '^[a-z]+(?:-[a-z0-9]+)*$'",
                                      name='proper_group_id'),)

    id = db.Column(db.Text, primary_key=True)
    order = db.Column(db.Integer, CheckConstraint('"order" >= 0'))
    name = db.Column(db.Text, nullable=False, index=True, unique=True)
    html_description = db.Column(db.Text, nullable=False, default='')
    parent_id = db.Column(db.Text, db.ForeignKey('group.id'))
    icon_fname = db.Column(db.Text)
    parent = db.relationship('WildLifeGroup', backref='children', foreign_keys=[parent_id],
                             remote_side='WildLifeGroup.id')


class Taxon(db.Model):
    """A group of one or more populations of a living organism or organisms,
    seen to form a unit (Wikipedia)."""

    __tablename__ = 'taxon'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Text, db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('WildLifeGroup', backref='taxons', foreign_keys=[group_id])


class ScientificName(db.Model):
    """A scientific name for a taxon."""

    __tablename__ = 'scientific_name'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Text, nullable=False, index=True)
    is_preferred = db.Column(db.Boolean, nullable=False, default=False)
    taxon_id = db.Column(db.Integer, db.ForeignKey('taxon.id'), nullable=False)
    taxon = db.relationship('Taxon', backref='scientific_names', foreign_keys=[taxon_id])


class CommonName(db.Model):
    """A common name for a taxon in French."""

    __tablename__ = 'common_name'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Text, nullable=False, index=True)
    taxon_id = db.Column(db.Integer, db.ForeignKey('taxon.id'), nullable=False)
    taxon = db.relationship('Taxon', backref='common_names', foreign_keys=[taxon_id])


class User(db.Model):
    """A user of the application, with an email address."""

    __tablename = 'user'

    username = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, name, email=None):
        self.username = username
        self.name = name
        self.email = email

    def set_password(self, value):
        """Encrypt and set the person's password."""
        if not value:
            raise ValueError('Password cannot be empty')
        self.password = crypt(value, mksalt(METHOD_SHA512))

    def check_password(self, value):
        """Return ``True`` if the given value match the person's password."""
        salt = CRYPT_REGEXP.match(self.password).group(1)
        return compare_hash(self.password, crypt(value, salt))

    @property
    def is_active(self):
        return self.is_authenticated

    @property
    def is_authenticated(self):
        """Return ``True`` if this person is authenticated."""
        return not isinstance(self, AnonymousUserMixin)

    @property
    def is_anonymous(self):
        """Return ``True`` if this person is anonymous."""
        return isinstance(self, AnonymousUserMixin)

    def get_id(self):
        """Return the username of the person."""
        return self.username
