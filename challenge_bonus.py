# SI364 DS7
# An application about recording favorite songs & info

import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand # needs: pip/pip3 install flask-migrate

# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configurations
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'

## Task 1: Create a database in postgresql in the code line below, and fill in your app's database URI.
app.config["SQLALCHEMY_DATABASE_URI"] = ""
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
manager = Manager(app)
db = SQLAlchemy(app) # For database use
migrate = Migrate(app, db) # This is used for database use/updating. Bear with me, we will cover this in greater detail in lecture.
manager.add_command('db', MigrateCommand) # Add migrate command to manager

#########
######### Everything above this line is important/useful setup, not problem-solving.
#########

### Copy paste the necessary code from challenges.py
