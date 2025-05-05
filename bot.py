import telebot
import requests
import openai

# =============== ВСТАВЬ СЮДА СВОИ ТОКЕНЫ ===================
TELEGRAM_TOKEN = '7753608741:AAGuR4R7wwwPKLgViJ-_nwnBLVk-FJ4r7KQ'
OPENAI_API_KEY = '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'
WEATHER_API_KEY = 'd7e728fd470cf320b445cd02e20d135f'
YOUTUBE_API_KEY = 'AIzaSyB3b6v9KDVlzjZNK63hcWfXcREULQ9e1n0'
# ===========================================================

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Погода
def get_weather(city='Moscow'):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    response = requests.get(url)
    data = response.json()
    if data.get('cod') != 200:
        return 'Не удалось получить погоду. Попробуйте позже.'
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    wind = data['wind']['speed']
    return f'В {city} сейчас {temp}°C, {desc}, ветер {wind} м/с.'

# YouTube
def search_youtube(query):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={YOUTUBE_API_KEY}&type=video'
    response = requests.get(url)
    data = response.json()
    items = data.get('items')
    if not items:
        return 'Видео не найдено.'
    video_id = items[0]['id']['videoId']
    title = items[0]['snippet']['title']
    return f'{title}\nhttps://www.youtube.com/watch?v={video_id}'

# ChatGPT
def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": question}],
            max_tokens=150,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f'Ошибка ChatGPT: {e}'

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    text = ("Привет! Я многофункциональный бот!\n\n"
            "Вот что я умею:\n"
            "/weather — Узнать погоду в Москве\n"
            "/youtube [запрос] — Найти видео на YouTube\n"
            "/ask [вопрос] — Задать вопрос ChatGPT\n")
    bot.send_message(message.chat.id, text)

# Команда /weather
@bot.message_handler(commands=['weather'])
def weather(message):
    weather_info = get_weather()
    bot.send_message(message.chat.id, f'Погода сейчас:\n{weather_info}')

# Команда /youtube
@bot.message_handler(commands=['youtube'])
def youtube(message):
    query = message.text.replace('/youtube', '').strip()
    if not query:
        bot.send_message(message.chat.id, 'Напиши запрос после команды, например: /youtube котики')
    else:
        result = search_youtube(query)
        bot.send_message(message.chat.id, result)

# Команда /ask
@bot.message_handler(commands=['ask'])
def ask(message):
    question = message.text.replace('/ask', '').strip()
    if not question:
        bot.send_message(message.chat.id, 'Напиши вопрос после команды, например: /ask Кто такой Ньютон?')
    else:
        answer = ask_gpt(question)
        bot.send_message(message.chat.id, answer)

# Ответ на любое сообщение (если написали "привет")
@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Чем могу помочь? Введи /start чтобы узнать команды.')
    else:
        bot.send_message(message.chat.id, 'Я пока не знаю такой команды. Введи /start чтобы посмотреть мои возможности.')

# Запуск бота
bot.polling(none_stop=True)

