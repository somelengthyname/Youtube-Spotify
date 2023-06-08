import flask
from flask import Flask, jsonify, request
import sqlite3
from sqlite3 import Error
import pandas as pd
import json

def create_connection (path):
    connection =None 
    try:
        connection = sqlite3.connect(
            path
        )
        print("Database connected")
    except Error as err:
        print("Error:", err)
    return connection





app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

Youtube_list = []
Spotify_list = []



def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print("Error:", err)

@app.route('/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

#selects songs from youtube
@app.route('/Youtube_Spotify/Youtube/SongSearch', methods=['GET'])
def Youtube_Search():
    Youtube_list.clear()
    song = None
    if 'song' in request.args:
        song = request.args['song']
    connection=create_connection("Database.db")
    sql = "SELECT Title, Views, Likes, Channel, Url_youtube FROM Spotify_Youtube WHERE Title LIKE '%" + song + "%'"
    titles = execute_read_query(connection, sql)
    for t in titles:

        Youtube_list.append(
            {
                'Title': t[0],
                'Views': t[1],
                'Likes': t[2],
                'Channel': t[3],
                'Url': t[4],
                
            }
        )
    connection.close()
    return jsonify(Youtube_list)

#select songs from youtube made by an artist
@app.route('/Youtube_Spotify/Youtube/ArtistSearch', methods=['GET'])
def Youtube_Artist_Search():
    Youtube_list.clear()
    connection = create_connection("Database.db")
    artist = None
    if 'artist' in request.args:
        artist = request.args['artist']
    else:
        return "Error: Please specify an artist you wish to search"
    sql = "SELECT Title, Views, Likes, Channel, Url_youtube FROM Spotify_Youtube WHERE Artist LIKE '%" + artist + "'"
    list = execute_read_query(connection, sql)
    connection.close()
    for track in list:
        Youtube_list.append(
            {
                'Title': track[0],
                'Views': track[1],
                'Likes': track[2],
                'Channel': track[3],
                'Url': track[4]
            }
        )
    
    return jsonify(Youtube_list)

#select songs from youtube with the most views
@app.route('/Youtube_Spotify/Youtube/MostViewed', methods=['GET'])
def Youtube_Most_Viewed():
    Youtube_list.clear()
    connection=create_connection("Database.db")

    limit = None
    if 'limit' in request.args:
        limit = request.args['limit']
    else:
        return "Incorrect syntax, please provide a limit"
    sql = "SELECT Title, Views, Likes, Channel, Url_Youtube FROM Spotify_Youtube GROUP BY Title, Views, Likes, Channel, Url_Youtube ORDER BY Views DESC LIMIT " + limit 
    list = execute_read_query(connection, sql)
    
    for track in list:
        Youtube_list.append(
            {
                'Title': track[0],
                'Views': track[1],
                'Likes': track[2],
                'Channel': track[3],
                'Url': track[4]
            }
        )
    connection.close()
    return jsonify(Youtube_list)

#select songs from spotify
@app.route('/Youtube_Spotify/Spotify/SongSearch', methods=['GET'])
def Spotify_Song_Search():
    Spotify_list.clear()
    connection = create_connection("Database.db")
    song = None
    if 'song' in request.args:
        song = request.args['song']
    else:
        return "Incorrect syntax, please specify a song"
    sql = "SELECT Track, Artist, Stream, Album, Uri FROM Spotify_Youtube WHERE Track LIKE '%" + song + "%'"
    list = execute_read_query(connection, sql)
    for track in list:
        Spotify_list.append(
            {
                'Track': track[0],
                'Artist': track[1],
                'Stream': track[2],
                'Album': track[3],
                'Url': track[4]
            }
        )
    connection.close()
    return jsonify(Spotify_list)

#select songs from spotify from an artist
@app.route('/YoutubeSpotify/Spotify/ArtistSearch', methods=['GET'])
def Spotify_Artist_Search():
    Spotify_list.clear()
    connection = create_connection("Database.db")
    artist = None
    if 'artist' in request.args:
        artist = request.args['artist']
    else:
        return "Incorrect syntax, please specify an artist"
    sql = "SELECT Track, Artist, Stream, Album, Uri FROM Spotify_Youtube WHERE Artist LIKE '%" + artist + "'"
    list = execute_read_query(connection, sql)
    for track in list:
        Spotify_list.append(
            {
                'Track': track[0],
                'Artist': track[1],
                'Stream': track[2],
                'Album': track[3],
                'Url': track[4]
            }
        )
    connection.close()
    return jsonify(Spotify_list)

#display albums and their songs
@app.route('/YoutubeSpotify/Spotify/Albums', methods=['GET'])
def Spotify_Album_display():
    Spotify_list.clear()
    connection = create_connection("Database.db")
    albumsql = "SELECT Album,Artist FROM Spotify_Youtube"
    list1 = execute_read_query(connection, albumsql)

    for a in list1:
        # songsql = "SELECT Track, Stream, Url_spotify FROM Spotify_Youtube WHERE Album LIKE '%" +a[0] + "%'"
        # list2 = execute_read_query(connection, songsql)
        Spotify_list.append(
            {
                'Album': a[0],
                'Artist': a[1]
                
            }
        )
    connection.close()
    return jsonify(Spotify_list)

#shows songs from an album
@app.route('/YoutubeSpotify/Spotify/AlbumSearch',methods=['GET'])
def Spotify_Album_Search():
    Spotify_list.clear()
    connection = create_connection("Database.db")
    album = None
    if 'album' in request.args:
        album = request.args['album']
    else:
        return "Incorrect syntax, please specify an album"
    sql = "SELECT Track, Artist, Uri, Stream FROM Spotify_Youtube WHERE Album LIKE '%" + album + "%'"
    result = execute_read_query(connection, sql)

    songs = []

    for track in result:
        songs.append(
            {
                'Track': track[0],
                'Artist': track[1],
                'Stream': track[3],
                'Url': track[2]
            }
        )

    Spotify_list.append(
        {
            'Album': album,
            'Tracks': songs
        }
    )

    connection.close()
    return jsonify(Spotify_list)


#shows all records
@app.route('/Youtube_Spotify/all', methods=['GET'])
def get_all():
    Youtube_list.clear()
    connection=create_connection("Database.db")
    sql = "SELECT * FROM Spotify_Youtube"
    list=execute_read_query(connection,sql)
    connection.close()
    
    for track in list:
            Youtube_list.append(
                {
                    'Title': track[0],
                    'Views': track[1],
                    'Likes': track[2],
                    'Channel': track[3],
                    'Url': track[4]
                }
            )
    return jsonify(Youtube_list)


if __name__ == '__main__':
    app.run()