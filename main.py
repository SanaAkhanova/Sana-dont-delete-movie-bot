import telebot
from telebot import types
import requests, bs4
import flask

appname = 'sana-dont-delet-move-bot'


link = 'https://filmix.co/'

token = '1519585389:AAFplChhTPvZtxXqJbmxNtwhqYiUO5fJxQY'
server = flask.Flask(__name__)
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    k = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    k.add(*[types.KeyboardButton(name) for name in ['Комедии',
                                                    'Боевики',
                                                    'Ужасы',
                                                    'Аниме',
                                                    'Документальные',
                                                    'Детектив',
                                                    'Драмы',
                                                    'Фантастика',
                                                    'Музыка',
                                                    'Мистика',
                                                    'Триллеры']])
                                                    
                                                
    m = bot.send_message(message.chat.id, 'Фильм какого жанра вы хотели бы посмотреть?', reply_markup=k)
    bot.register_next_step_handler(m, movie)
    
    
@bot.message_handler(content_types=['text'])
def movie(message):
    global link
    if message.text == 'Комедии':
        link = link + 'komedia/'
    elif message.text == 'Боевики':
        link = link + 'boevik/'
    elif message.text == 'Ужасы':
        link = link + 'uzhasu/'
    elif message.text == 'Аниме':
        link = link + 'animes/'
    elif message.text == 'Документальные':
        link = link + 'dokumentalenyj/'
    elif message.text == 'Детектив':
        link = link + 'detektivy/'
    elif message.text == 'Драмы':
        link = link + 'drama/'
    elif message.text == 'Фантастика':
        link = link + 'fantastiks/'
    elif message.text == 'Музыка':
        link = link + 'music/'
     elif message.text == 'Мистика':
        link = link + 'mistika/'
     elif message.text == 'Триллеры':
        link = link + 'triller/'       
            
          
        
    parsing(message)

def parsing(message):
    global link
    data = requests.get(link)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    links = soup.findAll('a') #ищем все теги '<a>'
    for l in links:
        href = l.get('href')
        if href.endswith('.html'):
            bot.send_message(message.chat.id, href)


@server.route('/' + token, methods=['POST'])
def get_message():
     bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
     return "!", 200

@server.route('/', methods=["GET"])
def index():
     bot.remove_webhook()
     bot.set_webhook(url=f"https://{appname}.herokuapp.com/{token}")
     return "Hello from Heroku!", 200
     

if __name__ == "__main__":
     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

#bot.polling(none_stop=True)
