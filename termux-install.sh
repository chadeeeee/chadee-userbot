apt update && apt upgrade
apt install python3 nano wget gnupg zlib libtiff libwebp
python3 -m venv venv
cp example.env .env
nano .env
