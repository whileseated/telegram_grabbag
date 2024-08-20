import logging
import feedparser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.error import NetworkError
import time

# Read the config file
with open('config.txt', 'r') as f:
    TOKEN, CHAT_ID, ALLOWED_USER_ID = [line.strip() for line in f.readlines()]

# Convert ALLOWED_USER_ID from string to int for comparison
ALLOWED_USER_ID = int(ALLOWED_USER_ID)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Global dictionary to temporarily store feed URLs before receiving nickname
pending_feeds = {}

def restricted(func):
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != ALLOWED_USER_ID:
            update.message.reply_text("I'm sorry, but this is not a publicly available RSS bot.")
            return  # Stop the execution of the function if user is not allowed
        return func(update, context, *args, **kwargs)
    return wrapped

def is_user_allowed(update):
    return update.message.from_user.id == ALLOWED_USER_ID

@restricted
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! I am your RSS feed bot. Send me an RSS URL to subscribe.')

def safe_send_message(bot, chat_id, text):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            bot.send_message(chat_id, text)
            break  # If send is successful, break out of the loop
        except NetworkError as e:
            logger.error(f"NetworkError occurred: {e}. Attempt {attempt + 1} of {max_retries}")
            time.sleep(5)  # Wait for 5 seconds before retrying

@restricted
def handle_message(update: Update, context: CallbackContext):
    if not is_user_allowed(update):
        return  # Exit if user is not allowed

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text.lower() == 'check':
        check_feeds(update, context)
    elif text.lower() == 'remove':
        show_remove_buttons(update, context)
    elif user_id in pending_feeds:
        # User is expected to send a nickname for the pending feed URL
        url = pending_feeds[user_id]
        latest_post_url = get_latest_post_url(url)
        add_feed_to_file(url, text, latest_post_url)
        del pending_feeds[user_id]
        update.message.reply_text(f"Feed added with nickname: {text}")
    else:
        # Assume the user is sending a new RSS feed URL
        pending_feeds[user_id] = text
        update.message.reply_text("Please send a nickname for this feed.")

def show_remove_buttons(update: Update, context: CallbackContext):
    keyboard = []
    with open("feeds.txt", "r") as file:
        for line in file:
            if not line.strip():
                continue
            _, nickname, _ = line.strip().split(',')
            keyboard.append([InlineKeyboardButton(nickname, callback_data=f"remove_{nickname}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a feed to remove:', reply_markup=reply_markup)

def get_latest_post_url(url):
    feed = feedparser.parse(url)
    return feed.entries[0].link if feed.entries else ""

def add_feed_to_file(url, nickname, latest_post_url):
    with open("feeds.txt", "a") as file:
        file.write(f"{url},{nickname},{latest_post_url}\n")

@restricted
def check_feeds(update: Update, context: CallbackContext):
    try:
        with open("feeds.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            found_new_posts = False

            for line in lines:
                if not line.strip():
                    continue  # Skip empty lines

                url, nickname, last_link = line.strip().split(',')
                feed = feedparser.parse(url)

                if feed.entries:
                    new_link = feed.entries[0].link
                    if new_link != last_link:
                        safe_send_message(context.bot, update.effective_chat.id, f"New post in {nickname}: {new_link}")
                        file.write(f"{url},{nickname},{new_link}\n")
                        found_new_posts = True
                    else:
                        file.write(line)
                else:
                    file.write(line)

            if not found_new_posts:
                safe_send_message(context.bot, update.effective_chat.id, "No new posts found in subscribed feeds.")

            file.truncate()
    except Exception as e:
        logger.error(f"An error occurred in check_feeds: {e}")
        safe_send_message(context.bot, update.effective_chat.id, "An error occurred while checking feeds.")

@restricted
def show_remove_buttons(update: Update, context: CallbackContext):
    keyboard = []
    with open("feeds.txt", "r") as file:
        for line in file:
            if not line.strip():
                continue
            _, nickname, _ = line.strip().split(',')
            keyboard.append([InlineKeyboardButton(nickname, callback_data=f"remove_{nickname}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a feed to remove:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Extract nickname from callback_data
    # Ensure that underscores in the nickname are preserved
    _, nickname_to_remove = query.data.split('remove_', 1)
    remove_feed_from_file(nickname_to_remove)
    query.edit_message_text(text=f"Feed removed: {nickname_to_remove}")

def remove_feed_from_file(nickname_to_remove):
    with open("feeds.txt", "r") as file:
        lines = file.readlines()
    with open("feeds.txt", "w") as file:
        for line in lines:
            _, nickname, _ = line.strip().split(',')
            if nickname != nickname_to_remove:
                file.write(line)

# Handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("check", check_feeds))
dispatcher.add_handler(CommandHandler("remove", show_remove_buttons))
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

# Start the bot
updater.start_polling()
updater.idle()
