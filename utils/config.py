from dotenv import load_dotenv
import os
import platform

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
ADMIN_CHATID = int(os.getenv('ADMIN_CHATID'))
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')

DB_NAME = os.getenv('DB_NAME')

ALERT_IN_UA_TOKEN = os.getenv('ALERT_IN_UA_TOKEN')
OPEN_WEATHER_TOKEN = os.getenv('OPEN_WEATHER_TOKEN')
OPEN_AI = os.getenv('OPEN_AI')
DETECT = os.getenv('DETECT')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_ID_SECRET = os.getenv('CLIENT_ID_SECRET')

if platform.system() == "Windows":
    modules_repo_branch = "win-main"
elif platform.system() == "Linux":
    modules_repo_branch = "linux-main"
elif platform.system() == "Darwin":
    modules_repo_branch = "macos-main"
else:
    modules_repo_branch = "main"
