# System imports
import asyncio
import platform

# imports needed to run discord
import discord
from discord.ext.commands import Bot

# personal files
import config

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
    """
    \"""Check if the caller is the ownder. Useful for having owner only commands.\"""
    if ctx.message.author.id == shroomy.application_info().owner:
        return True
    return False
    """
    return True


@shroomy.event
async def on_message(message):
    # Only listen to messages from other people
    if message.author == shroomy.user:
        return

    if message.content.startswith(shroomy.user.mention):
        # await shroomy.add_reaction(message, '\U0001F60D')
        await asyncio.sleep(1)
        # ctx = await Bot.get_context("-poke {0}".format(message.author.mention))
        # return await shroomy.invoke(ctx)
        return await shroomy.send_message(
            message.channel,
            "Hello, {0}".format(message.author.mention))

    return await shroomy.process_commands(message)


@shroomy.check(is_owner)
@shroomy.command(hidden=True)
async def load(extension_name: str):
    """Loads an extension."""
    try:
        shroomy.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await shroomy.whisper("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await shroomy.say("{} loaded.".format(extension_name))


@shroomy.check(is_owner)
@shroomy.command(hidden=True)
async def unload(extension_name: str):
    """Unloads an extension."""
    shroomy.unload_extension(extension_name)
    await shroomy.whisper("{} unloaded.".format(extension_name))


# [__echo_no_cmd] command.
@shroomy.check(is_owner)
@shroomy.command(pass_context=True, name='echo', hidden=True)
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


if __name__ == "__main__":
    for extension in config.bot_extensions:
        try:
            shroomy.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    shroomy.run(config.app_id)
