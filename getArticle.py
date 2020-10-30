from telebot import TeleBot, types
import requests

API_TOKEN = '<TOKEN>'
bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello! Click /getArticle to get started on getting your free Medium Articles!')

@bot.message_handler(commands=['getArticle'])
def get_article(message):
    msg = bot.send_message(message.chat.id, 'To download the free article, please input a valid Medium URL.')
    bot.register_next_step_handler(msg, process_url)

def process_url(message):
    chat_id = message.chat.id
    url = message.text
    filename = url

    try: 
        response = requests.get(url)
        filename = url.split('/')[-1].split('-')
        del filename[-1]
        filename = ' '.join(filename)

        # print(filename)
        if response.status_code == 200 and 'medium.com' in url:
            bot.send_message(chat_id, 'Processing URL for download...')
            with open(filename+'.html', 'w', encoding="utf-8") as f:
                res = response.text.replace('<script>window.__GRAPHQL_URI__ = \"https://medium.com/_/graphql\"</script>', '')
                f.write(res)   
            
            doc = open(filename+'.html', 'rb')
            bot.send_document(chat_id, doc)
        else:
            bot.send_message(chat_id, 'Please enter a valid URL.')
    except:
        msg = bot.send_message(chat_id, 'Please enter a valid URL.')
        bot.register_next_step_handler(msg, process_url)

bot.polling(none_stop=True)
