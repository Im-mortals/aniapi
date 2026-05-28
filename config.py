import os

# Telegram API credentials
APP_URL = os.getenv('APP_URL', '')
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# Parse comma-separated admins into a tuple of integers
_admins_env = os.getenv('ADMINS', '')
ADMINS = tuple(int(x.strip()) for x in _admins_env.split(',') if x.strip())

# File paths and messages
OWNER = os.getenv('OWNER', '')
REPO = os.getenv('REPO', '')
PATH = os.getenv('FILE_PATH', 'anime_data.txt')
MESSAGE = os.getenv('MESSAGE', '')
GIT_TOKEN = os.getenv('GIT_TOKEN', '')

# API keys for different platforms
RPMSHARE_API_KEY = os.getenv('RPMSHARE_API_KEY', '')
FILEMOON_API_KEY = os.getenv('FILEMOON_API_KEY', '')
ANIFLIX_USER_ID = os.getenv('ANIFLIX_USER_ID', '')

# URLs for fetching data
PLATFORMS = {
    'Filemoon': f"https://api.byse.sx/folder/list?key={FILEMOON_API_KEY}&fld_id=0",
    'RpmShare': f"https://rpmshare.com/api/folder/list?key={RPMSHARE_API_KEY}&fld_id=0",
    'Aniflix': f"https://aniflix.koyeb.app/api/folder_list?user_id={ANIFLIX_USER_ID}&page=1&page_size=200"
}

API_URLS = {
    'Kitsu': 'https://kitsu.io/api/edge/genres',
    'JikanV4': 'https://api.jikan.moe/v4/anime/1',
}

# Keep-alive settings
KEEP_ALIVE_INTERVAL = int(os.getenv('KEEP_ALIVE_INTERVAL', 120))
HEALTH_CHECK_PORT = int(os.getenv('HEALTH_CHECK_PORT', 8000))
