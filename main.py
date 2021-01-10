import logging
from private import KEY
from Birthday_Data import Birthday_Data

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def b_command(update: Update, context: CallbackContext) -> None:
    print(update.message.text)
    update.message.reply_text("Hola Bea :)")
    context.bot.send_photo(update.message.chat_id, photo=open('data/cat.png', 'rb'))

def alarm(context):
    # Send the alarm message
    job = context.job
    birthdays_today = birthdays.check_if_birthday()
    if (birthdays_today != []):
        for b in birthdays_today:
            msg_telegram = "Es el cumpleaños de "
            msg_telegram += b
            msg_telegram += " que no se te olvide felicitarlo, hijo de p***"
            context.bot.send_message(job.context, text=msg_telegram)


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
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(
            alarm, due, context=chat_id, name=str(chat_id))

        text = 'Notificacione de cumpleaños activadas'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(KEY, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("B", b_command))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))
 
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
