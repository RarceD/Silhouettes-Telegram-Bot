import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from private import KEY, stop_seconds
from Birthday_Data import Birthday_Data
from Request_Resources import Request_Resources
import time
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

birthdays = Birthday_Data()
birthdays.parse_file("birthday_input.json")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')

def jara_def(update: Update, context: CallbackContext) -> None:
    refresh_time = 5
    update.message.reply_text('Te va a felicitar tu puta madre')
    stop_seconds()
    update.message.reply_text('será el primer caso en el que le comáis los huevos a un bot')
    stop_seconds()
    update.message.reply_text('!Perra!')
    stop_seconds()
    update.message.reply_text('más perra y no naces')
    stop_seconds()
    update.message.reply_text('que te jodan: ')
    update.message.reply_text('Felicidades Jara')

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def b_command(context):
    # print(update.message.text)
    print("b_command")
    job = context.job
    # context.message.reply_text("Hola Bea :)")
    context.bot.send_message(job.context, text="Hola Bea: ")
    # Send a local cat:
    # context.bot.send_photo(update.message.chat_id, photo=open('data/cat.png', 'rb'))
    # Send a url:
    r = Request_Resources()
    context.bot.send_photo(job.context, r.obtein_cat_picture())

def stuff_function(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("TODO")

def alarm(context):
    # Send the alarm message
    job = context.job
    not_party = True
    birthdays_today = birthdays.check_if_birthday()
    if (birthdays_today != []):
        for b in birthdays_today:
            msg_telegram = "Es el cumpleaños de "
            msg_telegram += b
            msg_telegram += " que no se te olvide felicitarlo, hijo de p***"
            context.bot.send_message(job.context, text=msg_telegram)
            not_party = False
    if not_party:
        context.bot.send_message(
            job.context, text="Hoy no hay cumples a recordar")


def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        timer_info = str(context.args[1])
        print(timer_info)
        timer_info = timer_info[1:-1]
        print(timer_info)
        if due < 0:
            update.message.reply_text(
                'Al pasado no se me da bien ir no, de momento')
            return
        if timer_info == 'cats':
            job_removed = remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_repeating(
                b_command, due, context=chat_id, name=str(chat_id))
            text = 'Notificacione de gatos activadas'
            if job_removed:
                text += ' Old one was removed.'
            update.message.reply_text(text)
        else:
            job_removed = remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_repeating(
                alarm, due*60, context=chat_id, name=str(chat_id))
            text = 'Notificacione de cumpleaños activadas'
            if job_removed:
                text += ' Old one was removed.'
            update.message.reply_text(text)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def main():
    updater = Updater(KEY, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("B", stuff_function))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("jara", jara_def))
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
