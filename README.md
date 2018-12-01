# movie-list
1-day coding project. Build a web app that allows users to list, search, add, edit and delete movies.

database setup:
Created local phpMyAdmin MySQL database using MAMP.
Tables created manually via terminal in python shell with flask environment active.

To create necessary tables locally:
1. Start Servers in MAMP.
2. Browser will open to localhost MAMP interface. Navigate to Tools>PHPMYADMIN to access server if you desire.
3. In terminal, cd to “movie-list” project directory.
4. Activate flask environment.
5. Run Python shell
6. Type command and execute: from main import Movie, UserMovie, db
7. Type command and execute: db.create_all()
8. Tables in phpMyAdmin will be empty until filled with data from csv or by user.

db_utils.py:
contains functions add_movie and import_csv. import_csv uses add_movie to add Movie objects to the specified database from the specified csv file.

1. Make sure table has been created within the database
2. Within terminal, activate flask environment
3. Start up Python shell
4. Type command and execute: from db_utils import import_csv, db
5. Type command and execute: import_csv(db, [csv file name and directory])
6. Wait for function to loop through every row of the csv file.

Running movie-list web app:
1. In terminal, cd to “movie-list” project directory.
2. Activate flask environment if not already active.
3. Type command and execute: python main.py
4. Flask will start up web app.
5. In web browser, navigate to localhost:5000 to view Home page.
6. Enjoy using my movie-list web app!

