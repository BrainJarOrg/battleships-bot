# Brainjar.org - Battleships bot

![alt text](https://raw.github.com/BrainJar/battleships/master/resources/brainjar_org_logo_200.png "Logo Brainjar.org")

A simple bot to play [https://brainjar.org/battleships](https://brainjar.org/battleships)


## What's here ?

This is a sandbox,
test robot.

## How to play

### 1. Check the rules of the game

The game engine we use is open source and available here: https://github.com/BrainJar/battleships

Start with reading the rules https://github.com/BrainJar/battleships#rules-of-the-game

### 2. Fork this repository

It's easy: https://github.com/BrainJar/battleships-bot/fork

### 3. Hack your bot

A Battleships bot is a very simple creature.

It consists of a run.sh and the source code in one of the following languages:
- Coffeescript 1.7.1
- Java 7 (/!\ in this case you need to provide a jar file... and be careful with RAM and timeouts! ;-))
- Javascript (Node.js) 0.10.2
- PHP 5.3.10
- Perl 5.14.2
- Python 2.7.3
- Ruby 1.8.7

### 4. Test it locally, before the fight

To run your bot (with run.sh ready) you will need node.js and coffee-script installed.


    npm install
    coffee simulate.coffee --help

    Usage: simulate.coffee [options]

        Options:

        -h, --help       output usage information
        -V, --version    output the version number
        -n, --norefresh  doesn't download the game engine and random bot [false]
        -v, --verbose    verbose mode [false]

It's goting to download the game engine and a bot template, and play against your local bot. Yeah ! :-)


#### run.sh

This is the script we will call, which has to run properly your thing. You need to adapt it to the language you are going to use.

You can check examples https://github.com/BrainJar/battleships-bot/blob/master/run.sh


#### Code

You can code however you like as long as you follow the rules below. Third-party code is ok, as long as it doesn't violate any licences and is clearly stated in your README.md

#### Few rules

- bots are self-contained - all necessary code is in the repository
- bots are stateless - no storage is available, and don't have a memory between moves
- bots don't browse internet - your sandbox is isolated
- bots are slim - you have max 2MB for the code
- bots are short - your sandbox has 256 MB of RAM, so be reasonable
- bots are quick - timeout 2s per move
- bots play fair - if your code uses other people's code, state it clearly in your README.md

Please note that if you violate any of these, your bot will just keep getting beaten up. Be nice to your bot.

## HOWTO

### run.sh

Easy. Just run your script using one of the interpreters:

    #   coffeescript    ex. 'coffee bot.coffee $1'
    #   javascript      ex. 'node bot.js $1'
    #   python          ex. 'python bot.py $1'
    #   perl            ex. 'perl bot.pl $1'
    #   ruby            ex. 'ruby bot.rb $1'
    #   PHP             ex. 'php bot.php $1'

### Source code

#### Beginning of the game

##### Request for the init config

The bot will receive a following JSON object.

    {
        "cmd": "init"
    }

##### Initial config format

Initial config response has to follow this JSON format:

    {
        "2" :
            {
                "point": "00",
                "orientation" : "vertical"   // possible values "horizontal", "vertical"
            },
        "3" :
            {
                "point": "22",
                "orientation" : "vertical"
            },
        "4" :
            {
                "point": "42",
                "orientation" : "vertical"
            },
        "5" :
            {
                "point": "37",
                "orientation" : "horizontal"
            }
    }

This initial config will represent


        0   1   2   3   4   5   6   7
    0   X
    1   X
    2           X       X
    3           X       X
    4           X       X
    5                   X           
    6
    7               X   X   X   X   X


#### Moves

##### Grid snapshots

Before each move, player get the current situation - the opponent's grid's snapshot with marked fields.

A snapshot is represented by a JSON:

    {
        "cmd": "move",              // for less user-friendly languages

        // an array representing the the sequence of moves and results (see below)
        "moves": ["0001", "1003", "1113", ...],

        // for your convenience, we also suply the following data
        "hit"       : ["20", "30"],  // the cells shot at and hit
        "missed"    : ["44", "01"],  // the cells shot at but missed
        "destroyed" : [2]            // sizes (2, 3, 4, 5) of destroyed opponent's ships
    }

In the array representing the sequence, (player, move, results) are encoded.

    player = 0|1 // player number 0 or 1
    move   = XY  // see above
    result = 1|3 // 1 means missed, 3 means hit

For example an array:

    ["0001", "1003", "1113", "1331", "0123", "0133"]

Represents:
 - player 0 shoots 00 and misses
 - player 1 shoots 00 and hits
 - player 1 shoots 11 and hits
 - player 1 shoots 33 and misses
 - player 0 shoots 12 and hits
 - player 0 shoots 13 and hits


##### Move format

A move (as returned by the bot) is represented by a string (column, row).

A following JSON has to be returned for a bot to play a move.

    {
        "move" : "00"
        // any invalid output or shooting twice at the same cell will be taken as a surrender
    }



##### Valid turn

In a turn, player has to chose a valid location on the opponents side. Otherwise they lose.



## LICENCE

The MIT License (MIT)

Copyright (c) 2014 Mikolaj Pawlikowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
