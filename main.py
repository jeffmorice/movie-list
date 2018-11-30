# build a web app for movies that allows users to
#     list - add existing movies to a custom list
#     search - query the model to return matching items
#     add - add new Movies to the model
#     edit - edit existing entries
#     delete - delete existing entries
# movies should be stored in a database - check
# should contain the csv data linked to you - check
# should have a process for ingesting that csv into the database - check
# should also use Flask, allowing users to interactively edit that database - check
# Bonus: create a javascript frontend using a framework such as React, Vue or Angular for a more "modern" editing experience.

# import relevant modules
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

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
    # pass db info. Should support pagination as there are 34,000 entries
    page = request.args.get('page', 1, type=int)
    records = Movie.query.order_by(desc(Movie.release_year)).paginate(page, 20, False)
    next_url = url_for('index', page=records.next_num) \
        if records.has_next else None
    prev_url = url_for('index', page=records.prev_num) \
        if records.has_prev else None


    return render_template('index.html', records=records.items, next_url=next_url, prev_url=prev_url)

# run the app
if __name__ == "__main__":
    app.run()
