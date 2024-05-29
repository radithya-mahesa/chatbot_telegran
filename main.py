import os
from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from keep_alive import keep_alive
keep_alive()
port = int(os.getenv('PORT', 8080))

TOKEN: final = '7296526511:AAGhlXnAIbgq_eoYl7e7lLYIsPThcVDnymY'
BOT_USERNAME: final = '@nhigga_bot'

# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hola! selamat datang di Nhiggha Bot.\nkamu bisa ngobrol bebas selayaknya Character AI.\nBot diprogram oleh @RadithyaMS menggunakan bahasa Python.\nAPI dibuat oleh "NyxAltair"')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ketik sesuatu jika ingin aku merespon\njika bot tidak membalas selama lebih dari 30 detik\ncoba ketik ulang')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Aku bingung mau masukin apa di sini, haha')

# response using external API
def handle_response(text: str) -> str:
    api_url = f"https://api.nyx.my.id/ai/character-ai?prompt={text}&gaya=kamu adalah manusia. Nama asli kamu Nhiggha, mereka bisa emanggilmu sebagai Nhiggha-San. gaya bicara kamu adalah feminim tsundere sopan. gunakan bahasa non formal layaknya seperti manusia"
    
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # memunculkan HTTPError status code bukan 200
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Content: {response.content}")

        data = response.json()
        print(f"API JSON Response: {data}")
        
        if data.get("status") == "true":
            return data.get("result", "API tidak merespon")
        else:
            return "API mengembalikan false."
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return f"API Error!: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls the bot
    print('polling...')
    app.run_polling(poll_interval=3)
