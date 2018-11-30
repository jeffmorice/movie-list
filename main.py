# build a web app for movies that allows users to
#     list - add existing movies to a custom list
#         - display query results to table - check
#     search - query the model to return matching items
#     add - add new Movies to the model - check
#     edit - edit existing entries - check
#     delete - delete existing entries - check
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
    is_visible = db.Column(db.Boolean)

    def __init__(self, release_year, title, origin_ethnicity, director, cast, genre, wiki_page, plot):
        self.release_year = release_year
        self.title = title
        self.origin_ethnicity = origin_ethnicity
        self.director = director
        self.cast = cast
        self.genre = genre
        self.wiki_page = wiki_page
        self.plot = plot
        self.is_visible = True

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

@app.route('/movie')
def movie():
    # for displaying individual Movies
    movie_id = request.args.get('id')
    movie = Movie.query.filter_by(id=movie_id).first()
    return render_template('individual_movie.html', movie=movie)

@app.route('/search')
def search():
    # decide how to pass and handle queries
    # search by column or search all?
    return render_template('/index')

@app.route('/add-movie', methods=['POST', 'GET'])
def add_movie():
    if request.method =='POST':
        # retrieve form data
        # release_year, title, origin_ethnicity, director, cast, genre, wiki_page, plot
        release_year = request.form["release_year"]
        title = request.form["title"]
        origin_ethnicity = request.form["origin_ethnicity"]
        director = request.form["director"]
        cast = request.form["cast"]
        genre = request.form["genre"]
        wiki_page = request.form["wiki_page"]
        plot = request.form["plot"]

        new_movie = Movie(release_year, title, origin_ethnicity, director, cast, genre, wiki_page, plot)
        # stage
        db.session.add(new_movie)
        # commit to database
        db.session.commit()

        return redirect('/movie?id=' + str(new_movie.id))

    return render_template('add-movie.html')

@app.route('/edit-movie', methods=['POST', 'GET'])
def edit_movie():
    if request.method =='POST':
        # retrieve form data
        # release_year, title, origin_ethnicity, director, cast, genre, wiki_page, plot
        movie_id = request.form["movie_id"]
        release_year = request.form["release_year"]
        title = request.form["title"]
        origin_ethnicity = request.form["origin_ethnicity"]
        director = request.form["director"]
        cast = request.form["cast"]
        genre = request.form["genre"]
        wiki_page = request.form["wiki_page"]
        plot = request.form["plot"]

        target_movie = Movie.query.filter_by(id=movie_id).first()

        # if performing validation pre-edit, now is the time.
        # stage
        target_movie.release_year = release_year
        target_movie.title = title
        target_movie.origin_ethnicity = origin_ethnicity
        target_movie.director = director
        target_movie.cast = cast
        target_movie.genre = genre
        target_movie.wiki_page = wiki_page
        target_movie.plot = plot

        # commit to database
        db.session.commit()

        return redirect('/movie?id=' + str(movie_id))

    movie_id = request.args.get('id')
    movie = Movie.query.filter_by(id=movie_id).first()
    #print(movie.title)

    return render_template('edit-movie.html', movie=movie)

@app.route('/delete-movie', methods=['POST', 'GET'])
def delete_movie():
    if request.method == 'POST':
        # retrieve form database
        movie_id = request.form["movie_id"]
        target_movie = Movie.query.filter_by(id=movie_id).first()

        # set is_visible to False
        target_movie.is_visible = False
        db.session.commit()

        return render_template('index.html')

    movie_id = request.args.get('id')
    movie = Movie.query.filter_by(id=movie_id).first()
    return render_template('delete-movie.html', movie=movie)

# run the app
if __name__ == "__main__":
    app.run()
