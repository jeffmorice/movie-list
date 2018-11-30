# build a web app for movies that allows users to
#     list
#     search
#     add
#     edit
#     delete
# movies should be stored in a database
# should contain the csv data linked to you
# should have a process for ingesting that csv into the database
# should also use Flask, allowing users to interactively edit that database
# Bonus: create a javascript frontend using a framework such as React, Vue or Angular for a more "modern" editing experience.

# import relevant modules
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
#from movie import

# define your app
app = Flask(__name__)
app.config['DEBUG'] = True
# configure it to connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://movie-list:8938PNiGrqtBi5V@localhost:8889/movie-list'
app.config['SQLALCHEMY_ECHO'] = True
# create a reference to database and its methods
db = SQLAlchemy(app)
app.secret_key = 'aroundtheworldin80days'

# define any classes - used to construct objects, usually an entry in a table.
    # in MVC, classes should be defined in the model

# class defining movie objects
class Movie(db.Model):
    # the csv contains the following fields:
    # Release Year, Title, Origin/Ethnicity, Director, Cast, Genre, Wiki Page, Plot
    id = db.Column(db.Integer, primary_key=True)
    release_year = db.Column(db.Integer)
    title = db.Column(db.String(120))
    origin_ethnicity = db.Column(db.String(120))
    director = db.Column(db.String(255))
    cast = db.Column(db.Text)
    genre = db.Column(db.String(120))
    wiki_page = db.Column(db.String(255))
    plot = db.Column(db.Text)

    def __init__(self, release_year, title, origin_ethnicity, director, cast, genre, wiki_page, plot):
        self.release_year = release_year
        self.title = title
        self. origin_ethnicity = origin_ethnicity
        self.director = director
        self.cast = cast
        self.genre = genre
        self.wiki_page = wiki_page
        self.plot = plot



# define your request handlers, one for each page
    # include any logic, say for validation or updating the database
    # return rendered templates or redirect.
@app.route('/')
def index():
    return render_template('index.html')

# run the app
if __name__ == "__main__":
    app.run()
