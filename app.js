const sqlite3 = require('sqlite3').verbose();
const express = require('express');
const app = express();
const db = new sqlite3.Database('../Youtube-Spotify-Application/archive/Database.db');


app.listen(3000,function(){
    console.log('Server is running on port 3000');
})


db.all('SELECT Track, Views FROM Spotify_Youtube WHERE Artist Like \'%Drake\'', function(err,rows) {
    if(err) {
        return console.log('Something went wrong');
    }
    rows.forEach(row => {
        console.log('Track: ', row.Track);
        console.log('Views: ', row.Views);
    });
});

db.close();