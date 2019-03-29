import requests
import json

from flask import Flask
#from flask_sslify import SSLify
from flask import request
from flask import jsonify


app = Flask(__name__)
#sslify = SSLify(app)

proxies = {
    'https': 'http://142.93.128.158:8080',
}
URL = 'https://api.telegram.org/bot**********************************************/'

# функция отправки сообщения боту
def send_message(chat_id, text='Wait a second, please...'):
    url = URL + 'sendmessage?chat_id={}&text={}&parse_mode=markdown&disable_web_page_preview=false'.format(chat_id, text)
    answer = {'chat_id':chat_id, 'text':text}
    requests.post(url, json=answer, proxies=proxies)

def json_write(data):
    with open('updates.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# работаем с API погодного сайта и выдаем результат
def weather(location, day):
    if location == 'Москва':
        location = 'Moscow'
    # строим запрос к API сайта
    url = 'http://api.apixu.com/v1/forecast.json?key=********************************&q=%s&days=3' % (location)
    w = requests.get(url).json()
    # проверяем ошибку, если нет такого населенного пункта
    if 'error' in w and w['error']['code'] == 1006:
        return 'Такое место не найдено'
    #json_write(w)
    pic =  str(w['forecast']['forecastday'][day]['day']['condition']['icon'])
    tmax = str(w['forecast']['forecastday'][day]['day']['maxtemp_c'])
    tmin = str(w['forecast']['forecastday'][day]['day']['mintemp_c'])
    wind = (w['forecast']['forecastday'][day]['day']['maxwind_mph'])
    pic = 'http:'+pic
    wind = str(round(wind*0.44704, 1))
    if day == 0:
        sl = 'сегодня'
    if day == 1:
        sl = 'завтра'
    if day == 2:
        sl = 'послезавтра'
    answer = sl+''':
                Tmax= '''+tmax+''' C
                Tmin= '''+tmin+''' C
                Ветер: '''+wind+''' м/с'''+'[.]('+pic+')'
    return answer

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        for i in range(3):
            send_message(chat_id, text=weather(message, i))
        return jsonify(r)
    return '<h1>Hello, I am MeteoBot</h1>'

if __name__ == '__main__':
    app.run()

