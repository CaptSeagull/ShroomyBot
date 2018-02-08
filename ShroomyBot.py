# imports needed to run discord
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import platform

# personal files
import config
from config import shroomy_emoji
import commons

# Initialize our Bot
shroomy = Bot(description="Shroomy Bot " + config.version, command_prefix=config.prefix, pm_help=False)

# Initialize event when Bot is first invited
@shroomy.event
async def on_ready():
    print('Logged in as ' + shroomy.user.name + ' (ID:' + shroomy.user.id + ')' )
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Current Version: ' + config.version)
    print('--------')
    print('Use this link to invite {}:'.format(shroomy.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(shroomy.user.id))
    return await shroomy.change_presence(game=discord.Game(name='Game Called \'Life\''))

# [mood] command. Generates random mood whenever it is called.
@shroomy.command()
async def mood():
    # Retrieve a random item
    mood_items = tuple( shroomy_emoji.values() )
    mood_string = "Hai, my current mood is... " + commons.getRandomTuple(mood_items)

    # Display on Discord
    await shroomy.say(mood_string)
    await asyncio.sleep(1)
    await shroomy.say("...for now anyways. Ask me again later.")

# [choose] command.
@shroomy.command()
async def choose(*args):
    size = len(args)
    if size == 0:
        await shroomy.say("There wasn't anything to choose from. " + shroomy_emoji['gokucrei'])
    elif size == 1:
        await shroomy.say("Well... I guess " + args[0] + " since that's the only option!")
    else:
        items = []

        #scenarios:
        # 1. spaces only
        # 2. contains or
        # 3. contains comma
        # 4. contains comma AND or

        useDelim = False

        for i in (',','or'):
            if i in args:
                useDelim = True
                break

        if useDelim == True:
            text = ' '.join(args)
            items = commons.getSplit(text)
        else:
            items = args
        item_chosen = commons.getRandomTuple( items )
        if(item_chosen == "me") :
            item_chosen = "you, dad"
        await shroomy.say("I choose... " + str(item_chosen) + "!")
    

# [goodbye] command. Logs the bot off discord if owner calls it; otherwise, bot will simply say goodbye to the caller.
# uses 'dad' variable in config.py
@shroomy.command(pass_context=True)
async def goodbye(ctx):
    if config.dad not in ctx.message.author.name:
        return await shroomy.say("Oh! Goodbye, " + ctx.message.author.mention + "! See you again soon.")
    await shroomy.say("I'm logging off. Goodbye frineds!")
    await shroomy.close()

# [poke] command. If entered a user who is not the sender nor the bot, it will mention that the sender poked the user. Otherwise, it will assume the sender is poking the bot.
@shroomy.command(pass_context=True)
async def poke(ctx, member : discord.Member = None):
    source = ctx.message.author.mention
    pokingBot = True
    if member is not None and member.mention != source and member.bot != True:
        pokingBot = False
    if pokingBot == True:
        await shroomy.say('Hello, {0}!'.format(source))
    else:
        await shroomy.say('Hey {0}, {1} is poking you!'.format(member.mention, source))

# [echoNoCmd] command.
@shroomy.command(pass_context=True)
async def echoNoCmd(ctx, *args):
    if config.dad not in ctx.message.author.name:
        return
    message = ' '.join(args)
    await shroomy.delete_message(ctx.message)
    await asyncio.sleep(1)
    await shroomy.say(message)

# DEBUG get list of emojis
#@shroomy.command()
#async def getEmojis():
#    count = 0
#    for emoji in shroomy.get_all_emojis():
#        await shroomy.say("#" + str(count) + "<:" + emoji.name + ":" + emoji.id + ">")
#        count += 1

shroomy.run(config.app_id)
