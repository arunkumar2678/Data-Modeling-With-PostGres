import os
import glob
import psycopg2
import pandas as pd
import calendar
import datetime
import numpy as np
from datetime import datetime
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    """
    Process all the song files.
    
    Get song dimension records and load it into song dimension table.
    
    Get artist dimension records and load them into artist dimension table.

    Get song_id and artist_id from song and artist dimesion tables.

    """
    df =  pd.read_json(filepath, lines = True)

    # insert artist record
    da =  {'artist_id':df['artist_id'], 'artist_name':df['artist_name'], 'artist_location':df['artist_location'],'artist_latitude':df['artist_latitude'],'artist_longitude':df['artist_longitude']}
    selsong_artist_df = pd.DataFrame(data = da)
    #selsong_artist_df.to_csv('artist_output.csv')
    
    for index, row in selsong_artist_df.iterrows():
        try:
            cur.execute(artist_table_insert, (list(row)))
        except psycopg2.Error as e:
            print("Error: Issue inserting table")
            print (e)

            row = cur.fetchone()
            while row:
                print(row)
                row = cur.fetchone()

    
    # insert song record
    d = {'song_id':df['song_id'], 'title':df['title'], 'artist_id':df['artist_id'], 'year':df['year'], 'duration':df['duration']}
    song_df = pd.DataFrame(data = d)
   # song_df.to_csv('song_output.csv')

    for index, row in song_df.iterrows():
        try:
            cur.execute(song_table_insert, (list(row)))
        except psycopg2.Error as e:
            print("Error: Issue inserting table")
            print (e)

            row = cur.fetchone()
            while row:
                print(row)
                row = cur.fetchone()
        
        
def process_log_file(cur, filepath):
    # open log file
    """
    Process all the log files.
    
    Get time dimension records and load it into time demnsion table.
    
    Get user dimension records and load them inot user dimension table.
    
    Get data for fact table and load them into songplays fact table.
    
    """
    df =  pd.read_json(filepath, lines = True)     # filter by NextSong action
    # convert timestamp column to datetime
    df['date'] = pd.to_datetime(df['ts'].iloc[0])
    df['starttime'] = df['date'].dt.time
    df['hour'] = df['date'].dt.week
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['weekday'] = df['date'].dt.week  

    d1 = {'starttime':df['date'], 'hour':df['hour'], 'day':df['day'], 'week': df['week'], 'month': df['month'], 'year': df['year'], 'weekday': df['weekday'] }
    time_df = pd.DataFrame(data = d1)
    #time_df.to_csv('time_output.csv')
    
    # insert time data records
    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e:
            print("Error: Record not inserted")
            
#load user table
    d = {'userId':df['userId'], 'firstName':df['firstName'], 'lastName':df['lastName'], 'gender': df['gender'], 'level': df['level']}
    user_df = pd.DataFrame(data = d)
    #user_df.to_csv('user_output.csv')
    
    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, list(row))
        except psycopg2.Error as e:
            print("Error: Record not inserted")
            print(e)
            sys.exit(1)

#loadsongplays table
    #get songid and artistid from song and artist tables
    for index, row in df.iterrows():
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None
                
        songplay_data = (row['ts'], row['userId'], row['level'], song_id, artist_id, row['sessionId'], row['location'], row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
# get all files matching extension from directory

    """ Locate all the files in the data folder.

    Iterate the files and send it to processeing for fact and dimension tables.

    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='/home/workspace/data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='/home/workspace/data/log_data', func=process_log_file)

#fetch data from table time 
    try: 
        cur.execute ("Select * from time")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(list(data), columns=columns)

        writer = pd.ExcelWriter('time.xlsx')
        df.to_excel(writer, sheet_name='bar')
        writer.save()
       
    except psycopg2.Error as e: 
        print("Error: Issue selecting table")
        print (e)

    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()



#fetch data from table users 
    try: 
        cur.execute ("Select * from users")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(list(data), columns=columns)

        writer = pd.ExcelWriter('users.xlsx')
        df.to_excel(writer, sheet_name='bar')
        writer.save()

    except psycopg2.Error as e: 
        print("Error: Issue selecting table")
        print (e)

    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()

#fetch data from table songplays
    try: 
        cur.execute ("Select * from songplays")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(list(data), columns=columns)

        writer = pd.ExcelWriter('songplays.xlsx')
        df.to_excel(writer, sheet_name='bar')
        writer.save()

    except psycopg2.Error as e: 
        print("Error: Issue selecting table")
        print (e)
    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()

#fetch data from table songs
    try: 
        cur.execute ("Select * from songs")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(list(data), columns=columns)

        writer = pd.ExcelWriter('songs.xlsx')
        df.to_excel(writer, sheet_name='bar')
        writer.save()
    except psycopg2.Error as e: 
        print("Error: Issue selecting table")
        print (e)

    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()
        
#fetch data from table artists
    try: 
        cur.execute ("Select * from artists")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(list(data), columns=columns)

        writer = pd.ExcelWriter('artist.xlsx')
        df.to_excel(writer, sheet_name='bar')
        writer.save()
    except psycopg2.Error as e: 
        print("Error: Issue selecting table")
        print (e)

    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()


    conn.close()

if __name__ == "__main__":
    main()