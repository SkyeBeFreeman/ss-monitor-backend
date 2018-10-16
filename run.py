#!/usr/bin/env python
# encoding: utf-8

from flask_failsafe import failsafe


@failsafe  #出bug自动重启
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time
    from app import app
    return app


if __name__ == "__main__":
    app=create_app()
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])
