"""Laevus API blueprint."""

from flask import Blueprint
from flask_restful import Resource


api_bp = Blueprint('api', __name__)


class ChildGroupAPI(Resource):

    def get(self):
        return {'hello': 'world'}
