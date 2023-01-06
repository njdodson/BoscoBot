import discord
from discord.ext import commands
import random
from FantasyGame import HuntGame, HuntPlayer

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$',intents=intents)
token="MTA0MTg1MzE3OTYzOTM2NTY1Mg.GLoPOh.RUCgV0z2YcPvPoS1XEIqQYCzKOtkE5nNPN_lyw"

### Global Variables ###
#Creat the Current Showdown Fantasy Game
sdFantasy=HuntGame()


### Utility ###
@bot.event
async def on_ready():
    print("Beep boop, Rock and Stone!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("The heck you sayin dude")
        return
    raise error


@bot.event
async def on_message(message):
    #Cancel if the bot sent this message... could be a problem
    if message.author == bot.user:
        return

    #Check for Rock and Stone 'ing!
    if "rock" in message.content.lower().strip(" ") and "stone" in message.content.lower().strip(" "):
        print("Someone rocked and stoned!")
        IDnum=str(random.randint(10000,99999))
        await message.channel.send("Rock and Stone Employee #"+IDnum+"!")

    #Process a command instead
    await bot.process_commands(message)


### Deep Rock Galactic ###
@bot.command(brief="Pick random roles for DRG game", description="Randomly selects roles for players in your voice channel for a game of Deep Rock Galactic")
async def pickRolesDRG(ctx):
    print("Oh boy time to pick roles for "+str(ctx.author))
    roles=["Gunner","Driller","Engineer","Scout"]

    #Get player list based on people in voice channel with author,
    #return error if not in a VC
    voice=ctx.author.voice
    if voice == None:
        await ctx.send("Please enter a voice channel to use this command")
        return
    else:
        voiceChannel=ctx.author.voice.channel

    players=voiceChannel.members
    for player in players:
        playerName=player.name
        role=roles[random.randint(0,len(roles))]
        await ctx.send(playerName+" - "+role)
        roles.remove(role)
        #roles.pop(roles.index(role))

### Hunt: Showdown ###
@bot.command(brief="Start a game of Showdown Fantasy",description="Starts a game of Hunt:Showdown Fantasy, where multiple teams can compete against each other in a Fantasy Football Style")
async def StartShowdown(ctx,gamemode="Classic",nTeams=2):
    gamemode=gamemode.title()
    await ctx.send("Starting a game of Showdown Fantasy, selected gamemode: "+gamemode)

    #"Classic" fantasy game that prioritzes getting a bounty over kills
    if(gamemode.lower()=="classic"):
        await ctx.send("Get those bounties, whatever the cost.")

    #"Slayer" gamemode, which gives more points to player kills and removes points on downs
    elif(gamemode.lower()=="slayer"):
        await ctx.send("Kill or be killed boys, happy hunting!")

    elif(gamemode.lower()=="custom"):
        await ctx.send("Custom gamemode not supported yet, yell at Angel or something idc")
        return

    else:
        await ctx.send("What the heck is "+gamemode+"?")
        return

    #Team 1 at index 0, with memebers as a nested list
    teams=[]
    players=[]
    for n in range(nTeams):
        await ctx.send("Team "+str(n+1)+": enter a voice channel and give me a thumbs up when you're ready!")
        try:
            reaction, user = await bot.wait_for("reaction_add",timeout=120.0)
        #If there is a timeout, just close out and re-do, will come up with something better later.
        except asyncio.TimeoutError:
            await ctx.send("Two minutes have passed, how much time do you need?? Closing down startup...")
            return

        else:
            #Check if reaction user is in a voice channel
            if(user.voice == None):
                await ctx.send(user.name+", you aren't in a voice channel! It's all your fault.")
                return

            #Get a list of discord player objects in the voice channel
            discPlayers=user.voice.channel.members
            team=[]
            for discplayer in discPlayers:
                newPlayer=HuntPlayer(name=discplayer.name)
                players.append(newPlayer)
                team.append(newPlayer.name)
            teams.append(team)

    #Start the game!
    #Set the global game object
    global sdFantasy
    sdFantasy=HuntGame(instance=True,gamemode=gamemode,teams=teams,players=players)
    await ctx.send("Game on! Happy hunting and may the better team win...")

@bot.command(brief="Update your score in current Fantasy game")
async def UpdateScore(ctx,kills=-1,deaths=-1,tokens=-1):
    updatingPlayer=str(ctx.author.name)

    if not sdFantasy.instance:
        await ctx.send("There isn't a game currently running!")
        return

    elif(kills != -1 and deaths != -1 and tokens != -1):
        #Update scores directly without prompting the user
        player=sdFantasy.getPlayer(updatingPlayer)
        player.updateStats(kills,deaths,tokens)
        sdFantasy.calcPlayerScore(player)
        await ctx.send("Player score updated!")
        return

    #If the players did specify, guide them through it and give comments based on how well they did


@bot.command(brief="Display the current Showdown Fantasy game")
async def CheckShowdown(ctx):
    if sdFantasy.instance:
        await ctx.send("There is a fantasy game going on currently!\n"+
                        "Gamemode: "+sdFantasy.gamemode+"\n"+
                        "ppKill: "+str(sdFantasy.ppKill)+"\n"+
                        "ppDeath: "+str(sdFantasy.ppDeath)+"\n"+
                        "ppToken: "+str(sdFantasy.ppToken)+"\n")

        teams=sdFantasy.teams
        await ctx.send(sdFantasy.teamString())
    else:
        await ctx.send("There is no current game going on")

#Fantasy Debug#
@bot.command(brief="Debug tool, force ends current fantasy game")
async def EndShowdown(ctx):
    global sdFantasy
    sdFantasy=HuntGame()

#OH LAWD HE RUNNIN!!!
bot.run(token)
