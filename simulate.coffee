execSync = require "exec-sync"
colors   = require "colors"
http     = require "https"
fs       = require "fs"

path_battleships     = ".local.raw.github.com.brainjar.battleships.coffee"
path_battleships_bot = ".local.raw.github.com.brainjar.battleships-bot.coffee"

program = require("commander")
program.version("0.0.1")
program.option("-n, --norefresh", "doesn't download the game engine and random bot [false]", false)
program.option("-v, --verbose", "verbose mode [false]", false)
program.parse process.argv

getFreshCopies = (callback) ->
    console.log "INFO".grey, "fetching", path_battleships
    file    = fs.createWriteStream(path_battleships)
    request = http.get "https://raw.github.com/BrainJar/battleships/master/battleships.coffee", (response) ->
        response.pipe file
        file.on "finish", ->
            file.close()

            console.log "INFO".grey, "fetching", path_battleships_bot
            file    = fs.createWriteStream(path_battleships_bot)
            request = http.get "https://raw.github.com/BrainJar/battleships-bot/master/bot.coffee", (response) ->
                response.pipe file
                file.on "finish", ->
                    file.close()
                    console.log "INFO".grey, "fetching done"
                    callback()

parseJSON = (data) ->
    try
        config = JSON.parse data
    catch error
        console.log "ERROR".red, "Invalid JSON"
        console.log data
        process.exit 1
    config

simulate = ->

    Battleships = require "./#{path_battleships}"

    game = new Battleships()

    runBot = (cmd) ->
        run = "#{cmd} #{JSON.stringify(game.getBotCommand())}"
        console.log("Executing command: #{run}".grey) if program.verbose
        answer = execSync(run)
        console.log("Bot says: #{answer}".grey) if program.verbose
        answer

    bots = ["coffee #{path_battleships_bot}", "chmod +x ./run.sh && ./run.sh"]

    config0 = parseJSON runBot(bots[0])
    config1 = parseJSON runBot(bots[1])

    if not game.setup(config0, config1)
        console.log "ERROR".red, "Invalid config"
        console.log "Player #{game.winner()}:".yellow
        console.log configs[game.winner()]
        process.exit 1

    gameLoop = ->

        if game.over()
            console.log "Game over! Winner: #{game.winner()}"
            game.debugPrint()
            process.exit 0
        else
            data = runBot bots[game.player()]
            move = JSON.parse data

            who = if game.player() is 0 then "local".green else "random".blue
            console.log "Bot", who, "plays: #{data}"

            game.play move

            gameLoop()

    gameLoop()

if program.norefresh
    simulate()
else
    getFreshCopies ->
        simulate()
