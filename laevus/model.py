from geoalchemy2 import types as geo_types

from laevus.extensions import db


class Contribution(db.Model):
    __tablename__ = 'contribution'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_time = db.Column(db.DateTime, nullable=False)
    group_id = db.Column(db.Text, nullable=False)
    specie_id = db.Column(db.Integer, nullable=False)
    count_accuracy_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    is_alive = db.Column(db.Boolean, nullable=False)
    comments = db.Column(db.Text)
    first_name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    geometry = db.Column(geo_types.Geometry(geometry_type='POINT', srid=2154),
                         nullable=False)
