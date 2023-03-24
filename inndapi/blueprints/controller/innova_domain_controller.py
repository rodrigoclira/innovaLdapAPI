from flask import jsonify, request, abort
from flask_restful import Resource
from inndapi.service.error_handler import *

from inndapi.service import InnovaDomainService


class InnovaGatewayController(Resource):

    def __init__(self):
        self.service = InnovaDomainService()

    def get(self):
        try:
            gateways = self.service.find_all()
            response = jsonify([gateway.to_dict() for gateway in gateways])
            return response
        except Exception as e:
            abort(500, str(e))

    def post(self):
        gateway = request.get_json(force=True)
        try:
            res = self.service.save(**gateway)
            response = res.to_dict(), 201
            return response
        except MissedFields as mf:
            abort(mf.code, str(mf))
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception as e:
            abort(500, str(e))


class InnovaGatewayIdController(Resource):

    def __init__(self):
        self.service = InnovaDomainService()

    def get(self, id):
        try:
            gateway = self.service.find_by_pk(id)
            response = jsonify(gateway.to_dict())
            return response
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception as e:
            abort(500, str(e))

    def put(self, id):
        gateway = request.get_json(force=True)
        try:
            res = self.service.update(**gateway)
            response = res.to_dict(), 200
            return response
        except MissedFields as mf:
            abort(mf.code, str(mf))
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception as e:
            abort(500, str(e))

    def delete(self, id):
        try:
            self.service.delete(id)
            response = jsonify(dict({'status': 'ok'}))
            return response
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception as e:
            abort(500, str(e))