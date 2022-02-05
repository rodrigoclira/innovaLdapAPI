from inndapi.ext.database import db
from inndapi.ext.serialization import ma
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

#
# class SerializePasswordHash(SerializerMixin):
#     serialize_types = (
#         (PasswordHash, lambda x: str(x)),
#     )


class LdapServer(db.Model, SerializerMixin):
    __tablename__ = 'ldap-server'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain = db.Column(db.String(140), nullable=False)
    ip = db.Column(db.String(45), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    base_dn = db.Column(db.String(140), nullable=False)
    bind_dn = db.Column(db.String(140), nullable=False)
    bind_credential = db.Column(db.String(140), nullable=False)
    ldap_server_id = db.Column(
        db.Integer,
        db.ForeignKey('innova-gateway.id'),
        nullable=False
    )

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.domain = kwargs.get('domain')
        self.ip = kwargs.get('ip')
        self.port = kwargs.get('port')
        self.base_dn = kwargs.get('base_dn')
        self.bind_dn = kwargs.get('bind_dn')
        self.bind_credential = kwargs.get('bind_credential')
        self.ldap_server_id = kwargs.get('ldap_server_id')

    def pk(self):
        return self.id

    @staticmethod
    def schema():
        return ['id', 'domain', 'port', 'base_dn', 'bind_dn', 'bind_credential']

    @validates
    def _validade_password(self, key, password):
        return getattr(type(self), key).type.validator(password)

    def __lt__(self, other):
        return (isinstance(other, self.__class__) and
                getattr(other, 'id', None) < self.id)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                getattr(other, 'id', None) == self.id)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return str(self.__dict__)


class InnovaAffiliationSchema(ma.Schema):
    class Meta:
        model = LdapServer

    @staticmethod
    def schema_list():
        return LdapServer.schema()
