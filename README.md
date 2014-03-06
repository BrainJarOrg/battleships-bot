# Brainjar.org - Battleships 

![alt text](https://raw.github.com/BrainJar/battleships/master/resources/brainjar_org_logo_200.png "Logo Brainjar.org")

This is a simple bot to play [https://brainjar.org/battleships](https://brainjar.org/battleships)


## What's here ?

This is a template to get you started quickly.

## How to play

### 1. Check the rules of the game

The game engine we use is open source and available here: https://github.com/BrainJar/battleships

Start with reading the rules https://github.com/BrainJar/battleships#rules-of-the-game

### 2. Fork this repository

### 3. Hack your bot

A Battleships bot is a very simple creature.

It consists of a run.sh and the source code in one of the following languages
- coffeescript
- javascript
- python
- ruby
- perl
- PHP

## HOWTO

### run.sh


### Source code

#### Begginning of the game

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
