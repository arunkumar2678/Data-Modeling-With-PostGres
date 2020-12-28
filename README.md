# PostGresSQL - Python Project

# Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis by creating a database schema and ETL pipeline for the analysis. 

# Project Description
In this project, we will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

# Files
* etl.py- Final ETL file.
* create_tables.py - Python file creating database and tables.
* sql_queries.py - contains all the queries.
* test.ipynb - notbook to execute connection to DB and execute create and drop table statements.
* etl_03232020.ipynb - coding for rough draft to be used for the final ETL file (etl.py)

# Data output files
Output of data pull of all the tables will be stored as xlsx files when the program is run and they are named with TableName.xlslx (songs.xlsx, artist.xlsx, users.xslx,time.xlsx, songplays.xlsx)

etl.py - has the ETL process to load all the fact and dimension tables

## Fact and Dimension Tables - Fields and data types

|Artist Table | Data type | Is Null | Description|
|-------------|-----------|----------|-----------|
|artist_id | varchar | not null | (Primary key (unique id) of the table (This is treated as a primary key since it will uniquely identify the artist)|
|artist_name | varchar | not null | Name of the artist|
|artist_location | varchar | null | Location of the artist|
|artist_latitude | float | null | Latitude of location of the artist|
|artist_longitude | float | null | Longitude of location of the artist|

|Songs Table | Data type | Is Null | Description|
|------------|-----------|---------|--------------
|song_id | varchar | not null | Primary key (unique id) of the table (This is treated as a primary |key since it will uniquely identify the song)|
|title | varchar | not null | Title of the song\
|artist_id | varchar | not null | Id of the artist(foreign key)|
|year | int | not null | Year of the song|
|duration | float | not null | Duration of the song|

| Time Table | Data type | Is Null | Description |
|------------|-----------|---------|-------------|
|starttime | date | not null | Primary key (unique id) of the table|
|hour | int | not null | Hour from timestamp|
|day | int | not null | Day from timestamp|
|week | int | not null | Week from timestamp|
|month | int | not null | Month from timestamp|
|year | int | not null | Year from timestamp|
|weekday | int | not null | Weekday from timestamp|

|Users | Data type | Is Null | Description|
|------|-----------|---------|------------|
userid | int | null | Primary key (unique id) of the table (This is treated as a primary key since it will uniquely identify the user)
firstname | varchar | null | First name of the user
lastname | varchar | null | Last name of the user
gender | varchar | null | Gender of the user
level | varchar | not null | Level of the user

|Songplays | Data type | Is Null | Description|
|----------|-----------|---------|------------|
|songplay_id | int | int | Primary key (unique id) of the table (This is treated as a primary key since it will uniquely identify the record with all the songplays information).|
|starttime | varchar | not null | Timestamp of the song|
|userid | varchar | null | ID of the user (Foreign key)|
|level | varchar | not null | The level of user app|
|song_id | varchar | null | ID of the song (Foreign key)|
|artist_id | varchar | null | ID of the artist (Foreign key)|
|sessionid | int | not null | The session id of the user on the app|
|location | varchar | null | Location of song played|
|useragent | varchar | null | User agent of the app|

## Some websites referred for help

[Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)
[Converting Dictionary to List](https://stackoverflow.com/questions/1679384/converting-dictionary-to-list)
[w3 school](www.w3schools.com)
