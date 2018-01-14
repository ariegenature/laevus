"""Laevus API blueprint."""

from flask import Blueprint
from flask_restful import Resource, fields, marshal_with

from laevus.model import WildLifeGroup


api_bp = Blueprint('api', __name__)


class StaticPath(fields.Raw):
    """A custom field for Flask-RESTful that prepends ``static/`` to the value."""

    def format(self, value):
        return 'static/{0}'.format(value)


group_fields = {
    'id': fields.String,
    'name': fields.String,
    'icon': StaticPath(attribute='icon_fname'),
}


class ChildGroupAPI(Resource):

    @marshal_with(group_fields)
    def get(self, parent_id=None):
        return (WildLifeGroup.query.
                filter_by(parent_id=parent_id).
                order_by(WildLifeGroup.order).
                all())
