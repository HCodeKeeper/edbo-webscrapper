import telebot
import boot
import localization

lang = "RU"
TOKEN = "1905627526:AAFH2dLAzvdCNq3KKpAFYclPhs2vWZQEsKA"


STATES = {
    "FIOTfilter_credits_by_docs" : 2,
   "filter_credits" : 1,
   "idle" : 0
}
STATE = STATES["idle"]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["filter"])
def request_filter(message):
    global STATE
    reply = localization.Filter.RU.tip
    STATE = STATES["filter_credits"]
    bot.reply_to(message, reply)


@bot.message_handler(commands=["filterFIOT_by_docs"])
def request_filter_by_docs(message):
    global STATE
    reply = localization.Filter.RU.tip
    STATE = STATES["FIOTfilter_credits_by_docs"]
    bot.reply_to(message, reply)


@bot.message_handler(commands=["help"])
def manual(message):
    bot.reply_to(message, localization.WelcomeMessage.Beta.RU.welcome_message)
    bot.reply_to(message, localization.BotReference.RU._list)


@bot.message_handler(content_types=["text"])
def redirect_reply(message):
    if STATE == STATES["filter_credits"]:
        get_filter_credits(message)
    elif STATE == STATES["FIOTfilter_credits_by_docs"]:
        get_filter_credits_by_docs(message)


@bot.message_handler(commands=["facultieslinks"])
def among_faculties_links(message):
    print("!")
    items = boot.config.tables.values
    for faculty in items:
        bot.reply_to(message, faculty)


def get_filter_credits(message):
    global STATE
    _message = validating_filter_credits(message)
    if _message:
        fio, site = _message
        bot.reply_to(message, localization.BotValid.RU.valid) 
        result = boot.api.run_filter(fio, site)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, localization.BotValid.RU.invalid) 
    STATE = STATES["idle"]


def get_filter_credits_by_docs(message):
    global STATE
    _message = validating_filter_credits(message)
    if _message:
        fio, site = _message
        bot.reply_to(message, localization.BotValid.RU.valid) 
        result = boot.api.run_filter_by_docs(fio, site)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, localization.BotValid.RU.invalid) 
    STATE = STATES["idle"]


def validating_filter_credits(message):
    print("filter")
    text = message.text
    if "," in text:
        count = text.count(",")
        if count == 1:
            fio, site = text.split(",")
            if "https://" in site:
                if " " in site:
                    site = site.replace(" ","")
            return [fio, site]
    return False


def run():
    bot.polling()


if __name__ == "__main__":
    run()
