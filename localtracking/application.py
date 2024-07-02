# /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

def create_app(config_file):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    from database import db
    db.init_app(app)

    from views import api
    app.register_blueprint(api)

    app.debug = True
    return app

# On Elastic Beanstalk, Config.py lives there.
application = create_app('/opt/python/current/app/config.py')

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
