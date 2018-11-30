import csv
from main import db, Movie

def add_movie(db, release_year, title, origin_ethnicity, director, cast, genre, wiki_page, plot):
    movie = Movie(release_year, title, origin_ethnicity, director, cast, genre, wiki_page, plot)
    db.session.add(movie)
    db.session.commit()

def import_csv(db, csv_file_directory):
    with open(csv_file_directory) as csv_data:
        csv_reader = csv.reader(csv_data, delimiter=',', quotechar='"')

        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                # do nothing for now
                line_count += 1
            else:
                add_movie(db, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                line_count += 1
