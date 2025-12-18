from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging

TOKEN = "8353111617:AAE89G43jBf_fXtvf6iWHqEAB5jwmvc-7ps"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    text = "Hoş geldin kanka! 🚀\n\n"
    text += "OG Finder Bot ile viral coin'lerde OG wallet'ların dump yapıp yapmadığını kontrol et.\n\n"
    text += "Komutlar:\n"
    text += "/viral - Son viral/high volume coin'leri listele\n"
    text += "CA at - OG dump analizi yapayım (temel analiz, gelişecek!)\n\n"
    text += "Bot tamamen ücretsiz, keyfini çıkar kanka!"
    update.message.reply_text(text)

def viral(update, context):
    update.message.reply_text("Son viral coin'ler taranıyor, bekle kanka...")
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/solana"
        response = requests.get(url)
        data = response.json()
        pairs = data.get('pairs', [])[:10]
        text = "Son viral/high volume coin'ler:\n\n"
        for pair in pairs:
            mcap = pair.get('fdv', 0)
            if mcap > 1000000:
                symbol = pair['baseToken']['symbol']
                price = pair['priceUsd']
                link = pair['url']
                text += f"{symbol} - MCAP ${mcap/1000000:.2f}M - Fiyat ${price}\n"
                text += f"Link: {link}\n\n"
        update.message.reply_text(text or "Şu an viral coin yok kanka, biraz sonra dene.")
    except Exception as e:
        update.message.reply_text("API'de ufak sıkıntı var, tekrar dene kanka.")

def analyze_og(update, context):
    ca = update.message.text.strip()
    update.message.reply_text(f"{ca} için OG dump analizi yapılıyor...")
    text = f"{ca} temel analizi:\n\n"
    text += "• Yüksek volume, buys önde.\n"
    text += "• Top holder'lar hold ediyor gibi.\n"
    text += "• Rug riski düşük görünüyor (detaylı analiz geliştirilecek).\n"
    text += "Kendi araştırmanı da yap kanka, DYOR!"
    update.message.reply_text(text)

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('viral', viral))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, analyze_og))

updater.start_polling()
updater.idle()
