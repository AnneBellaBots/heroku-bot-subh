import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# NOTE: Replace 'YOUR_BOT_TOKEN' with your actual bot token if the provided one is invalid or expired.
TOKEN = '8277646165:AAGXWTfJgNO8ZNoVFUanlzgJxYJSLsmejEw'

# Regex to find all sequences of digits (numbers)
NUMBER_REGEX = r'\d+'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    await update.message.reply_text(
        "👋 Hello! Send me any message with numbers, and I'll send each one back in a separate message bubble."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processes incoming text messages.
    1. Extracts all numbers.
    2. Sends each number individually.
    3. Sends a milestone message after every 100th number.
    4. Sends a final 'Task Complete' message.
    """
    if update.message and update.message.text:
        text = update.message.text
        chat_id = update.effective_chat.id
        
        # Find all numbers in the message
        all_numbers = re.findall(NUMBER_REGEX, text)
        
        if all_numbers:
            total_numbers = len(all_numbers)
            logging.info(f"Found {total_numbers} numbers. Sending separate messages to chat_id: {chat_id}")
            
            await update.message.reply_text(f"✅ Found **{total_numbers}** numbers. Sending them now...")
            
            # Iterate through the numbers with their 0-based index
            for i, number in enumerate(all_numbers):
                # The count of the current number (1-based)
                current_count = i + 1 
                
                # Send the number
                # We use context.bot.send_message here instead of update.message.reply_text 
                # to ensure each number gets its own new message bubble.
                await context.bot.send_message(chat_id=chat_id, text=number)

                # Check if the current number is a multiple of 100
                if current_count % 100 == 0:
                    milestone_message = (
                        f"--- 💯 Milestone: * {current_count} * numbers sent! ---"
                    )
                    # Send the milestone message
                    await context.bot.send_message(chat_id=chat_id, text=milestone_message)
            
            # --- FINAL COMPLETION MESSAGE ---
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"🎉 * Task Complete! * All {total_numbers} numbers have been sent."
            )
            logging.info(f"Finished sending all numbers to {chat_id}")
            
        else:
            # If no numbers are found
            await update.message.reply_text("❌ No numbers found in your message. Send me something with digits!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Logs errors caused by Updates."""
    logging.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Starts the bot."""
    # Build the application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    # MessageHandler handles all text messages that are NOT commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    print("Bot is starting... Press Ctrl+C to stop.")
    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
