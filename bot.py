import requests
import json
import telebot

# Ganti dengan token bot Telegram Anda
TOKEN = "gantitoken" 
bot = telebot.TeleBot(TOKEN)

# URL endpoint PHP Anda
PHP_ENDPOINT = "https://msfile.me/bot.php"  # Ganti dengan URL endpoint PHP Anda
VALID_KEY = "msdigital"  # Key yang valid

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    Menangani pesan yang diterima dari pengguna dan mengirimkan respon dari endpoint PHP.
    """
    try:
        # Kirim permintaan ke endpoint PHP
        params = {
            "key": VALID_KEY,
            "pesan": message.text
        }
        response = requests.get(PHP_ENDPOINT, params=params)
        response.raise_for_status()  # Raise HTTPError untuk kesalahan HTTP

        # Parse respon JSON
        data = response.json()
        responses = data.get('response', [])

        # Kirim respon ke pengguna
        for resp in responses:
            bot.reply_to(message, resp)

    except requests.exceptions.RequestException as e:
        print(f"Error saat menghubungi endpoint PHP: {e}")
        bot.reply_to(message, "Maaf, terjadi kesalahan. Silakan coba lagi nanti.")
    except json.JSONDecodeError as e:
        print(f"Error saat parsing respon JSON: {e}")
        bot.reply_to(message, "Maaf, terjadi kesalahan. Silakan coba lagi nanti.")

# Mulai polling untuk pesan baru
bot.polling()
