from flask_security.core import UserMixin, RoleMixin
from flask_security.datastore import UserDatastore

from google.cloud import datastore

from appengine_flask_security_auth import ds_client

class UserModelMeta(type):
    def __new__(cls, name, bases, attrs):
        klass = super().__new__(cls, name, bases, attrs)
        # Make flask-security happy.
        # It requires field name on the class, not on the object.
        for key in attrs.get('PROPERTIES'):
            setattr(klass, key, None)
        return klass


class UserModelCommonMixin:
    def __init__(self, **kwargs):
        for key in self.PROPERTIES:
            setattr(self, key, kwargs.get(key))

    @classmethod
    def from_query_result(cls, result):
        kwargs = {key: value for key, value in result.items()}
        kwargs['id'] = result.id
        return cls(**kwargs)

    def save(self):
        if hasattr(self, 'id') and self.id != None:
            key = ds_client.key(self.KIND, self.id)
        else:
            key = ds_client.key(self.KIND)
        entity = datastore.Entity(key=key)
        update_properties = {
            key: value for (key, value) in self.__dict__.items()
            if key in self.PROPERTIES
        }
        entity.update(update_properties)
        ds_client.put(entity)

    def delete(self):
        key = ds_client.key(self.KIND, self.id)
        ds_client.delete(key)


class Role(UserModelCommonMixin, RoleMixin, metaclass=UserModelMeta):
    KIND = 'Role'
    PROPERTIES = set(('id', 'name', 'description'))


class User(UserModelCommonMixin, UserMixin, metaclass=UserModelMeta):
    KIND = 'User'
    PROPERTIES = set((
        'id', 'email', 'password', 'active', 'confirmed_at', 'last_login_at',
        'current_login_at', 'last_login_ip', 'current_login_ip', 'login_count',
        'roles'
    ))


class AppEngineUserDatastore(UserDatastore):
    """User datastore for google appengine
    :param user_model: A user model class definition
    :param role_model: A role model class definition
    """

    def get_user(self, id_or_email):
        """Returns a user matching the specified ID or email address."""
        result = None
        try:
            key = ds_client.key('User', int(id_or_email))
            result = ds_client.get(key)
            if result:
                return User.from_query_result(result)
            else:
                return None
        except (TypeError, ValueError):
            return self.find_user(**{'email': id_or_email})

    def find_user(self, **kwargs):
        if kwargs.get('id'):
            return self.get_user(kwargs['id'])

        query = ds_client.query(kind=User.KIND)
        for key, value in kwargs.items():
            query.add_filter(key, '=', value)
        result = list(query.fetch(1))
        if result:
            return User.from_query_result(result[0])
        else:
            return None

    def find_role(self, **kwargs):
        """Returns a role matching the provided name."""
        query = ds_client.query(kind=Role.KIND)
        for key, value in kwargs:
            query.add_filter(key, '=', value)
        result = list(query.fetch(1))
        if result:
            return Role.from_query_result(result[0])
        else:
            return None

    def put(self, model):
        model.save()
        return model

    def delete(self, model):
        model.delete()

    def commit(self):
        pass
