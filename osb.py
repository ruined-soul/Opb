import logging
from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define commands
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your group management bot.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Get help\n/kick - Kick a user')

def welcome(update: Update, context: CallbackContext) -> None:
    for member in update.message.new_chat_members:
        update.message.reply_text(f'Welcome {member.full_name}!')

def kick(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user_to_kick = update.message.reply_to_message.from_user
        try:
            context.bot.kick_chat_member(update.message.chat_id, user_to_kick.id)
            update.message.reply_text(f'User {user_to_kick.full_name} has been kicked.')
        except Exception as e:
            update.message.reply_text(f'Failed to kick user: {e}')
    else:
        update.message.reply_text('Reply to the user you want to kick.')

def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main() -> None:
    # Your bot's token from BotFather
    TOKEN = '7322708595:AAExdf_Swh65yIOvHHbBRXrJXGJb15N1mSY'

    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("kick", kick))

    # Add message handler for new members
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
