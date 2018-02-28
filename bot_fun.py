import discord
from discord.ext import commands

# personal files
import config
import commons
import discord_commons


class BotFun:
    def __init__(self, bot):
        self.bot = bot

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
        await self.bot.sleep(1)
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
    @commands.command(pass_context=True, aliases=['interact', 'hug', 'pet'])
    async def poke(self, ctx, member: discord.Member = None):
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
        poking_bot = False if (member is not None and member != self.bot.user) else True
        if poking_bot:
            await self.bot.say('Hello, {0}! You are {1} me!'
                               .format(source.mention,
                                       action_dict[ctx.invoked_with]))
        else:
            await self.bot.say('Hey {0}, {1} is {2} you!'
                               .format(member.mention,
                                       source.mention,
                                       action_dict[ctx.invoked_with]))


def setup(bot):
    bot.add_cog(BotFun(bot))
