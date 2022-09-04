import os
import telegram

from telegram.ext import MessageHandler, Filters
from telegram.ext import Dispatcher
from telegram.ext import InlineQueryHandler
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from huggingface_hub.inference_api import InferenceApi
from time import time

# warmRun = False


bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
# bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)
inference = InferenceApi(repo_id="arpanghoshal/EmoRoBERTa",
                         token=os.environ["API_KEY"])



def start(update: Update, context: CallbackContext):
    print(
        f"\\start request from user: {update.effective_user} in chat: {update.effective_chat}")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Add me to groups and type /emo followed by a sentence you wish to be analysed for its evoked emotions. Original model from https://huggingface.co/arpanghoshal/EmoRoBERTa. Contact @incomple for feedback and suggestions.")


def helpCommand(update: Update, context: CallbackContext):
    print(
        f"\\help request from user: {update.effective_user} in chat: {update.effective_chat}")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Add me to groups and type /emo followed by a sentence you wish to be analysed for its evoked emotions. Original model from https://huggingface.co/arpanghoshal/EmoRoBERTa. Contact @incomple for feedback and suggestions.")


def emoText(inputText):
    start = time()
    result = inference(inputs=inputText)
    end = time()
    msecTime = f"{int((end - start)*1000)} msec"
    result = result[0]
    finalStr = f"({msecTime}) Top 5 emotions for: '{inputText}' \n\n"
    counter = 0
    for d in result:
        finalStr += f"{d['label']}: {d['score']} \n"
        counter += 1
        if counter == 5:
            break
    return finalStr


def emo(update: Update, context: CallbackContext):
    # if not warmRun:
    #     warmRun = True
    #     context.bot.send_message(
    #         chat_id=update.effective_chat.id, text="Cold start; please wait a few minutes for me to warm up...")
    #     dispatcher.process_update(update)
    print(
        f"\\emo request from user: {update.effective_user} in chat: {update.effective_chat}")
    incoming_text = ' '.join(context.args)
    if not (incoming_text.strip()):
        incoming_text = "You gotta type something after the /emo command for me to analyse!"
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=incoming_text)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Running inference for '{incoming_text}' (May be slow if running from cold start); please wait...")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=emoText(incoming_text))


def inline_emo(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=3,
            title='emo',
            input_message_content=InputTextMessageContent(emoText(query))
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


def webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', helpCommand)
        dispatcher.add_handler(help_handler)

        emo_handler = CommandHandler('emo', emo)
        dispatcher.add_handler(emo_handler)

        inline_mock_handler = InlineQueryHandler(inline_emo)
        dispatcher.add_handler(inline_mock_handler)

        # unknown_handler = MessageHandler(Filters.command, unknown)
        # dispatcher.add_handler(unknown_handler)

        dispatcher.process_update(update)
    return "ok"
