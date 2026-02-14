import telebot
import requests
import os

# --- CONFIGURATION ---
# Railway par 'Variables' section mein ye keys daalna
TMDB_API_KEY = os.getenv("TMDB_API_KEY") 
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

def get_poster_url(query):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['results']:
            first_result = data['results'][0]
            if first_result.get('poster_path'):
                poster_path = first_result['poster_path']
                full_hd_url = f"https://image.tmdb.org/t/p/original{poster_path}"
                title = first_result.get('title') or first_result.get('name')
                return full_hd_url, title
        return None, None
    except:
        return None, None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✨ **Welcome to High Quality Poster Bot!**\n\n"
        "Just send me any Movie or Series name, and I will find the original quality poster for you.\n\n"
        "👤 **Owner:** @stoicmeta"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    movie_name = message.text
    bot.send_chat_action(message.chat.id, 'upload_photo')
    
    poster_url, title = get_poster_url(movie_name)
    
    if poster_url:
        caption = f"🎬 **Title:** {title}\n\n📤 **Quality:** Ultra HD (Original)\n👤 **Owner:** @stoicmeta"
        bot.send_photo(message.chat.id, poster_url, caption=caption, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Sorry, I couldn't find any poster for that name. Please check the spelling.")

print("Bot is running...")
bot.polling(none_stop=True)
