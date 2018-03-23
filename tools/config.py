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
sql_db = os.getenv('SQL_DB')
sql_host = os.getenv('SQL_HOST')
sql_username = os.getenv('SQL_USERNAME')
sql_password = os.getenv('SQL_PASSWORD')
reddit_client_id = os.getenv('REDDIT_APP')
reddit_secret_id = os.getenv('REDDIT_SECRET')
reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

bot_extensions = ["bot_query", "bot_fun"]
subreddits = {
    'thinking': "Thinking",
    'smug': "Smugs",
    'woof': "shiba",
    'cozy': "CozyPlaces",
    'yuri': "wholesomeyuri",
    'wakanda': "wholesomebpt",
    'slep': "AnimalsBeingSleepy",
    'kawaii': "awwnime",
    'aww': "Awww",
    'futaba': "churchoffutaba",
    'wafu': "headpats",
    'kyoko': "ultimatedetective",
    'uguu': "wholesomeanimemes",
    'chan': "wholesomegreentext",
    'wikihow': "disneyvacation",
    'wholesome': "wholesomememes",
    'butwhy': "mildlyinfuriating",
    'pikaboo': "PeepingPooch",
    'hellothere': "PrequelMemes",
    'javascript': "ProgrammerHumor"
}
