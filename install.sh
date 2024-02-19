#!/bin/bash

# Отримуємо інформацію про систему
uname_output=$(uname -a)

# Стандартні змінні
ENV_FILE=.env
DB_DEFAULT_NAME=db.sqlite3

# Функція для виведення тексту кольором
print_color_text() {
    local text="$1"
    local color="$2"

    case "$color" in
        "black") echo -e "\e[30m${text}\e[0m" ;;
        "red") echo -e "\e[31m${text}\e[0m" ;;
        "green") echo -e "\e[32m${text}\e[0m" ;;
        "yellow") echo -e "\e[33m${text}\e[0m" ;;
        "blue") echo -e "\e[34m${text}\e[0m" ;;
        "magenta") echo -e "\e[35m${text}\e[0m" ;;
        "cyan") echo -e "\e[36m${text}\e[0m" ;;
        "white") echo -e "\e[37m${text}\e[0m" ;;
        *) echo "$text" ;;
    esac
}

# Функція для запиту вводу з підказкою та кольорованим текстом
prompt_input() {
    local prompt_text="$1"
    local color="$2"

    case "$color" in
        "black") local color_code="\e[30m" ;;
        "red") local color_code="\e[31m" ;;
        "green") local color_code="\e[32m" ;;
        "yellow") local color_code="\e[33m" ;;
        "blue") local color_code="\e[34m" ;;
        "magenta") local color_code="\e[35m" ;;
        "cyan") local color_code="\e[36m" ;;
        "white") local color_code="\e[37m" ;;
        *) local color_code="" ;;
    esac

    echo -e "${color_code}\e[1m${prompt_text}\e[0m" >&2
    read -p "> " -r value

    echo "$value"
}

# Перевірка, чи існує і заповнений файл .env
if [ -s "$ENV_FILE" ]; then
    print_color_text "$ENV_FILE вже існує та містить дані. Скрипт відмінено." "red"
    exit 1
fi

API_ID=$(prompt_input "Введіть API_ID" "cyan")
API_HASH=$(prompt_input "Введіть API_HASH" "cyan")
ADMIN_CHATID=$(prompt_input "Введіть ADMIN_CHATID" "cyan")
ADMIN_USERNAME=$(prompt_input "Введіть ADMIN_USERNAME" "cyan")
OPEN_AI=$(prompt_input "Введіть OPEN_AI" "cyan")

DB_NAME=$(prompt_input "Введіть DB_NAME (Натисніть Enter для стандартного імені db)" "cyan")
DB_NAME=${DB_NAME:-$DB_DEFAULT_NAME}

#TOKEN=$(prompt_input "Введіть TOKEN (Натисніть Enter, щоб пропустити)" "cyan")

ALERT_IN_UA_TOKEN=$(prompt_input "Введіть ALERT_IN_UA_TOKEN (Натисніть Enter, щоб пропустити)" "cyan")
OPEN_WEATHER_TOKEN=$(prompt_input "Введіть OPEN_WEATHER_TOKEN (Натисніть Enter, щоб пропустити)" "cyan")

echo "API_ID=$API_ID" > $ENV_FILE
echo "API_HASH=$API_HASH" >> $ENV_FILE
echo "ADMIN_CHATID=$ADMIN_CHATID" >> $ENV_FILE
echo "ADMIN_USERNAME=$ADMIN_USERNAME" >> $ENV_FILE
echo "OPEN_AI" >> $ENV_FILE
echo "DB_NAME=$DB_NAME" >> $ENV_FILE

#if [ -n "$TOKEN" ]; then
#    echo "TOKEN=$TOKEN" >> $ENV_FILE
#fi

if [ -n "$ALERT_IN_UA_TOKEN" ]; then
    echo "ALERT_IN_UA_TOKEN=$ALERT_IN_UA_TOKEN" >> $ENV_FILE
fi

if [ -n "$OPEN_WEATHER_TOKEN" ]; then
    echo "OPEN_WEATHER_TOKEN=$OPEN_WEATHER_TOKEN" >> $ENV_FILE
fi

print_color_text "Дані збережено в файлі $ENV_FILE" "cyan"
sleep 2
clear

# Визначаємо тип системи
print_color_text "Встановлення необхідних пакетів. " "cyan"
case $uname_output in
    *Android*)
        # Ваш код для Android
        pkg install -y python3 git clang ffmpeg wget libjpeg-turbo libcrypt ndk-sysroot zlib openssl
        ;;
    *Darwin*)
        # Ваш код для macOS
        sudo brew update
        sudo brew install python3 python3-venv nano wget zlib gnupg libtiff libwebp cairo
        ;;
    *Linux*)
        # Ваш код для Linux
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv nano wget ffmpeg gnupg zlib1g-dev
        ;;
    *)
        print_color_text "Не вдалося визначити тип системи." "red"
        exit 1
        ;;
esac
sleep 2
clear

# Загальний код для всіх систем
VENV_DIR="$(dirname "$(readlink -f "$0")")/venv"

# Перевірка версії Python та створення віртуального середовища
if ! command -v python3 &>/dev/null; then
    print_color_text "Python 3 не встановлено. Встановіть Python 3 і спробуйте знову." "red"
    exit 1
fi

python3 -c "import sys; exit(1) if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 6) else exit(0)"
if [ $? -ne 0 ]; then
    print_color_text "Вимагається версія Python 3.6 або вище. Встановіть сумісну версію та спробуйте знову." "red"
    exit 1
fi

# Перевірка віртуального середовища та створення, якщо його немає
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    print_color_text "Створення віртуального середовища в каталозі $VENV_DIR" "cyan"
    python3 -m venv "$VENV_DIR"
fi

# Активація віртуального середовища
source "$VENV_DIR/bin/activate"

# Встановлення залежностей
print_color_text "Встановлення залежностей..." "cyan"
pip install --upgrade pip
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_color_text "Помилка при встановленні залежностей. Перевірте для отримання додаткової інформації." "red"
    deactivate
    exit 1
fi

# Продовження виконання скрипта або вихід, в залежності від потреб
deactivate
print_color_text "Вихід." "cyan"
sleep 2
clear
