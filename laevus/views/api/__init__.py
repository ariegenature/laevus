"""Laevus API blueprint."""

import json

from flask import Blueprint, current_app
from flask_login import current_user, login_required
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import func, text

from laevus.model import CommonName, Contribution, ScientificName, Taxon, WildLifeGroup, db


api_bp = Blueprint('api', __name__)


class StaticPath(fields.Raw):
    """A custom field for Flask-RESTful that prepends ``static/`` to the value."""

    def format(self, value):
        return 'static/{0}'.format(value)


group_fields = {
    'id': fields.String,
    'name': fields.String,
    'html_description': fields.String,
    'icon': StaticPath(attribute='icon_fname'),
}


class ChildGroupAPI(Resource):

    @marshal_with(group_fields)
    def get(self, parent_id=None):
        return (WildLifeGroup.query.
                filter_by(parent_id=parent_id).
                order_by(WildLifeGroup.order).
                all())


class TaxonAPI(Resource):

    def get(self, group_id):
        res = {'groupId': group_id, 'species': []}
        species = res['species']
        cname_query = (db.session.query(CommonName.value, Taxon.id).
                       join('taxon').
                       filter_by(group_id=group_id))
        sciname_query = (db.session.query(ScientificName.value, Taxon.id).
                         join('taxon').
                         filter_by(group_id=group_id))
        rows = cname_query.union(sciname_query).all()
        for name, taxref_id in rows:
            species.append({'taxrefId': taxref_id, 'name': name})
        return res


class ContributionAPI(Resource):

    def get(self):
        res = {
            'type': 'FeatureCollection',
            'features': []
        }
        features = res['features']
        rows = (db.session.query(Contribution.id,
                                 Contribution.date_time,
                                 WildLifeGroup.name,
                                 Contribution.count_accuracy_id,
                                 Contribution.count,
                                 Contribution.is_alive,
                                 func.ST_AsGeoJSON(Contribution.geometry).label('geojson')).
                join('group').
                order_by(Contribution.date_time.desc()).
                all())
        for row in rows:
            features.append({
                'type': 'Feature',
                'id': row.id,
                'properties': {
                    'date_time': row.date_time.strftime('%Y-%m-%d'),
                    'group': row.name,
                    'accuracy': row.count_accuracy_id,
                    'count': row.count,
                    'is_alive': row.is_alive,
                },
                'geometry': json.loads(row.geojson)
            })
        return res


class FullContributionAPI(Resource):

    @login_required
    def get(self):
        res = []
        query = text('select * from full_report')
        rows = db.engine.execute(query)
        for row in rows:
            res.append({
                'id': row.id,
                'dateTime': row.date_time.strftime('%Y-%m-%d %H:%M'),
                'groupName': row.group_name,
                'taxrefId': row.taxref_id,
                'scientificName': row.scientific_name,
                'commonNames': ('<br>'.join(row.common_names.split(';')) if row.common_names
                                else None),
                'countAccuracy': row.count_accuracy,
                'count': row.count,
                'isAlive': row.is_alive,
                'comments': row.comments,
                'firstName': row.first_name,
                'surname': row.surname,
                'email': row.email,
            })
        return res


class CurrentUserAPI(Resource):

    def get(self):
        if current_user.is_authenticated:
            return {'username': current_user.username, 'name': current_user.name}
        else:
            return None


class MapLayerAPI(Resource):

    def get(self):
        res = {'layers': []}
        i = 1
        layer_name = current_app.config.get('LAYER{0}_NAME'.format(i))
        while layer_name is not None:
            res['layers'].append({
                'order': i,
                'name': layer_name,
                'url': current_app.config['LAYER{0}_URL'.format(i)],
                'attribution': current_app.config['LAYER{0}_ATTRIB'.format(i)],
            })
            i += 1
            layer_name = current_app.config.get('LAYER{0}_NAME'.format(i))
        return res
