import os
import config
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def log_print(text):
    with open('logs.txt', 'a') as logFile:
        logFile.writelines(f"{datetime.datetime.now()}     {text}\n")


def dateReverser(date):
    tempList = date.split(".")
    newDate = f"{tempList[2]}.{tempList[1]}.{tempList[0]}"
    return newDate


def txt_to_string(date):
    menuText = ""
    f = open(f'dailyMenus/{date}', 'r').readlines()

    for line in f:
        menuText += f"{line}"

    return menuText


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hacettepe Yemekhanecisi'ne hoşgeldin Hacettepeli!")

    # job_queue works in UTC time zone, it will be updated in the future versions of the bot!
    context.job_queue.run_daily(updateDatabase, time=datetime.time(hour=21, minute=0))
    log_print("updateDatabase() is in the job queue right now!")

    context.job_queue.run_daily(send_dailyMenu, time=datetime.time(hour=5, minute=0))
    log_print("send_dailyMenu() is in the job queue right now!")


def updateDatabase(context: CallbackContext):
    os.system('python3 main.py')
    log_print(f"Menu list has been scrapped from website")


def send_dailyMenu(context: CallbackContext):
    # Reformatting the date to search in database
    todaysDate = str(datetime.date.today()).replace("-", ".")
    if todaysDate[8] == '0':
        todaysDate = todaysDate[:8] + todaysDate[-1]

    # Fetching the menu as string from database
    menuText = txt_to_string(todaysDate)
    log_print(f"{todaysDate}'s menu has been fetched from database")

    context.bot.send_message(chat_id=config.chat_id, text=menuText)
    log_print("Daily menu has been sent!")


def main():
    updater = Updater(config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()
    log_print("Bot has been initialized")


if __name__ == '__main__':
    main()