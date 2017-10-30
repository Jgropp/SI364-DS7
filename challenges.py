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

##### Set up Models #####

## Task 2: Write the models for the tables
class Album(db.Model):
    __tablename__ = "albums"

class Artist(db.Model):
    __tablename__ = "artists"

class Song(db.Model):
    __tablename__ = "songs"


##### Set up Forms #####

class SongForm(FlaskForm):
    song = StringField("What is the title of your favorite song?", validators=[Required()])
    artist = StringField("What is the name of the artist who performs it?",validators=[Required()])
    genre = StringField("What is the genre of that song?", validators
        =[Required()])
    submit = SubmitField('Submit')

##### Helper functions
### For database additions / get_or_create functions

def get_or_create_artist(db_session,artist_name):
    artist = db_session.query(Artist).filter_by(name=artist_name).first()
    if artist:
        return artist
    else:
        artist = Artist(name=artist_name)
        db_session.add(artist)
        db_session.commit()
        return artist

def get_or_create_song(db_session, song_title, song_artist, song_genre):
    song = db_session.query(Song).filter_by(title=song_title).first()
    if song:
        return song
    else:
        artist = get_or_create_artist(db_session, song_artist)
        song = Song(title=song_title,genre=song_genre,artist_id=artist.id)
        db_session.add(song)
        db_session.commit()
        return song

##### Set up Controllers (view functions) #####

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

## Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    # Task 3: Update the view function such that you can display
    songs = Song.query.all()
    num_songs = len(songs)
    form = SongForm()
    if form.validate_on_submit():
        if db.session.query(Song).filter_by(title=form.song.data).first(): # If there's already a song with that title, though...
            flash("You've already saved a song with that title!")
        get_or_create_song(db.session,form.song.data, form.artist.data, form.genre.data)
        return redirect(url_for('see_all'))
    return render_template('index.html', form=form,num_songs=num_songs)


# Task 3: Update the view function.
## HINTS provided but I would recommend solving the task without looking at the hints
############################################
############################################
## 1. Query all songs and assigns the result to variable 'songs'
## 2. Collects the title, artist and genre for each song in a list variable 'all_songs'. You can use a for loop and collect each property in a tuple.
## 3. Use all_songs as a parameter in render_template
## 4. Make sure you delete 'pass' from the function code
############################################
############################################
@app.route('/all_songs')
def see_all():
    return 'You have to update this view function to view all songs!'


# Task 4: Update the view function.
## HINTS provided but I would recommend solving the task without looking at the hints
############################################
############################################
## 1. Query all artists and assign the result to variable artists
## 2. Use a for loop to collect artist name and number of songs written by the artist
## 3. To find the number of songs by each artist, filter by artist_id on the song table
## 3. Collect the artist name and number of songs
## 4. Make sure you delete 'pass' from the function code
############################################
############################################
@app.route('/all_artists')
def see_all_artists():
    return 'You have to update this function to view artists and number of songs by each artist!'

if __name__ == '__main__':
    db.create_all()
    manager.run() # NEW: run with this: python main_app.py runserver
    # Also provides more tools for debugging
