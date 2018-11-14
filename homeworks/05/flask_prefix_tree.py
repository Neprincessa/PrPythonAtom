from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)


class PrefixTree:
    def __init__(self):
        self.root = [{}]
        self.amount = 0

    def add(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:  # проверка наличия текущей буквы в словаре
                wrk_dict = wrk_dict[0][i]  # обращаемся к словарю по ключу "i"
            else:
                if len(wrk_dict) == 1:  # если list состоит только из 1 словаря, т.о.слово ранее не записывалось
                    wrk_dict.append(0)
                wrk_dict[0][i] = [{}]  # записываем по ключу "i"  снова список с пустым словарем внутри
                wrk_dict = wrk_dict[0][i]  # переходим в свежезаписанный list
        if len(wrk_dict) == 1:  # если list состоит только из словаря, т.e. слово ранее не записывалось
            wrk_dict.append(1)
        else:
            wrk_dict[1] = wrk_dict[1] + 1
        self.amount += 1
        # TODO добавить строку

    def check(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]  # если буква-ключ есть, то углубляемся
            else:
                return False
        if wrk_dict[1] == True:
            return True
        return False
        # TODO проверить наличие строки

    def check_part(self, string):  # всегда проверят от начала
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        return True

    def show_tree(self):
        w = self.root
        s = ''
        for key in w[0]:
            print(self.recur(w, s, key))

    def recur(self, w, string, key):  # обход дерева
        string = string + key
        if len(list(w[0][key][0].keys())) == 0:  # если внутренний словарь пуст, значит это последняя буква слова
            return string
        else:
            w = w[0][key]  # иначе переходим по текущему ключу в его внутренний словарь
            for m in list(w[0].keys()):  # перебираем все ключи во внутреннем словаре
                return self.recur(w, string, m)
                # запустить цикл который будет засовывать сюда же все ключи из массива ключей

                def init_prefix_tree(filename):
    #TODO в данном методе загружаем данные из файла. Предположим вормат файла "Строка, чтобы положить в дерево" \t "json значение для ноды"  частота встречаемости


@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    #TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод

@app.route("/")
def hello():
    #TODO должна возвращатьс инструкция по работе с сервером
    return

if __name__ == "__main__":
    app.run()