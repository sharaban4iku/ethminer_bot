import telebot
import requests

api_key = input("api key tg bot: ")
bot = telebot.TeleBot("5222691219:AAEjhmceZXqi9_EIURxroZqJI0LSiodClKU")


@bot.message_handler(commands=["start"])
def start(message):
    msg = bot.send_message(message.chat.id, "Введи свой кошелек: ")
    bot.register_next_step_handler(msg, wallet_bot)

def wallet_bot(message):
    global wallet
    wallet = message.text
    msg = bot.send_message(message.chat.id, "Супер! Я запомнил ваш кошель, теперь я готов к своей работе " + wallet)


@bot.message_handler(commands=["info"])
def get_active_worker(message):
    link = f"https://api.ethermine.org/miner/{wallet}/dashboard"
    a = requests.get(link).json()
    worker = a["data"]["workers"]
    hash = a["data"]["currentStatistics"]["reportedHashrate"]
    worker_count = a["data"]["currentStatistics"]["activeWorkers"]
    hash = hash / 1000000
    msg = bot.send_message(message.chat.id, f"Всего в работе {worker_count}\nАктивный hash: {hash}")


@bot.message_handler(commands=["balance"])
def balaca(message):
    link = f"https://api.ethermine.org/miner/{wallet}/dashboard"
    a = requests.get(link).json()
    balance = a["data"]["currentStatistics"]["unpaid"]
    balance = balance / 1000000000000000000
    b = requests.get("https://api.ethermine.org/poolStats").json()
    usd_price = b["data"]["price"]["usd"]
    usd_price = balance * usd_price
    msg = bot.send_message(message.chat.id, f"Баланс: {balance} eth | {usd_price}$")



bot.polling(none_stop=True, interval=0)
