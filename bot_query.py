import asyncio

# imports needed to run discord
import discord
from discord.ext import commands

# personal files
import config
import otherapi


class BotQuery:
    def __init__(self, bot):
        self.bot = bot

    # [pkmn]
    @commands.command()
    async def pkmn(self, *, pokemon="MissingNo"):
        """Looks up pokemon of the given name"""
        msg = await self.bot.say("Ok, let me look it up...")
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
                embed = discord.Embed(color=0x2b9b29)
                embed.add_field(name="I say...", value=msg, inline=False)
                embed.set_image(url=("https://cdn.discordapp.com/"
                                     "emojis/401429201976295424.png"))
                return await self.bot.say(embed=embed)

            # if no phrases passed, return a random quote
            result_dict = otherapi.get_random_quote()
            if not result_dict.get('error', ""):
                embed = discord.Embed(title="A quote for you...",
                                      url=result_dict['source'], color=0x2b9b29)
                embed.add_field(name="**{0}**".format(result_dict['author']),
                                value="{0}".format(result_dict['quote']), inline=False)
                return await self.bot.say(embed=embed)
            else:
                return await self.bot.say(
                    content="O-oh | Failed: {0}".format(result_dict['error']))

    @say.command()
    async def woof(self):
        """Send a woof"""
        result_dict = otherapi.get_random_uk_doge()
        if not result_dict.get('error', ""):
            embed = discord.Embed(color=0x2b9b29)
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
                word = ctx.message.content.split(" ")[1]
                result_dict = otherapi.get_dictionary(word, config.oxford_app_id, config.oxford_app_key)
                if not result_dict.get('error', ""):
                    etymologies = '; '.join(result_dict['etymology'])
                    definitions = '\n'.join(("{0}. {1}".format(count, eng_def)
                                             for count, eng_def
                                             in enumerate(result_dict['definitions'], 1)))
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
                    return await self.bot.say(embed=embed)
                else:
                    return await self.bot.say("Oops! | {0}".format(result_dict['error']))
            return await self.bot.say("What should I define?")

    # [define jp]
    @define.command()
    async def jp(self, *, words=""):
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
            await self.bot.say(embed=embed)
        else:
            await self.bot.say("Oops! | {0}".format(result_dict['error']))


def setup(bot):
    bot.add_cog(BotQuery(bot))
