import environs
import platform

env = environs.Env()
env.read_env("./.env")

API_ID_1 = env.int('API_ID_1')
API_HASH_1 = env.str('API_HASH_1')
ADMIN_CHATID_1 = env.int('ADMIN_CHATID_1')
ADMIN_USERNAME_1 = env.str('ADMIN_USERNAME_1')

DB_NAME = env.str('DB_NAME')

ALERT_IN_UA_TOKEN = env.str('ALERT_IN_UA_TOKEN')
OPEN_WEATHER_TOKEN = env.str('OPEN_WEATHER_TOKEN')

#TOKEN_1 = env.str('TOKEN_1')
#CHANNEL_ID = env.int('CHANNEL_ID')

if platform.system() == "Windows":
    modules_repo_branch = "win-main"
elif platform.system() == "Linux":
    modules_repo_branch = "linux-main"
elif platform.system() == "Darwin":
    modules_repo_branch = "macos-main"
else:
    modules_repo_branch = "main"
