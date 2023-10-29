#!/bin/bash

# Функція для виведення тексту кольором
print_color_text() {
    local text="$1"
    local color="$2"
    echo -e "${color}${text}\e[0m"
}

# Оновлення системи
clear
print_color_text "Оновлення системи..." "\e[36m"
sleep 1
clear
apt update && apt upgrade
sleep 1
clear

# Встановлення необхідних пакетів
print_color_text "Встановлення необхідних пакетів..." "\e[36m"
apt install python3 nano wget gnupg zlib libtiff libwebp libcairo
sleep 1

# Ініціалізація віртуальнлї среди Python
python3 -m venv venv
clear

# Інструкції для запуску
print_color_text "Впишіть свої данні в файлі .env який зараз відкриється: " "\e[36m"
sleep 5
cp example.env .env
nano .env
clear

print_color_text "Перед запуском юзербота ви повинні активувати віртуальне середовище Python: " "\e[36m"
sleep 1
print_color_text "source venv/bin/activate" "\e[91m"
sleep 2
print_color_text "Встановіть відповідні бібліотеки Python: " "\e[36m"
sleep 1
print_color_text "pip install -r requirements.txt" "\e[91m"
sleep 2
print_color_text "Для запуску юзебота введіть команду: " "\e[36m"
sleep 1
print_color_text "python3 main.py" "\e[91m"
