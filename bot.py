from telegram.ext import Updater, CommandHandler, Job
from github import Github

import datetime
import redis
import sys, getopt

def main(argv):
    if len(argv) != 3:
        print('Expected usage of script:')
        print('python3 bot.py redishost redispost redispassword')
        sys.exit(2)
    host, port, pwd = argv
    try:
        r = redis.StrictRedis(host=host, port=port, password=pwd)
        print(r.get('foo'))
    except Exception:
        print("Provided params are incorrect. Couldn't connect to Redis instance")
    

if __name__ == "__main__":
    main(sys.argv[1:])


prodrink = Github("").get_organization("prodrink")

chatid = -1

one_hour = datetime.timedelta(minutes = 4*60.0)

utc = datetime.timedelta(hours = 3)

def start(bot, update):
    if update.message.chat.id == chatid:
        update.message.reply_text("Hello, Prodrink chat!")
    else:
        update.message.reply_text("Sosite!")

def hello(bot, update):
    if update.message.chat.id == chatid:
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))
    else:
        update.message.reply_text("Sosite!")

def callback_minute(bot, job):
    #bot.send_message(chat_id='-231093383', text='Sosite! Nachinau pull!')
    last_hour = datetime.datetime.now() - one_hour
    print(last_hour)
    for e in prodrink.get_events():
        if e.created_at > last_hour:
            bot.send_message(chat_id='-231093383',
                             text="{} for repo {} from {} at {} MSK".format(e.type, e.repo.name, e.actor.name, e.created_at + utc))

updater = Updater('')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))

queue = updater.job_queue

queue.run_repeating(callback_minute, interval=60.0*60.0, first=0)

updater.start_polling()
updater.idle()
