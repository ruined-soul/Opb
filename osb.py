import logging
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your group management bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Get help\n/kick - Kick a user')

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for member in update.message.new_chat_members:
        await update.message.reply_text(f'Welcome {member.full_name}!')

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message:
        user_to_kick = update.message.reply_to_message.from_user
        try:
            await context.bot.ban_chat_member(update.message.chat_id, user_to_kick.id)
            await update.message.reply_text(f'User {user_to_kick.full_name} has been kicked.')
        except Exception as e:
            await update.message.reply_text(f'Failed to kick user: {e}')
    else:
        await update.message.reply_text('Reply to the user you want to kick.')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f'Update "{update}" caused error "{context.error}"')

async def main() -> None:
    # Your bot's token from BotFather
    TOKEN = '7322708595:AAExdf_Swh65yIOvHHbBRXrJXGJb15N1mSY'

    # Create the Application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("kick", kick))

    # Add message handler for new members
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # Log all errors
    application.add_error_handler(error_handler)

    # Start the Bot
    await application.start_polling()

    # Run the bot until you press Ctrl-C
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
