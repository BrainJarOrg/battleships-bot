###

  Random bot: an example bot to illustrate how easy it is to write one.

  It doesn't do much: starts with a fixed config and plays a random, valid move.

  Author: Mikolaj Pawlikowski (mikolaj@pawlikowski.pl)

###


# this is a very simple bot, it always starts the same
config =
  2:
    point: "00"
    orientation: "vertical"
  3:
    point: "22"
    orientation: "vertical"
  4:
    point: "42"
    orientation: "vertical"
  5:
    point: "37"
    orientation: "horizontal"

randomMove = ->
  "#{Math.round(Math.random()*7)}#{Math.round(Math.random()*7)}"


# get and parse the state
# it will be called like so:
#     coffee bot.coffee "{'cmd':'init'}"

incoming = JSON.parse process.argv.slice(2)

# they want us to set up our ships
if incoming.cmd is 'init'
  console.log JSON.stringify config

# otherwise, let's play!
# we should get something like this:
# {
#     "cmd": "move",
#     
#     "moves": ["0001", "1003", "1113"], // an array representing the the sequence of moves and results (see below)
# 
#     "hit"       : ["20", "30"],  // the cells shot at and hit
#     "missed"    : ["44", "01"],  // the cells shot at but missed
#     "destroyed" : [2]            // sizes (2, 3, 4, 5) of destroyed opponent's ships
# }
else
  move = randomMove()
  while (move in incoming.hit) or (move in incoming.missed)
    move = randomMove()
  console.log JSON.stringify
    move: move
