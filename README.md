# movie-list
1-day coding project. Build a web app that allows users to list, search, add, edit and delete movies.

db_utils.py:
contains functions add_movie and import_csv. import_csv uses add_movie to add Movie objects to the specified database from the specified csv file.

1. Make sure table has been created within the database
2. Within terminal, activate flask environment
3. Start up Python shell
4. Type the following command and execute: from db_utils import import_csv, db
5. Type the following command and execute: import_csv(db, [csv file name and directory])
6. Wait for function to loop through every row of the csv file.
