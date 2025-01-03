from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, handle_contact, handle_admin_command

def main():
    application = Application.builder().token("8003742610:AAGqhdFyBxZYTtC3Two7Ymklip5CxRmKyh0").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.TEXT, handle_admin_command))
    application.run_polling()

if __name__ == "__main__":
    main()
