from appengine_flask_security_auth.settings import *

TESTING = True
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql:///appengine_flask_security_auth_test'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
