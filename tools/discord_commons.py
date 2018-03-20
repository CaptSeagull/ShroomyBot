import discord


def format_emoji(emoji: discord.Emoji):
    return '<:{0}:{1}>'.format(emoji.name, emoji.id)
