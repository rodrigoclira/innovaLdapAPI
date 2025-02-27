from flask import jsonify, request, abort
from flask_restful import Resource, reqparse
from sqlalchemy import exc
from inndapi.service.error_handler import *

from inndapi.service import InnovaLdapSyncService


class InnovaLdapSyncController(Resource):

    def __init__(self):
        self.service = InnovaLdapSyncService()

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('status', location='args')
        parser.add_argument('date', location='args')
        parser.add_argument('domain', location='args')
        args = parser.parse_args()

        status = args.get('status')
        date = args.get('date')
        domain = args.get('domain')
        entities = []
        if status:
            try:
                entities = self.service.find_all_by_status(status=status, domain=domain)
            except Exception:
                abort(500, "Erro Inesperado")

        elif date:
            try:
                entities = self.service.find_all_by_date(date=date)
            except Exception:
                abort(500, "Erro Inesperado")
        else:
            try:
                entities = self.service.find_all()
            except Exception:
                abort(500, "Erro Inesperado")

        response = jsonify(
            {"innova-ldap-sync": [entity.to_dict() for entity in entities]}
        )
        return response

    def post(self):
        entity = request.get_json(force=True)
        try:
            res = self.service.save(**entity)
            response = res.to_dict(), 201
            return response
        except MissedFields as mf:
            abort(mf.code, str(mf))
        except exc.SQLAlchemyError as e:
            print(e)
            abort(400, "duplicado")
        except Exception:
            abort(500, "Erro inesperado")


class InnovaLdapSyncIdController(Resource):

    def __init__(self):
        self.service = InnovaLdapSyncService()

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
        parser = reqparse.RequestParser()
        parser.add_argument('resolve', location='args')
        args = parser.parse_args()

        resolve = args.get('resolve')

        if resolve:
            self.service.deliberate(sync_id=id, resolve=resolve)
            response = jsonify(dict({'status': 'ok'}))
            return response

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