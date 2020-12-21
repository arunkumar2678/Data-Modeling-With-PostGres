# DROP TABLES

"""
Drop the tables if they already exist.

"""
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

"""
Create the fact and dimension tables.

"""

# CREATE TABLES
user_table_create = """create table if not exists users (
    userId varchar primary key,
    firstName varchar,
    lastName varchar,
    gender varchar,
    level varchar not null
);"""

song_table_create = """create table if not exists songs (
    song_id varchar primary key,
    title varchar not null,
    artist_id varchar,
    year varchar,
    duration float
);""" 

artist_table_create = """create table if not exists artists (
    artist_id varchar primary key,
    artist_name varchar not null,
    artist_location varchar,
    artist_latitude float,
    artist_longitude float
);"""

time_table_create = """create table if not exists time (
    starttime varchar not null,
    hour int CHECK(hour > 0 and hour <=24) not null,
    day int not null,
    week varchar not null,
    month int CHECK(month >0 and month <= 12) not null,
    year int not null, 
    weekday varchar not null
);"""

songplay_table_create = """create table if not exists songplays (
    starttime varchar not null,
    userId varchar,
    level varchar not null,
    song_id varchar,
    artist_id varchar,
    sessionId varchar not null,
    location varchar,
    userAgent varchar
);"""

# INSERT RECORDS
""""
Queries to run the insert statements.

"""
user_table_insert = """Insert into users (userId, firstName, lastName, gender, level) 
                       values (%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT users_pkey DO UPDATE SET level= excluded.level;"""

song_table_insert = """Insert into songs (song_id, title, artist_id, year, duration) 
                       values (%s,%s,%s,%s,%s) ON CONFLICT (song_id) DO NOTHING;"""

artist_table_insert = """Insert into artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude)                            values (%s,%s,%s,%s,%s) ON CONFLICT (artist_id) DO NOTHING;"""

time_table_insert = """Insert into time (starttime, hour, day, week, month, year, weekday) 
                       values (%s,%s,%s,%s,%s,%s,%s);"""

songplay_table_insert = """Insert into songplays (starttime, userId, level, song_id, artist_id, sessionId, location, useragent) 
                           values (%s,%s,%s,%s,%s,%s,%s,%s);""" 



"""
Select song_id and artist_id from the songs and artist tables

"""

# FIND SONGS
song_select = """Select a.song_id, b.artist_id from songs a join artists b on a.artist_id = b.artist_id  
                 where a.title = %s and artist_name = %s  and duration = %s"""

"""
Arrays to loop the create and drop table statements.

"""

# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
