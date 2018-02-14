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
    print('Current Discord.py Version: {} | Current Python Version: {}'
          .format(discord.__version__, platform.python_version()))
    print('--------')
    print('Current Version: ' + config.version)
    print('--------')
    print('Use this link to invite {}:'.format(shroomy.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'
          .format(shroomy.user.id))
    return await shroomy.change_presence(game=discord.Game(name='Monster Hunter World'))

@shroomy.event
async def on_message(message):
    # Only listen to messages from other people
    if message.author == shroomy.user:
        return

    if message.content.startswith(shroomy.user.mention):
        if "ask me" in message.content:
            await shroomy.send_message(message.channel, "Ok, {0}, what is 1+1?".format(message.author.mention))
            message = await shroomy.wait_for_message(author=message.author,
                                           channel=message.channel)
            message_text = message.content
            num_answer = 2
            num_input = None
            if message_text:
                try:
                    reply = message.content.split(' ')[0] # only look at first answer
                    num_input = int(reply)
                except ValueError:
                    pass
            bot_reply = "You replied with: {0}".format(num_input)
            if num_input is not None and num_answer == num_input:
                bot_reply += "\nThat's right! Thanks for playing!"
            else:
                bot_reply += "\nOh no that wasn't right...Try again!"
            return await shroomy.send_message(message.channel, bot_reply)
        await shroomy.add_reaction(message, '\U0001F60D')
        await asyncio.sleep(1)
        #ctx = await Bot.get_context("-poke {0}".format(message.author.mention))
        #return await shroomy.invoke(ctx)
        return await shroomy.send_message(
            message.channel, "Hello, {0}".format(message.author.mention))

    return await shroomy.process_commands(message)
        

# [mood] command. Generates random mood whenever it is called.
@shroomy.command()
async def mood():
    """Generate text with a custom emoji from server"""
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
    """Choose one or more items asked"""
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
    

# [goodbye] command. Logs the bot off discord if owner calls it;
# otherwise, bot will simply say goodbye to the caller.
# uses 'dad' variable in config.py
@shroomy.command(pass_context=True)
async def goodbye(ctx):
    """Sends a goodbye text; stops if host"""
    if config.dad not in ctx.message.author.name:
        return await shroomy.say("Oh! Goodbye, " + ctx.message.author.mention + "! See you again soon.")
    await shroomy.say("I'm logging off. Goodbye frineds!")
    await shroomy.close()

# [poke] command. If entered a user who is not the sender nor the bot,
# it will mention that the sender poked the user. Otherwise, it will assume the sender is poking the bot.
@shroomy.command(pass_context=True,aliases=['interact','hug','pet'])
async def poke(ctx, member : discord.Member = None):
    """poke someone. Assumes itself if no mention."""
    action_dict = {
        'poke':"poking",
        'hug':"hugging",
        'pet':"petting",
        'interact':"interacting with"
        }
    source = ctx.message.author
    pokingBot = True
    if member is not None and member.mention != source and member != shroomy.user:
        pokingBot = False
    if pokingBot == True:
        await shroomy.say('Hello, {0}! You are {1} me!'
                          .format(source.mention, action_dict[ctx.invoked_with]))
    else:
        await shroomy.say('Hey {0}, {1} is {2} you!'.format(
            member.mention, source.mention, action_dict[ctx.invoked_with]))

# [pkmn]
@shroomy.command()
async def pkmn(*, pokemon="MissingNo"):
    """Looks up pokemon of the given name"""
    msg = await shroomy.say("Ok, let me look it up...")
    # pokemon = ' '.join(args)
    result_dict = otherapi.getPokemon(pokemon)
    types = ""
    for pkmn_type in result_dict['pkmn_types']:
        types += pkmn_type + " "
    embed = discord.Embed(color=0x2b9b29)
    embed.add_field(name="Pokemon#{0}".format(result_dict['pkmn_id']),
                    value="{0}".format(result_dict['pkmn_name']), inline=True)
    embed.add_field(name="Type:", value=types, inline=True)
    embed.set_image(url=result_dict['pkmn_sprite'])
    embed.set_footer(text="courtesy of {0}".format(result_dict['source']))
    footer_text = "Pokemon found!"
    if result_dict['error']:
        footer_text = "Oops! | {0}".format(result_dict['error'])
    return await shroomy.say(content=footer_text,embed=embed)

@shroomy.group(pass_context=True)
async def say(ctx):
    """Repeats sender. If nothing, a quote."""
    if ctx.invoked_subcommand is None:
        # if a phrase was passed, repeat what they said
        if ctx.subcommand_passed is not None:
            msg = ctx.message.content[
                len( "{0}{1}".format(ctx.prefix,ctx.invoked_with) ):].strip() # remove the command from the phrase
            embed = discord.Embed(color=0x2b9b29)
            embed.add_field(name="I say...",value=msg, inline=False)
            embed.set_image(url="https://cdn.discordapp.com/emojis/401429201976295424.png")
            return await shroomy.say(embed=embed)
        
        # if no phrases passed, return a random quote
        result_dict = otherapi.getRandomQuote()
        if not result_dict['error']:
            embed = discord.Embed(url=result_dict['source'],color=0x2b9b29)
            embed.add_field(name="**{0}**".format(result_dict['author']),
                            value="{0}".format(result_dict['quote']), inline=False)
            return await shroomy.say(embed=embed)
        else:
            return await shroomy.say(
                content="O-oh | Failed: {0}".format(result_dict['error']))

# PENDING #
@say.command()
async def woof():
    """Send a woof"""
    result_dict = otherapi.getRandomUkDoge()
    if not result_dict['error']:
        #embed = discord.Embed(title="woof woof!",color=0x2b9b29)
        embed = discord.Embed(color=0x2b9b29)
        embed.set_image(url=result_dict['doge_url'])
        embed.set_footer(text="courtesy of {0}"
                         .format(result_dict['source']))
        return await shroomy.say(content=":dog: | Woof Woof!",
                                 embed=embed)
    else:
        return await shroomy.say(content=":dog: | Failed: {0}"
                                 .format(result_dict['error']))
@shroomy.group(pass_context=True)
async def define(ctx):
    """Actions to define the given message"""
    if ctx.invoked_subcommand is None:
        return await shroomy.say("What should I define?")

# [define jp]
@define.command()
async def jp(*, words=""):
    """Looks up a japanese definition"""
    #words = ' '.join(args)
    result_dict = otherapi.getJishoPage(words)
    if not result_dict['error']:
        definitions = ""
        count = 1
        for eng_def in result_dict['definitions']:
            definitions += "{0}. {1}\n".format(count, eng_def)
            count += 1
        speech_types = ""
        for speech in result_dict['speech_type']:
            speech_types += speech + " "
        embed = discord.Embed(color=0xa6dded)
        embed.add_field(name="Reading(s)",
                        value="{0} ({1})".format(
                            result_dict['writing'],
                            result_dict['reading']), inline=True)
        if speech_types:
            embed.add_field(name="Type(s) of Speech",
                            value=speech_types, inline=True)
        if definitions:
            embed.add_field(name="Definition(s)",
                            value=definitions, inline=False)
        embed.set_image(url="https://orig00.deviantart.net/ca57/f/2015/073/2/c/joe0001_by_nch85-d8logqm.gif")
        embed.set_footer(text="Made using {0}".format(result_dict['source']))
        await shroomy.say(embed=embed)
    else:
        await shroomy.say("Oops! | {0}".format(result_dict['error']))
            
# [echoNoCmd] command.
@shroomy.command(pass_context=True,name='echo')
async def _echoNoCmd(ctx, *args):
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
