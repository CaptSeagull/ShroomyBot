import asyncio

import discord
from decimal import Decimal, InvalidOperation
from discord.ext import commands

# personal files
import config
import commons
import discord_commons


class fun:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.content.startswith(self.bot.user.mention):
            if "ask me" in message.content:
                return await self.ask_math(message)

    # [mood] command. Generates random mood whenever it is called.
    @commands.command()
    async def mood(self):
        """Generate text with a custom emoji from server"""
        # Retrieve a random item from custom emojis from the server
        # Make sure the emojis are unrestricted otherwise they will be ignored
        custom_emojis = [emoji for emoji in self.bot.get_all_emojis() if not emoji.roles]

        if not custom_emojis:
            return await self.bot.say((
                "Aww... "
                "There's no custom emojis I can express in this server. "
                "In that case my mood is :poop:"))

        # Retrieve random emoji retrieved from server and format it to be shown on chat.
        emoji_string = discord_commons.format_emoji(
            commons.get_random_item(custom_emojis))

        # Display on Discord
        await self.bot.say("Hai, my current mood is... " + emoji_string)
        await asyncio.sleep(1)
        await self.bot.say("...for now anyways. Ask me again later.")

    # [choose] command.
    @commands.command()
    async def choose(self, *args):
        """Choose one or more items asked"""
        items = [text.replace(',', '') for text in args if text.lower() != "or"]
        size = len(items)
        if size == 0:
            return await self.bot.say("There wasn't anything to choose from. :cry:")
        elif size == 1:
            return await self.bot.say(
                "Well... I guess {0} since that's the only option!".format(
                    str(items[0])))
        else:
            item_chosen = commons.get_random_item(items)
            if item_chosen == "me":
                item_chosen = "you"
            return await self.bot.say("I choose... {0}!".format(
                str(item_chosen)))

    # [goodbye] command. Logs the bot off discord if owner calls it;
    # otherwise, bot will simply say goodbye to the caller.
    # uses 'dad' variable in config.py
    @commands.command(pass_context=True)
    async def goodbye(self, ctx):
        """Sends a goodbye text; stops if host"""
        if config.dad not in ctx.message.author.name:
            return await self.bot.say("Oh! Goodbye, "
                                     + ctx.message.author.mention
                                     + "! See you again soon.")
        await self.bot.say("I'm logging off. Goodbye frineds!")
        await self.bot.close()

    # [poke] command. If entered a user who is not the sender nor the bot,
    # it will mention that the sender poked the user.
    # Otherwise, it will assume the sender is poking the bot.
    @commands.command(pass_context=True, aliases=['interact', 'hug', 'pet', 'pat'])
    async def poke(self, ctx, member: discord.Member = None):
        """ poke someone. Assumes itself if no mention.

            Can also use -interact, -hug, or -pet instead
        """
        action_dict = {
            'poke': "poking",
            'hug': "hugging",
            'pet': "petting",
            'pat': "patting",
            'interact': "interacting with"
        }
        source = ctx.message.author
        poking_bot = False if (member is not None and member != self.bot.user) else True
        poker_bot = True if (member is not None and member == source) else False
        if not poking_bot and poker_bot:
            await self.bot.say('I\'m {1} you, {0}!'
                               .format(source.mention,
                                       action_dict[ctx.invoked_with]))
        elif poking_bot:
            await self.bot.say('Hello, {0}! You are {1} me!'
                               .format(source.mention,
                                       action_dict[ctx.invoked_with]))
        else:
            await self.bot.say('Hey {0}, {1} is {2} you!'
                               .format(member.mention,
                                       source.mention,
                                       action_dict[ctx.invoked_with]))

    @commands.group(pass_context=True)
    async def ask(self, ctx):
        if ctx.invoked_subcommand is None:
            return await self.ask_math(ctx.message)

    @ask.command(pass_context=True)
    async def me(self, ctx):
        """Asks you a math question.

        Careful, you are timed!
        """
        await self.ask_math(ctx.message)

    async def ask_math(self, message):
        question, num_answer = commons.get_random_math_question()
        await self.bot.say(
            "Ok, {0}, what is {1}?".format(
                message.author.mention,
                question))
        try:
            reply_message = await self.bot.wait_for_message(
                author=message.author,
                channel=message.channel,
                timeout=20.0)
        except asyncio.TimeoutError:
            reply_message = None
            pass
        if reply_message is None:
            return await self.bot.say(
                "Oh, sorry, you took too long. Try again")
        message_text = reply_message.content
        reply = message_text
        num_input = None
        if message_text:
            try:
                reply = message_text.split(' ')[0]  # only look at first word
                num_input = Decimal(reply)
            except InvalidOperation:
                pass
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
        return await self.bot.say(bot_reply)


def setup(bot):
    bot.add_cog(fun(bot))
