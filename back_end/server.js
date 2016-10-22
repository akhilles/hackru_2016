var express = require('express');
const fs = require('fs');
const spawn = require('child_process').spawn;
const stockfish = spawn('stockfish.exe');
var app = express();

var position;
var pos_finished;
var move;

stockfish.stdout.on('data', (data) => {
    if (data.indexOf('Stockfish 7 64 by T. Romstad, M. Costalba, J. Kiiski, G. Linscott') !== -1){
        console.log('out: ' + data);
        out('isready');
    } else if (data.indexOf('bestmove') !== -1) {
        move = data.toString().substring(data.indexOf('bestmove') + 9);
        if (move.indexOf(' ') != -1){
            move = move.substring(0, move.indexOf(' '));
        }
        console.log('out: ' + move);
        pos_finished = position;
    }
});

stockfish.stderr.on('data', (data) => {
    console.log('stderr: ' + data);
});

stockfish.on('close', (code) => {
    console.log('child process exited with code ' + code);
});

stockfish.on('error', (code) => {
    console.log('failed to start child process');
});

app.get('/', function (req, res) {
    pos_finished = "---";
    move = "---";
    position = JSON.parse(req.query.moves).toString().replace(/,/g, " ");
    out('position startpos moves ' + position);

    setTimeout(function(){
        out('go movetime 2900');
        setTimeout(function(){
            res.write(move);
            res.end();
        }, 3000)
    }, 100)
});

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});

var out = function(in_stream) {
    console.log('in: ' + in_stream);
    stockfish.stdin.write(in_stream + '\n');
}