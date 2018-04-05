from tools.config import *
from tools.otherapi import *
from tools.commons import get_random_int, get_random_item, get_suffled_list, get_random_math_question
from tools.discord_commons import format_emoji, check_mark_emoji, cross_mark_emoji, loading_emoji, evil_emoji
from tools.postgres_handler import KyonCoin, PokemonSearch, Token, Subreddit
from tools.meme_generator import generate_meme_from_text
from tools.dialogflow_handler import talk_ai


def update_subreddits():
    sub = Subreddit()
    sub.get_image_subreddits()
