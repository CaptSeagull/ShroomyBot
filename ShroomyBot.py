# imports needed to run discord
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import platform

# personal files
import config
import commons
import discord_commons
import otherapi

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
    return await shroomy.change_presence(game=discord.Game(name='Monster Hunter World'))

# [mood] command. Generates random mood whenever it is called.
@shroomy.command()
async def mood():
    # Retrieve a random item from custom emojis from the server
    custom_emojis = []
    for emoji in shroomy.get_all_emojis():
        # Make sure the emojis are unrestriced otherwise they will be ignored
        if not emoji.roles:
            custom_emojis.append(emoji)

    if not custom_emojis:
        return await shroomy.say("Aww...There's no custom emojis I can express in this server."
                                 + " In that case my mood is :poop:")

    # Retrieve random emoji retrieved from server and format it to be shown on chat.
    emoji_item = commons.getRandomTuple(custom_emojis)
    emoji_string = discord_commons.formatEmoji(emoji_item)

    # Display on Discord
    await shroomy.say("Hai, my current mood is... " + emoji_string)
    await asyncio.sleep(1)
    await shroomy.say("...for now anyways. Ask me again later.")

# [choose] command.
@shroomy.command()
async def choose(*args):
    items = []

    for text in args:
        if text == 'or':
            continue
        items.append(text.replace(',',''))
    size = len(items)
    if size == 0:
        await shroomy.say("There wasn't anything to choose from. :cry:")
    elif size == 1:
        await shroomy.say("Well... I guess " + str(items[0]) + " since that's the only option!")
    else:            
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

# [pkmn]
@shroomy.command()
async def pkmn(*args):
    await shroomy.say("Ok, let me look it up...")
    pokemon = ' '.join(args)
    result_msg = otherapi.getPokemon(pokemon)
    await shroomy.say(result_msg)

# PENDING #
@shroomy.command()
async def say(*args):
    word = ' '.join(args)
    embed = discord.Embed(color=0x2b9b29)
    embed.add_field(name="I say...",value="    {0}!!".format(word), inline=False)
    embed.set_image(url="https://cdn.discordapp.com/emojis/401429201976295424.png?v=1")
    await shroomy.say(embed=embed)

# [define]
@shroomy.command()
async def define(command, *args):
    if not command:
        ### CREATE HELP ###
        return
    if command == "jp":
        words = ' '.join(args)
        result_msg = otherapi.getJishoPage(words)
        if not result_msg['error']:
            definitions = ""
            count = 1
            for eng_def in result_msg['definitions']:
                definitions += "{0}. {1}\n".format(count, eng_def)
                count += 1
            
            embed = discord.Embed(color=0xa6dded)
            embed.add_field(name="Reading(s)",value="{0} ({1})".format(result_msg['writing'],result_msg['reading']), inline=False)
            embed.add_field(name="Definition(s)",value=definitions, inline=False)
            #embed.set_image(url="https://cdn.discordapp.com/emojis/401429201976295424.png?v=1")
            embed.set_image(url="https://orig00.deviantart.net/ca57/f/2015/073/2/c/joe0001_by_nch85-d8logqm.gif")
            embed.set_footer(text="Made using Jisho http://jisho.org")
            await shroomy.say(embed=embed)
        else:
            await shroomy.say(result_msg['error'])
                
    else:
        ### CREATE HELP ###
        return

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
