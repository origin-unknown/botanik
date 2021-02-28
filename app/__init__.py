#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(env=os.environ.get('FLASK_ENV', 'production')):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=b'\x9e|\t\xe8V\xdb\x975{\x1aZz\xe9G\xea\x95\xd6\xfa\xcf`\x7f\\*\n',
        SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(app.instance_path, f'{env.lower()}.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    register_blueprints(app)
    register_endpoints(app)


    # Add a sample application to start. It writes a file in the root folder.
    @app.before_request
    def before_request_func():
        db.create_all()

        from .bots.models import Bot
        target = os.path.join(app.instance_path, 'apps', 'bot1.py')
        bot = Bot(
            name="Example Bot",
            command=f"python3 {target} user"
        )
        db.session.add(bot)
        try:
            db.session.commit()
        except:
            db.session.rollback()


    return app

def register_blueprints(app):
    from importlib import import_module
    mods = (
        ('.bots', {}),
    )
    for ident,kwargs in mods:
        module = import_module(ident, __name__)
        module.create_module(app, **kwargs)

def register_endpoints(app):
    app.add_url_rule('/', 'index', index, methods=('GET',))

def index():
    from flask import redirect, url_for
    return redirect(url_for('bots.index'))
