import logging
import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from private import KEY, stop_seconds, jokes
from Birthday_Data import Birthday_Data
from Request_Resources import Request_Resources
from mqtt_controller import mqtt_light_change, mqtt_read_status_lamp



# birthdays = Birthday_Data()
# birthdays.parse_file("birthday_input.json")
# print(times_)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')



def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def b_command(context):
    # print(update.message.text)
    # print("b_command")
    job = context.job
    # context.message.reply_text("Hola Bea :)")
    context.bot.send_message(job.context, text="Hola Bea: ")
    # Send a local cat:
    # context.bot.send_photo(update.message.chat_id, photo=open('data/cat.png', 'rb'))
    # Send a url:
    r = Request_Resources()
    context.bot.send_photo(job.context, r.obtein_cat_picture())
    
def shit_joke(update: Update, context: CallbackContext):
    # import json
    import random
    update.message.reply_text(jokes[random.randint(0,88)])
    # with open("birthday_input.json") as json_file:
    #     j = json.load(json_file)
    #     joke = j['jokes'][random.randint(0,60)]
    # update.message.reply_text(json.dumps(joke))

def stuff_function(update: Update, context: CallbackContext) -> None:
    job_removed = remove_job_if_exists(str(update.message.chat_id), context)
    update.message.reply_text("ya vale de gatos")


def alarm(context):
    # Send the alarm message
    job = context.job
    not_party = True
    # birthdays_today = birthdays.check_if_birthday()
    # if (birthdays_today != []):
    #     for b in birthdays_today:
    #         msg_telegram = "Es el cumpleaños de "
    #         msg_telegram += b
    #         msg_telegram += " que no se te olvide felicitarlo, hijo de p***"
    #         context.bot.send_message(job.context, text=msg_telegram)
    #         not_party = False
    # if not_party:
    #     context.bot.send_message(
    #         job.context, text="Hoy no hay cumples a recordar")


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
        # print(timer_info)
        timer_info = timer_info[1:-1]
        # print(timer_info)
        if due < 0:
            update.message.reply_text(
                'Al pasado no se me da bien ir no, de momento')
            return
        if timer_info == 'cats':
            job_removed = remove_job_if_exists(str(chat_id), context)
            t = datetime.time(9, 13, 00, 000000)
            # context.job_queue.run_daily(
                # b_command, t, days=tuple(range(7)), context=update)
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

def send_msg_mqtt_light(update: Update, context: CallbackContext) -> None:
    status = mqtt_light_change()
    response = "Canbricks: Action Light: " + str(status) + " - OK"
    update.message.reply_text(response)

def read_msg_mqtt(update: Update, context: CallbackContext) -> None:
    mqtt_response, raw_data = mqtt_read_status_lamp()
    response = "Canbricks: Read Status - OK: " + mqtt_response 
    update.message.reply_text(response)
    update.message.reply_text(raw_data)


def main():
    updater = Updater(KEY, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("B", stuff_function))
    dispatcher.add_handler(CommandHandler("set", set_timer))

    dispatcher.add_handler(CommandHandler("action", send_msg_mqtt_light))
    dispatcher.add_handler(CommandHandler("read", read_msg_mqtt))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
