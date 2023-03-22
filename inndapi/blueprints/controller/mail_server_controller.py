from flask import jsonify, request, abort
from flask_restful import Resource

from inndapi.service.error_handler import *
from inndapi.service import MailService


class MailServerController(Resource):

    def __init__(self):
        self.service = MailService()

    def get(self):
        try:
            entities = self.service.find_all()
            response = jsonify([entity.to_dict() for entity in entities])
            return response
        except Exception:
            abort(500, "Erro Inesperado")

    def post(self):
        entity = request.get_json(force=True)
        try:
            res = self.service.save(**entity)
            response = res.to_dict(), 201
            return response
        except MissedFields as mf:
            abort(mf.code, str(mf))
        except Exception:
            abort(500, "Erro inesperado")


class MailServerIdController(Resource):

    def __init__(self):
        self.service = MailService()

    def get(self, id):
        try:
            entity = self.service.find_by_pk(id)
            response = entity.to_dict()
            return response
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception:
            abort(500, "Erro inesperado")

    def put(self, id):
        entity = request.get_json(force=True)
        try:
            res = self.service.update(**entity)
            response = res.to_dict(), 200
            return response
        except MissedFields as mf:
            abort(mf.code, str(mf))
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception:
            abort(500, "Erro inesperado")

    def delete(self, id):
        try:
            self.service.delete(id)
            response = jsonify(dict({'status': 'ok'}))
            return response
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception:
            abort(500, "Erro inesperado")
