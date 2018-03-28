import discord


cross_mark_emoji = '\U0000274E'
check_mark_emoji = '\U00002705'
loading_emoji = '\U0001F501'
evil_emoji = '\U0001F608'


def format_emoji(emoji: discord.Emoji):
    return '<:{0}:{1}>'.format(emoji.name, emoji.id)
