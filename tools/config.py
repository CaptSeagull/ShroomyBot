import os

app_id = os.getenv('BOT_TOKEN')
owner_id = os.getenv('OWNER_ID')
version = os.getenv('VERSION')
prefix = os.getenv('PREFIX')
dad = os.getenv('DAD')
game = os.getenv('GAME')
oxford_app_id = os.getenv('OX_APP')
oxford_app_key = os.getenv('OX_KEY')
channel_spam_id = os.getenv('CHANNEL_ROOM')
reddit_client_id = os.getenv('REDDIT_APP')
reddit_secret_id = os.getenv('REDDIT_SECRET')
reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

bot_extensions = ["bot_query", "bot_fun"]
subreddits = {
    'thinking': "Thinking",
    'smug': "Smugs",
    'woof': "shiba"
}


def get_postgress_sql_url():
    """the url may get updated so use function to retrieve new value"""
    return os.environ['DATABASE_URL']
