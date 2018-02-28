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
        await shroomy.sleep(1)
        # ctx = await Bot.get_context("-poke {0}".format(message.author.mention))
        # return await shroomy.invoke(ctx)
        return await shroomy.send_message(
            message.channel,
            "Hello, {0}".format(message.author.mention))

    return await shroomy.process_commands(message)


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


if __name__ == "__main__":
    for extension in config.bot_extensions:
        try:
            shroomy.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    shroomy.run(config.app_id)
