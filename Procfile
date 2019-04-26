release: FLASK_APP=classiplex FLASK_ENV=production flask db upgrade
web: FLASK_ENV=production gunicorn 'classiplex:create_app()' --log-file -
