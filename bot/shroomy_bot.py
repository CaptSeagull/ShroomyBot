# System imports
import platform
import logging

# imports needed to run discord
import discord
from discord.ext import commands
from discord.ext.commands import Bot

# personal files
import tools as config

# Initialize our Bot
shroomy = Bot(description="Shroomy Bot " + config.version,
              command_prefix=config.prefix,
              pm_help=False)


# Initialize event when Bot is first invited
@shroomy.event
async def on_ready():
    presence_string = '\n--------\n'.join([
        "Logged in as {0} (ID:{1})".format(shroomy.user.name, shroomy.user.id),
        "Current Discord.py Version: {} | Current Python Version: {}".format(
            discord.__version__, platform.python_version()),
        "Current Version: {0}".format(config.version),
        "Use this link to invite {}:".format(shroomy.user.name),
        "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8".format(shroomy.user.id)
    ])
    logging.info(presence_string)
    return await shroomy.change_presence(game=discord.Game(name=config.game))


def is_owner(ctx):
    return ctx.message.author.id == config.owner_id


@shroomy.event
async def on_message(message):
    # Only listen to messages from other people and none bots
    if message.author == shroomy.user or message.author.bot:
        return

    return await shroomy.process_commands(message)


@commands.check(is_owner)
@shroomy.command(hidden=True)
async def load(extension_name: str):
    """Loads an extension."""
    try:
        shroomy.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        return await shroomy.whisper("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
    return await shroomy.whisper("{} loaded.".format(extension_name))


@commands.check(is_owner)
@shroomy.command(hidden=True)
async def unload(extension_name: str):
    """Unloads an extension."""
    shroomy.unload_extension(extension_name)
    return await shroomy.whisper("{} unloaded.".format(extension_name))


@commands.check(is_owner)
@shroomy.command(hidden=True)
async def reload(extension_name: str):
    """Unloads THEN loads an extension."""
    try:
        shroomy.unload_extension(extension_name)
        shroomy.load_extension(extension_name)
    except Exception as ex:
        exce = '{}: {}'.format(type(ex).__name__, ex)
        logging.error('Failed to load extension {}\n{}'.format(extension_name, exce))
    return await shroomy.whisper("{} reloaded.".format(extension_name))


@commands.check(is_owner)
@shroomy.command(hidden=True)
async def update_subreddit():
    """Updates subreddits to be used"""
    try:
        import tools
        tools.update_subreddits()
    except Exception as ex:
        exce = '{}: {}'.format(type(ex).__name__, ex)
        logging.error('Failed to update subreddits \n{}'.format(exce))
    return await shroomy.whisper("subreddits reloaded.")


@commands.check(is_owner)
@shroomy.command(pass_context=True, hidden=True)
async def echo(ctx, *args):
    message = ' '.join(args)
    logging.debug(ctx.message.author.name + " called echo: " + ctx.message.content)
    await shroomy.delete_message(ctx.message)
    embed = discord.Embed(color=ctx.message.author.color)
    embed.add_field(name="Hey!", value=message, inline=False)
    embed.set_image(url=shroomy.user.avatar_url)
    return await shroomy.say(embed=embed)


@commands.check(is_owner)
@shroomy.command(pass_context=True, hidden=True)
async def clean(ctx, *, args=""):
    limit = 10
    bot_del = False
    user = None

    argv = args.split(config.prefix)
    for arg in argv:
        if arg.startswith('size'):
            try:
                limit = int(arg[len('size'):])
            except:
                logging.exception("Exception when parsing limit")
                pass
        elif arg.startswith('type'):
            bot_del = True if 'bot' in arg else False
            user = ctx.message.author if 'me' in arg else None

    def is_included(message):
        has_check = bot_del or user is not None
        should_delete_bot = False
        should_delete_me = False
        if bot_del:
            should_delete_bot = message.author == shroomy.user
        if user:
            should_delete_me = message.author == user
        return not has_check or should_delete_bot or should_delete_me

    deleted = await shroomy.purge_from(ctx.message.channel, limit=limit, check=is_included)
    logging.info('Deleted {} message(s)'.format(len(deleted)))


def run():
    for extension in config.bot_extensions:
        cogs_dir = "cogs"
        try:
            shroomy.load_extension(cogs_dir + "." + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            logging.error('Failed to load extension {}\n{}'.format(extension, exc))

    shroomy.run(config.app_id)


if __name__ == "__main__":
    run()
