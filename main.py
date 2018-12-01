# build a web app for movies that allows users to
#     list - add existing movies to a custom list
#         - display query results to table - check
#     search - query the model to return matching items - check
#     add - add new Movies to the model - check
#     edit - edit existing entries - check
#     delete - delete existing entries - check
# movies should be stored in a database - check
# should contain the csv data linked to you - check
# should have a process for ingesting that csv into the database - check
# should also use Flask, allowing users to interactively edit that database - check
# Bonus: create a javascript frontend using a framework such as React, Vue or Angular for a more "modern" editing experience.

# import relevant modules
from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import datetime

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

class UserMovie(db.Model):
    # create a model for storing user-created list of movies
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, unique=True)
    date_added = db.Column(db.DateTime)
    is_visible = db.Column(db.Boolean)

    def __init__(self, movie_id, date_added):
        self.movie_id = movie_id
        self.date_added = date_added
        self.is_visible = True

# define your request handlers, one for each page
    # include any logic, say for validation or updating the database
    # return rendered templates or redirect.
@app.route('/')
def index():
    # pass db info. Should support pagination as there are 34,000 entries
    page = request.args.get('page', 1, type=int)
    records = Movie.query.filter_by(is_visible=1).order_by(desc(Movie.release_year)).paginate(page, 20, False)
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

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        # decide how to pass and handle queries
        # search by column or search all?
        # start with column
        search_term = request.form['search_term']
        column = request.form['column']

        page = request.args.get('page', 1, type=int)

        # Could not get pagination to work with search results. Commented out pagination attibutes.

        if column == 'release_year':
            search_results = Movie.query.filter(Movie.release_year.contains(int(search_term))).all() #.paginate(page, 20, False)
        elif column == 'title':
            search_results = Movie.query.filter(Movie.title.contains(search_term)).all() #.paginate(page, 20, False)
        elif column == 'origin_ethnicity':
            search_results = Movie.query.filter(Movie.origin_ethnicity.contains(search_term)).all() #.paginate(page, 20, False)
        elif column == 'director':
            search_results = Movie.query.filter(Movie.director.contains(search_term)).all() #.paginate(page, 20, False)
        elif column == 'cast':
            search_results = Movie.query.filter(Movie.cast.contains(search_term)).all() #.paginate(page, 20, False)
        elif column == 'genre':
            search_results = Movie.query.filter(Movie.genre.contains(search_term)).all() #.paginate(page, 20, False)

        # next_url = url_for('search', page=search_results.next_num) \
        #     if search_results.has_next else None
        # prev_url = url_for('search', page=search_results.prev_num) \
        #     if search_results.has_prev else None

        # currently returns un-paginated results
        return render_template('search.html', search_results=search_results) #.items, next_url=next_url, prev_url=prev_url)

    # use session data to enable search results to persist through pagination
    # if request.method != 'POST' and 'search_term' in session:
    #     next_url = url_for('search', page=search_results.next_num) \
    #         if search_results.has_next else None
    #     prev_url = url_for('search', page=search_results.prev_num) \
    #         if search_results.has_prev else None

        return render_template('search.html', search_results=search_results.items, next_url=next_url, prev_url=prev_url)

    return render_template('search.html')

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
        target_movie.is_visible = 0
        db.session.commit()

        return redirect('/')

    movie_id = request.args.get('id')
    movie = Movie.query.filter_by(id=movie_id).first()
    return render_template('delete-movie.html', movie=movie)

@app.route('/add-to-list')
def add_to_list():
    movie_id = request.args.get('id')
    current_date = datetime.datetime.today()

    new_user_movie = UserMovie(movie_id, current_date)

    db.session.add(new_user_movie)
    db.session.commit()

    return redirect('/user-movies')

@app.route('/user-movies')
def user_movies():
    user_movies = UserMovie.query.all()
    movies = []

    for movie in user_movies:
        movies.append(Movie.query.filter_by(id=movie.movie_id).first())

    return render_template('user-movies.html', movies=movies)

# run the app
if __name__ == "__main__":
    app.run()
