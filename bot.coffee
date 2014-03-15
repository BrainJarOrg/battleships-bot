###

  Random bot: an example bot to illustrate how easy it is to write one.
  Author: Mikolaj Pawlikowski (mikolaj@pawlikowski.pl)

###

state = JSON.parse process.argv.slice(2)


rand = (n) ->
  Math.floor(Math.random()*100000 + new Date().getTime()) % (n+1)

randomMove = ->
  "#{rand(7)}#{rand(7)}"

if state.cmd is 'init'
  diff = 0
  config = {}
  for i in [2..5]
    config[i] =
      point: "#{rand(7-i)}#{diff}"
      orientation: "horizontal"
    diff = diff + 1 + rand(1)
  console.log JSON.stringify config

else
  move = randomMove()
  while (move in state.hit) or (move in state.missed)
    move = randomMove()
  console.log JSON.stringify
    move: move
