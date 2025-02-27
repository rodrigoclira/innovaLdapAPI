from flask import jsonify, request, abort
from flask_restful import Resource, reqparse
from sqlalchemy import exc
import logging
from inndapi.service.error_handler import *
from inndapi.service import LdapServerService


class InnovaLdapServeController(Resource):

    def __init__(self):
        self.service = LdapServerService()

    def get(self):
        try:
            entities = self.service.find_all()
            response = jsonify([entity.to_dict() for entity in entities])
            return response
        except Exception as e:
            abort(500, str(e))

    def post(self):
        entity = request.get_json(force=True)
        try:
            res = self.service.save(**entity)
            response = res.to_dict(), 201
            return response
        except MissedFields as mf:
            abort(mf.code, str(mf))
        except exc.SQLAlchemyError as e:
            abort(400, "duplicado")
        except Exception as e:
            abort(500, str(e))


class InnovaLdapServerIdController(Resource):

    def __init__(self):
        self.service = LdapServerService()

    def get(self, id):
        try:
            entity = self.service.find_by_pk(id)
            response = jsonify(entity.to_dict())
            return response
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception as e:
            abort(500, str(e))

    def put(self, id):

            parser = reqparse.RequestParser()
            parser.add_argument('service', location='args')
            parser.add_argument('uid', location='args')
            args = parser.parse_args()

            service = args.get('service')
            logging.log(logging.INFO, f'Starting service={service}')

            if service == 'sync-entity':
                uid = args.get('uid')
                try:
                    entity = self.service.sync_entity(pk=id, uid=uid)
                except ResourceDoesNotExist as rdne:
                    abort(rdne.code, str(rdne) + " on LDAP Server")
                except Exception as e:
                    abort(500, str(e))

            elif service == 'sync':
                try:
                    entity = self.service.sync_entries(ldap_pk=id)
                    response = entity, 200
                    return response
                except Exception as e:
                    abort(500, str(e))

            elif service == 'save':
                uid = args.get('uid')
                try:
                    entity = self.service.save_entry(pk=id, uid=uid, is_update=False)
                except ResourceDoesNotExist as rdne:
                    abort(rdne.code, str(rdne))
                except Exception as e:
                    abort(500, str(e))

            elif service == 'update':
                uid = args.get('uid')
                try:
                    entity = self.service.save_entry(pk=id, uid=uid, is_update=True)
                except ResourceDoesNotExist as rdne:
                    abort(rdne.code, str(rdne))
                except Exception as e:
                    abort(500, str(e))

            else:
                entity = request.get_json(force=True)
                try:
                    res = self.service.update(**entity)
                    response = res.to_dict(), 200
                    return response
                except MissedFields as mf:
                    abort(mf.code, str(mf))
                except ResourceDoesNotExist as rdne:
                    abort(rdne.code, str(rdne))
                except Exception as e:
                    abort(500, str(e))
            response = jsonify(entity.to_dict())
            return response


    def delete(self, id):
        try:
            self.service.delete(id)
            response = jsonify(dict({'status': 'ok'}))
            return response
        except ResourceDoesNotExist as rdne:
            abort(rdne.code, str(rdne))
        except Exception as e:
            abort(500, str(e))

class InnovaLdapServerUserController(Resource):

    def __init__(self):
        self.service = LdapServerService()

    def put(self, id):
        person = request.get_json(force=True)
        try:
            res = self.service.change_password(pk=id, **person)
            response = jsonify(res.to_dict())
            return response
        except InvalidPassword as ip:
            abort(ip.code, str(ip))
        except Exception as e:
            abort(500, str(e))

