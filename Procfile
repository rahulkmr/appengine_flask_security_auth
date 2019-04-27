release: FLASK_APP=appengine_flask_security_auth FLASK_ENV=production flask db upgrade
web: FLASK_ENV=production gunicorn 'appengine_flask_security_auth:create_app()' --log-file -
