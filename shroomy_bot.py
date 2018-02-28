# System imports
import asyncio
import platform
from decimal import Decimal, InvalidOperation

# imports needed to run discord
import discord
from discord.ext.commands import Bot

# personal files
import config
import commons
import discord_commons
import otherapi

# Initialize our Bot
shroomy = Bot(description="Shroomy Bot " + config.version,
              command_prefix=config.prefix,
              pm_help=False)


# Initialize event when Bot is first invited
@shroomy.event
async def on_ready():
    print('Logged in as {0} (ID:{1})'.format(shroomy.user.name, shroomy.user.id))
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'
          .format(discord.__version__, platform.python_version()))
    print('--------')
    print('Current Version: {0}'.format(config.version))
    print('--------')
    print('Use this link to invite {}:'.format(shroomy.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'
          .format(shroomy.user.id))
    return await shroomy.change_presence(game=discord.Game(name=config.game))


@shroomy.event
async def on_message(message):
    # Only listen to messages from other people
    if message.author == shroomy.user:
        return

    if message.content.startswith(shroomy.user.mention):
        if "ask me" in message.content:
            question, num_answer = commons.get_random_math_question()
            await shroomy.send_message(
                message.channel,
                "Ok, {0}, what is {1}?".format(
                    message.author.mention,
                    question))
            try:
                reply_message = await shroomy.wait_for_message(
                    author=message.author,
                    channel=message.channel,
                    timeout=20.0)
            except asyncio.TimeoutError:
                pass
            if reply_message is None:
                return await shroomy.send_message(
                    message.channel,
                    "Oh, sorry, you took too long. Try again")
            message_text = reply_message.content
            if message_text:
                try:
                    reply = message_text.split(' ')[0]  # only look at first word
                    num_input = Decimal(reply)
                except InvalidOperation:
                    reply = message_text
                    num_input = None
            bot_reply = "You replied with: {0}\n{1}".format(
                num_input if (num_input is not None)  # If input was a number, show
                else reply,  # Otherwise, display what was entered
                "That's right! Thanks for playing!"  # Result if right
                if (
                        num_input is not None
                        and num_answer == num_input
                )
                else ("Oh no that wasn't right..."
                      "The answer is {0}!").format(num_answer)  # Result if wrong
                )
            return await shroomy.send_message(message.channel, bot_reply)
        # await shroomy.add_reaction(message, '\U0001F60D')
        await asyncio.sleep(1)
        # ctx = await Bot.get_context("-poke {0}".format(message.author.mention))
        # return await shroomy.invoke(ctx)
        return await shroomy.send_message(
            message.channel,
            "Hello, {0}".format(message.author.mention))

    return await shroomy.process_commands(message)
        

# [mood] command. Generates random mood whenever it is called.
@shroomy.command()
async def mood():
    """Generate text with a custom emoji from server"""
    # Retrieve a random item from custom emojis from the server
    # Make sure the emojis are unrestricted otherwise they will be ignored
    custom_emojis = [emoji for emoji in shroomy.get_all_emojis() if not emoji.roles]
    
    if not custom_emojis:
        return await shroomy.say((
            "Aww... "
            "There's no custom emojis I can express in this server. "
            "In that case my mood is :poop:"))

    # Retrieve random emoji retrieved from server and format it to be shown on chat.
    emoji_string = discord_commons.format_emoji(
        commons.get_random_item(custom_emojis))

    # Display on Discord
    await shroomy.say("Hai, my current mood is... " + emoji_string)
    await asyncio.sleep(1)
    await shroomy.say("...for now anyways. Ask me again later.")


# [choose] command.
@shroomy.command()
async def choose(*args):
    """Choose one or more items asked"""
    items = [text.replace(',', '') for text in args if text.lower() != "or"]
    size = len(items)
    if size == 0:
        return await shroomy.say("There wasn't anything to choose from. :cry:")
    elif size == 1:
        return await shroomy.say(
            "Well... I guess {0} since that's the only option!".format(
                str(items[0])))
    else:            
        item_chosen = commons.get_random_item(items)
        if item_chosen == "me":
            item_chosen = "you"
        return await shroomy.say("I choose... {0}!".format(
            str(item_chosen)))
    

# [goodbye] command. Logs the bot off discord if owner calls it;
# otherwise, bot will simply say goodbye to the caller.
# uses 'dad' variable in config.py
@shroomy.command(pass_context=True)
async def goodbye(ctx):
    """Sends a goodbye text; stops if host"""
    if config.dad not in ctx.message.author.name:
        return await shroomy.say("Oh! Goodbye, "
                                 + ctx.message.author.mention
                                 + "! See you again soon.")
    await shroomy.say("I'm logging off. Goodbye frineds!")
    await shroomy.close()


# [poke] command. If entered a user who is not the sender nor the bot,
# it will mention that the sender poked the user.
# Otherwise, it will assume the sender is poking the bot.
@shroomy.command(pass_context=True, aliases=['interact', 'hug', 'pet'])
async def poke(ctx, member: discord.Member = None):
    """ poke someone. Assumes itself if no mention.

        Can also use -interact, -hug, or -pet instead
    """
    action_dict = {
        'poke': "poking",
        'hug': "hugging",
        'pet': "petting",
        'interact': "interacting with"
        }
    source = ctx.message.author
    poking_bot = False if (member is not None and member != shroomy.user) else True
    if poking_bot:
        await shroomy.say('Hello, {0}! You are {1} me!'
                          .format(source.mention,
                                  action_dict[ctx.invoked_with]))
    else:
        await shroomy.say('Hey {0}, {1} is {2} you!'
                          .format(member.mention,
                                  source.mention,
                                  action_dict[ctx.invoked_with]))


# [pkmn]
@shroomy.command()
async def pkmn(*, pokemon="MissingNo"):
    """Looks up pokemon of the given name"""
    msg = await shroomy.say("Ok, let me look it up...")
    result_dict = otherapi.get_pokemon(pokemon)
    types = ", ".join((pkmn_type.title() for pkmn_type in result_dict['pkmn_types']))
    embed = discord.Embed(color=0x2b9b29)
    embed.add_field(name="Pokemon#{0}".format(result_dict['pkmn_id']),
                    value="{0}".format(result_dict['pkmn_name'].title()),
                    inline=True)
    embed.add_field(name="Type:", value=types, inline=True)
    embed.set_image(url=result_dict['pkmn_sprite'])
    embed.set_footer(text="courtesy of {0}".format(result_dict['source']))
    footer_text = "Pokemon found!"
    if result_dict.get('error', ""):
        footer_text = "Oops! | {0}".format(result_dict['error'])
    await asyncio.sleep(2)
    return await shroomy.edit_message(msg, new_content=footer_text, embed=embed)
    # return await shroomy.say(content=footer_text, embed=embed)


@shroomy.group(pass_context=True)
async def say(ctx):
    """Repeats sender. If nothing, a quote. type '-help say' for more"""
    if ctx.invoked_subcommand is None:
        # if a phrase was passed, repeat what they said
        if ctx.subcommand_passed is not None:
            # remove the command from the phrase
            msg = ctx.message.content[len(ctx.prefix+ctx.invoked_with):].strip()
            embed = discord.Embed(color=0x2b9b29)
            embed.add_field(name="I say...", value=msg, inline=False)
            embed.set_image(url=("https://cdn.discordapp.com/"
                                 "emojis/401429201976295424.png"))
            return await shroomy.say(embed=embed)
        
        # if no phrases passed, return a random quote
        result_dict = otherapi.get_random_quote()
        if not result_dict.get('error', ""):
            embed = discord.Embed(title="A quote for you...",
                                  url=result_dict['source'], color=0x2b9b29)
            embed.add_field(name="**{0}**".format(result_dict['author']),
                            value="{0}".format(result_dict['quote']), inline=False)
            return await shroomy.say(embed=embed)
        else:
            return await shroomy.say(
                content="O-oh | Failed: {0}".format(result_dict['error']))


@say.command()
async def romaji(*, args="nani"):
    """Converts words to kata/hira and vice versa"""
    embed = discord.Embed(color=0x2b9b29)
    embed.set_image(url=("https://cdn.discordapp.com/"
                         "emojis/401429201976295424.png"))
    return await shroomy.say(content=args, embed=embed)
    return


# PENDING #
@say.command()
async def woof():
    """Send a woof"""
    result_dict = otherapi.get_random_uk_doge()
    if not result_dict.get('error', ""):
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
    """type '-help define' for more"""
    if ctx.invoked_subcommand is None:
        # if a phrase was passed, find its english definition
        if ctx.subcommand_passed is not None:
            # retrieve only the first word after the command
            word = ctx.message.content.split(" ")[1]
            result_dict = otherapi.get_dictionary(word, config.oxford_app_id, config.oxford_app_key)
            if not result_dict.get('error', ""):
                etymologies = '; '.join(result_dict['etymology'])
                definitions = '\n'.join(("{0}. {1}".format(count, eng_def)
                                         for count, eng_def
                                         in enumerate(result_dict['definitions'], 1)
                                         if not eng_def))
                embed = discord.Embed(color=0x2b9b29)
                embed.add_field(name="Entry found for", value=word, inline=True)
                if etymologies:
                    embed.add_field(name="Etymologies",
                                    value=etymologies, inline=True)
                if definitions:
                    embed.add_field(name="Definition(s)",
                                    value=definitions, inline=False)
                embed.set_image(url=("https://cdn.discordapp.com/"
                                     "emojis/401429201976295424.png"))
                embed.set_footer(text="Made possible by {0}".format(result_dict['source']))
                return await shroomy.say(embed=embed)
            else:
                return await shroomy.say("Oops! | {0}".format(result_dict['error']))
        return await shroomy.say("What should I define?")


# [define jp]
@define.command()
async def jp(*, words=""):
    """Looks up a japanese definition"""
    result_dict = otherapi.get_jisho_page(words)
    if not result_dict.get('error', ""):
        speech_types = '; '.join(result_dict['speech_type'])
        definitions = '\n'.join(("{0}. {1}".format(count, eng_def)
                                for count, eng_def
                                in enumerate(result_dict['definitions'], 1)))
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
        embed.set_image(url=("https://orig00.deviantart.net/"
                             "ca57/f/2015/073/2/c/"
                             "joe0001_by_nch85-d8logqm.gif"))
        embed.set_footer(text="Made using {0}".format(result_dict['source']))
        await shroomy.say(embed=embed)
    else:
        await shroomy.say("Oops! | {0}".format(result_dict['error']))


# [__echo_no_cmd] command.
@shroomy.command(pass_context=True, name='echo')
async def __echo_no_cmd(ctx, *args):
    # if config.dad not in ctx.message.author.name:
    #    return
    message = ' '.join(args)
    print(ctx.message.author.name + " called echo: " + ctx.message.content)
    await shroomy.delete_message(ctx.message)
    embed = discord.Embed(color=0x2b9b29)
    embed.add_field(name="Hey!", value=message, inline=False)
    embed.set_image(url=("https://cdn.discordapp.com/"
                         "emojis/401429201976295424.png"))
    return await shroomy.say(embed=embed)

shroomy.run(config.app_id)
