# System imports
import platform

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
        await shroomy.whisper("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await shroomy.whisper("{} loaded.".format(extension_name))


@commands.check(is_owner)
@shroomy.command(hidden=True)
async def unload(extension_name: str):
    """Unloads an extension."""
    shroomy.unload_extension(extension_name)
    await shroomy.whisper("{} unloaded.".format(extension_name))


@commands.check(is_owner)
@shroomy.command(hidden=True)
async def reload(extension_name: str):
    """Unloads THEN loads an extension."""
    try:
        shroomy.unload_extension(extension_name)
        shroomy.load_extension(extension_name)
    except Exception as ex:
        exce = '{}: {}'.format(type(ex).__name__, ex)
        print('Failed to load extension {}\n{}'.format(extension_name, exce))
    return await shroomy.whisper("{} reloaded.".format(extension_name))


@commands.check(is_owner)
@shroomy.command(pass_context=True, name='echo', hidden=True)
async def __echo_no_cmd(ctx, *args):
    message = ' '.join(args)
    print(ctx.message.author.name + " called echo: " + ctx.message.content)
    await shroomy.delete_message(ctx.message)
    embed = discord.Embed(color=0x2b9b29)
    embed.add_field(name="Hey!", value=message, inline=False)
    embed.set_image(url=("https://cdn.discordapp.com/"
                         "emojis/401429201976295424.png"))
    return await shroomy.say(embed=embed)


def run():
    for extension in config.bot_extensions:
        cogs_dir = "cogs"
        try:
            shroomy.load_extension(cogs_dir + "." + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    shroomy.run(config.app_id)


if __name__ == "__main__":
    run()
