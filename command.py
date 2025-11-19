import telebot

# === CONFIG ===
BOT_TOKEN = "8488169985:AAFZCSr2jG2Z9Xxh6AGrKD0L44rZmkXHfCs"  # replace with your Telegram bot token
bot = telebot.TeleBot(BOT_TOKEN)

# Temporary storage for user inputs
user_data = {}

# === Start Command ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hi! welcome to command genrator - by Fire drop ✓ Let's generate your command.\nPlease enter your username:")
    user_data[message.chat.id] = {'step': 'username'}

# === Message Handler ===
@bot.message_handler(func=lambda msg: True)
def collect_data(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.reply_to(message, "Please start with /start")
        return

    step = user_data[chat_id].get('step')

    if step == 'username':
        user_data[chat_id]['username'] = message.text
        user_data[chat_id]['step'] = 'password'
        bot.reply_to(message, "Enter password:")

    elif step == 'password':
        user_data[chat_id]['password'] = message.text
        user_data[chat_id]['step'] = 'target'
        bot.reply_to(message, "Enter target:")

    elif step == 'target':
        user_data[chat_id]['target'] = message.text
        user_data[chat_id]['step'] = 'reasons'
        bot.reply_to(message, "Enter reasons (comma-separated):")

    elif step == 'reasons':
        user_data[chat_id]['reasons'] = message.text
        user_data[chat_id]['step'] = 'storage'
        bot.reply_to(message, "Enter storage-state:")

    elif step == 'storage':
        user_data[chat_id]['storage'] = message.text
        # All data collected
        send_final_command(chat_id)
        del user_data[chat_id]  # reset for next use

def send_final_command(chat_id):
    data = user_data[chat_id]
    command = f"""python3 rep.py \\
  --username "{data['username']}" \\
  --password "{data['password']}" \\
  --target "{data['target']}" \\
  --reasons "{data['reasons']}" \\
  --storage-state "{data['storage']}" \\
  --headless True"""
    
    bot.send_message(chat_id, "✅ Your generated command:\n\n" + f"```\n{command}\n```", parse_mode="Markdown")

# === Run Bot ===
print("🤖 Bot is running...")
bot.infinity_polling()