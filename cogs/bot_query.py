# imports needed to run discord
import asyncio
from random import random, randint

import discord
from discord.ext import commands

# personal files
import tools


class query:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        # Only listen to messages from other people and none bots
        if message.author == self.bot.user or message.author.bot:
            return

        if random() < 0.01 and message.content.startswith("<:hmm"):
            return await self.random_reddit_image(message, 'Thinking')

    # [pkmn]
    @commands.command(pass_context=True)
    async def pkmn(self, ctx, *, pokemon="MissingNo"):
        """Looks up pokemon of the given name"""
        msg = await self.bot.say("Ok, let me look it up...")
        result_dict = tools.get_pokemon(pokemon)
        types = ", ".join((pkmn_type.title() for pkmn_type in result_dict['pkmn_types']))
        embed = discord.Embed(color=ctx.message.author.color)
        embed.add_field(name="Pokemon#{0}".format(result_dict['pkmn_id']),
                        value="{0}".format(result_dict['pkmn_name'].title()),
                        inline=True)
        embed.add_field(name="Type:", value=types, inline=True)
        embed.set_image(url=result_dict['pkmn_sprite'])
        embed.set_footer(text="courtesy of {0}".format(result_dict['source']))
        footer_text = "Pokemon found!"
        if result_dict.get('error', ""):
            footer_text = "Oops! | {0}".format(result_dict['error'])
        return await self.bot.edit_message(msg, new_content=footer_text, embed=embed)

    @commands.group(pass_context=True)
    async def say(self, ctx):
        """Repeats sender. If nothing, a quote.

         type '-help say' for more"""
        if ctx.invoked_subcommand is None:
            # if a phrase was passed, repeat what they said
            if ctx.subcommand_passed is not None:
                # remove the command from the phrase
                msg = ctx.message.content[len(ctx.prefix + ctx.invoked_with):].strip()
                embed = discord.Embed(color=ctx.message.author.color)
                embed.add_field(name="I say...", value=msg, inline=False)
                #  embed.set_image(url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                return await self.bot.say(embed=embed)

            # if no phrases passed, return a random quote
            result_dict = tools.get_random_quote()
            if not result_dict.get('error', ""):
                embed = discord.Embed(title="A quote for you...",
                                      url=result_dict['source'], color=ctx.message.author.color)
                embed.add_field(name="**{0}**".format(result_dict['author']),
                                value="{0}".format(result_dict['quote']), inline=False)
                return await self.bot.say(embed=embed)
            else:
                return await self.bot.say(
                    content="O-oh | Failed: {0}".format(result_dict['error']))

    @say.command(pass_context=True)
    async def woof(self, ctx):
        """Send a woof"""
        result_dict = tools.get_random_uk_doge()
        if not result_dict.get('error', ""):
            embed = discord.Embed(color=ctx.message.author.color)
            embed.set_image(url=result_dict['doge_url'])
            embed.set_footer(text="courtesy of {0}"
                             .format(result_dict['source']))
            return await self.bot.say(content=":dog: | Woof Woof!",
                                      embed=embed)
        else:
            return await self.bot.say(content=":dog: | Failed: {0}"
                                      .format(result_dict['error']))

    @commands.group(pass_context=True)
    async def define(self, ctx):
        """Generates an Oxford dictionary definition.

        type '-help define' for more.
        """
        if ctx.invoked_subcommand is None:
            # if a phrase was passed, find its english definition
            if ctx.subcommand_passed is not None:
                # retrieve only the first word after the command
                word = ctx.message.content.split(" ", maxsplit=1)[1]
                result_dict = tools.get_dictionary(word, tools.oxford_app_id, tools.oxford_app_key)
                if not result_dict.get('error', ""):
                    etymologies = '; '.join(result_dict['etymology'])
                    definitions = '\n'.join(("{0}. {1}".format(count, eng_def)
                                             for count, eng_def
                                             in enumerate(result_dict['definitions'], 1)))
                    embed = discord.Embed(color=ctx.message.author.color)
                    embed.add_field(name="Entry found for", value=word, inline=True)
                    if etymologies:
                        embed.add_field(name="Etymologies",
                                        value=etymologies, inline=True)
                    if definitions:
                        embed.add_field(name="Definition(s)",
                                        value=definitions, inline=False)
                    embed.set_thumbnail(url=self.bot.user.avatar_url)
                    embed.set_footer(text="Made possible by {0}".format(result_dict['source']))
                    return await self.bot.say(embed=embed)
                else:
                    return await self.bot.say("Oops! | {0}".format(result_dict['error']))
            return await self.bot.say("What should I define?")

    # [define jp]
    @define.command(pass_context=True)
    async def jp(self, ctx, *, words=""):
        """Looks up a japanese definition"""
        result_terms = tools.get_jisho_page(words)
        if not result_terms.get('error', ""):
            # There will be more than one term so we will prompt user
            term_list = result_terms.get('terms', [])
            header = "Enter a number for your desired term:"
            choices = '\t' + '\n\t'.join(
                [
                    "{0}. {1} ({2})".format(
                        number, term['writing'], term['reading']
                    ) for number, term in enumerate(term_list, 1)
                ]
            )
            time = 30.0
            footer = "::You have {} seconds to choose otherwise one will randomly be chosen.::".format(time)
            message_block = "Found the following terms :japanese_ogre: ```{}```".format(
                '\n'.join([header, choices, footer]))
            await self.bot.send_message(ctx.message.channel, message_block)

            # Wait for user to select a number from the given block, if invalid or 30 secs have passed
            # Retrieve a random item from the list
            try:
                reply_message = await self.bot.wait_for_message(
                    author=ctx.message.author,
                    channel=ctx.message.channel,
                    timeout=time)
            except asyncio.TimeoutError:
                reply_message = None
                pass

            result_index = None
            if reply_message and reply_message.content:
                try:
                    result_index = int(reply_message.content.split(' ')[0])
                    if result_index > len(term_list):
                        result_index = None
                        await self.bot.add_reaction(ctx.message, emoji=tools.cross_mark_emoji)
                except ValueError:
                    pass
            if not result_index or result_index < 1 or result_index > len(term_list):
                result_index = randint(1, len(term_list))
            elif reply_message:
                await self.bot.add_reaction(reply_message, emoji=tools.check_mark_emoji)
            result_dict = term_list[result_index - 1]

            # Create embed object
            embed = discord.Embed(color=ctx.message.author.color)

            # Loop through each senses definition grouped by type of speech
            senses = result_dict.get('senses', {})
            for sense_keys in senses.keys():
                definitions = '\n'.join("{0}. {1}".format(count, eng_def)
                                        for count, eng_def
                                        in enumerate(senses[sense_keys], 1))
                entry_header = "Type: {}".format(sense_keys if sense_keys else "Other")
                embed.add_field(name=entry_header,
                                value=definitions,
                                inline=False)

            # Set footer and thumbnail
            embed.set_footer(text="Made using {0}".format(result_terms['source']))
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await self.bot.send_message(ctx.message.channel,
                                        content="Results for {0} ({1})".format(
                                            result_dict['writing'],
                                            result_dict['reading']),
                                        embed=embed)
        else:
            await self.bot.send_message(ctx.message.channel, "Oops! | {0}".format(result_terms['error']))

    @commands.command(pass_context=True, aliases=list(tools.subreddits.keys()))
    async def reddit(self, ctx):
        """Gets an image from a subreddit.

        Could also use the following inside the brackets instead to call a
        specific subreddit
        """
        subreddit = tools.subreddits.get(ctx.invoked_with)
        if not subreddit:
            subreddit = tools.get_random_item(list(tools.subreddits.values()))
        return await self.random_reddit_image(ctx.message, subreddit)

    async def random_reddit_image(self, message, subreddit: str = 'Thinking'):
        img_dict = tools.get_subreddit_image_list(subreddit)
        if not img_dict.get('error'):
            img_item = tools.get_random_item(img_dict.get('img_list', []))
            if img_item:
                embed = discord.Embed(color=message.author.color)
                embed.set_image(url=img_item)
                return await self.bot.send_message(message.channel, embed=embed)
            else:
                return await self.bot.send_message(message.channel,
                                                   ":thinking: | Couldn\'t find an image in this subreddit.")
        return await self.bot.send_message(message.channel,
                                           ":thinking: | {0}".format(img_dict.get('error')))


def setup(bot):
    bot.add_cog(query(bot))
