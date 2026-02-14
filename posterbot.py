import telebot
import requests
import os

# --- CONFIGURATION ---
# Railway Variables se keys fetch hongi
TMDB_API_KEY = os.getenv("TMDB_API_KEY") 
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

def get_poster_url(query):
    # include_adult=true aur language=en-US add kiya hai better results ke liye
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}&include_adult=true&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('results'):
            # Loop through results to find the first valid poster
            for result in data['results']:
                if result.get('poster_path'):
                    poster_path = result['poster_path']
                    # 'original' for Full Quality
                    full_hd_url = f"https://image.tmdb.org/t/p/original{poster_path}"
                    
                    # Title for Movies, Name for TV Series
                    title = result.get('title') or result.get('name')
                    return full_hd_url, title
        return None, None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✨ **Welcome to High Quality Poster Bot!**\n\n"
        "Send me any Movie or Web Series name (e.g., Dangal, Mirzapur, Avengers).\n\n"
        "👤 **Owner:** @stoicmeta"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text
    bot.send_chat_action(message.chat.id, 'upload_photo')
    
    poster_url, title = get_poster_url(query)
    
    if poster_url:
        caption = f"🎬 **Title:** {title}\n\n📤 **Quality:** Ultra HD (Original)\n👤 **Owner:** @stoicmeta"
        bot.send_photo(message.chat.id, poster_url, caption=caption, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Sorry, I couldn't find any poster for that name. Try adding the release year (e.g., Dangal 2016).")

print("Bot is running perfectly...")
bot.polling(none_stop=True)
