import asyncio
import logging
from pycoingecko import CoinGeckoAPI
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace with your actual values
BOT_TOKEN = "8122500988:AAGolgFcZMURXJDXa4rxtVcu8QtkIIaqIrs"
CHAT_ID = 7703835442

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

cg = CoinGeckoAPI()

async def send_update(app: Application):
    try:
        trending = cg.get_search_trending()
        coins = trending.get('coins', [])[:3]

        message = "🚀 <b>Trending Crypto Alert</b>\n\n"
        for i, coin_data in enumerate(coins, 1):
            coin = coin_data['item']
            message += f"{i}. {coin['name']} ({coin['symbol'].upper()})\n"

        message += "\n📊 Stay updated with Dante Bot!"
        await app.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')
        logging.info("Update sent successfully")
    except Exception as e:
        logging.error(f"Error sending update: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Dante Bot is running and will send crypto updates every 15 minutes.")

async def schedule_updates(app: Application):
    while True:
        await send_update(app)
        await asyncio.sleep(900)  # 15 minutes

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))

    async def on_startup(_):
        asyncio.create_task(schedule_updates(app))

    app.post_init = on_startup

    app.run_polling()

if __name__ == "__main__":
    main()
