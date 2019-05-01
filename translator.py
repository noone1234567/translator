from flask import Flask, request
import logging
import json
import random

#https://www.pythonanywhere.com/user/alwin123/files/home/alwin123
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    res['response']['buttons'] = [{'title': 'Помощь', 'hide': True},
                                  {'title': 'http://translate.yandex.ru/', 'hide': True, 'url': 'http://translate.yandex.ru/'}]
    logging.info(req['request']['command'])
    if req['session']['new']:
        res['response']['text'] = 'Это переводчик отдельных слов. Формат запроса: "Переведите (переведи) слово: *слово*". Переведено сервисом «Яндекс.Переводчик»'
        return

    if 'помощь' in req['request']['nlu']['tokens'] or 'помоги' in req['request']['nlu']['tokens']:
        res['response']['text'] = 'Это переводчик отдельных слов. Формат запроса: "Переведите (переведи) слово: *слово*". Переведено сервисом «Яндекс.Переводчик». Поехали!'
        return

    if req['request']['nlu']['tokens'][0] in ['переведи', 'переведите'] and len(req['request']['nlu']['tokens']) == 3 and req['request']['nlu']['tokens'][1] == 'слово':
        text = translate(req['request']['nlu']['tokens'][2])
        res['response']['text'] = 'Ошибка' if text is None else text

        return
    else:
         res['response']['text'] = 'Неправильный формат запроса. Попробуй ещё раз.'

    return


def translate(word):
    lang = "en"
    key = "trnsl.1.1.20190430T184245Z.d64c8ccf0b01b8d1.8221599076bea49f91cbc451af19b77fdcc703e2"
    req = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}".format(key, word, lang)

    response = requests.get(req)

    return response.json()['text'][0] if response else None


if __name__ == '__main__':
    app.run()

