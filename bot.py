from pyrogram import Client, filters
import subprocess
bot = Client(
    "myfirs",
    api_id=17983098,
    api_hash="ee28199396e0925f1f44d945ac174f64",
    bot_token="5782497998:AAGQaYV5w_Rw1ZSBhApXgV763_g8wf_PZEw"
)
@bot.on_message(filters.command('start') & filters.private)
def command1(bot,message):
    bot.send_message(message.chat.id, " السلام عليكم أنا بوت تفريغ صوتيات , فقط أرسل الصوتية هنا ")
    
@bot.on_message(filters.private & filters.incoming & filters.audio )
def _telegram_file(client, message):
  user_id = message.from_user.id
  sent_message = message.reply_text('جار التفريغ', quote=True)
  file = message.audio
  file_path = message.download(file_name="entry")

    # Execute speech.py script with entry file
  subprocess.call(['python', 'speech.py', 'RK3ETXWBJQSMO262RXPAIXFSG6NH3QRH', "./downloads/entry" , 'transcription.txt'])
    # Upload transcription file to user
  with open('transcription.txt', 'rb') as f:
        bot.send_document(message.chat.id, f)

bot.run()
