from flask import Flask, request
import requests
import json


def translate(word):
    lang = "en"
    key = "trnsl.1.1.20190430T184245Z.d64c8ccf0b01b8d1.8221599076bea49f91cbc451af19b77fdcc703e2" # мой ключ
    req = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}".format(key, word, lang)

    response = requests.get(req)

    return response.json()['text'][0] if response else None


if __name__ == '__main__':
    print(translate('коробка'))
