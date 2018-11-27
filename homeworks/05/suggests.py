import pandas as pd
from flask import Flask, json, jsonify
# -*- coding: utf-8 -*-



class TrieNode(object):

    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.word_finished = False


def add(root, word: str):
    word = word.lower().replace('ё', 'е')
    node = root
    for char in word:
        found_in_child = False
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                break
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            node = new_node
    node.word_finished = True


def prefix_descent(root, prefix: str):
    node = root
    # if prefix == '':
    # return False
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
        if char_not_found:
            return False
    return node


def display(node, string, level, list_of_strings):
    if node.word_finished:
        res_string = ''.join(string)
        list_of_strings.append(res_string)
    else:
        for child in node.children:
            string.insert(level, child.char)
            display(child, string.copy(), level + 1, list_of_strings)
            string.pop()


def make_suggestions(root, prefix):
    prefix = prefix.lower()
    node = prefix_descent(root, prefix)
    list_of_strings = []
    string = []
    if type(node) == bool:
        list_of_strings.append(prefix)
    else:
        display(node, string, 0, list_of_strings)
        for i in range(len(list_of_strings)):
            list_of_strings[i] = prefix + list_of_strings[i]
    return list_of_strings


root = TrieNode('*')


# ТОП-250 Кинопоиска
movie_list = pd.read_csv('top.csv', names=['movies'])

for i in movie_list['movies']:
    add(root, i.replace('\xa0', ' '))

# новые фильмы 2018
top2018 = pd.read_csv('best2018.csv', names=['movies'])

for i in top2018['movies']:
    add(root, i)

# ТОП 2017 года
top2017 = pd.read_csv('best2017.csv', names=['movies'])

for i in top2017['movies']:
    add(root, i)
# ТОП 2016 года
top2016 = pd.read_csv('best2016.csv', names=['movies'])

for i in top2016['movies']:
    add(root, i)
# ТОП 2015 года
top2015 = pd.read_csv('best2015.csv', names=['movies'])

for i in top2015['movies']:
    add(root, i)

# ТОП 2014 года
top2014 = pd.read_csv('best2014.csv', names=['movies'])

for i in top2014['movies']:
    add(root, i)

# ТОП 2013 года
top2013 = pd.read_csv('best2013.csv', names=['movies'])

for i in top2013['movies']:
    add(root, i)

# ТОП 2012 года
top2012 = pd.read_csv('best2012.csv', names=['movies'])

for i in top2012['movies']:
    add(root, i)

# ТОП 2011 года
top2011 = pd.read_csv('best2011.csv', names=['movies'])

for i in top2011['movies']:
    add(root, i)

# ТОП 2010 года
top2010 = pd.read_csv('best2010.csv', names=['movies'])

for i in top2010['movies']:
    add(root, i)

# ТОП 2009 года
top2009 = pd.read_csv('best2009.csv', names=['movies'])

for i in top2009['movies']:
    add(root, i)

# ТОП 2010-ых годов
top2010s = pd.read_csv('best2010s.csv', names=['movies'])

for i in top2010s['movies']:
    add(root, i)

# ТОП 2000-ых годов
top2000s = pd.read_csv('best2000s.csv', names=['movies'])

for i in top2000s['movies']:
    add(root, i)

# ТОП 1990-ых годов
top1990s = pd.read_csv('best1990s.csv', names=['movies'])

for i in top1990s['movies']:
    add(root, i)

# ТОП 1980-ых годов
top1980s = pd.read_csv('best1980s.csv', names=['movies'])

for i in top1980s['movies']:
    add(root, i)

# ТОП 1970-ых годов
top1970s = pd.read_csv('best1970s.csv', names=['movies'])

for i in top1970s['movies']:
    add(root, i)

# ТОП 1960-ых годов
top1960s = pd.read_csv('best1960s.csv', names=['movies'])

for i in top1960s['movies']:
    add(root, i)

# Oscar winners page 1
oscar1 = pd.read_csv('oscar1.csv', names=['movies'])

for i in oscar1['movies']:
    add(root, i)

# Oscar winners page 2
oscar2 = pd.read_csv('oscar2.csv', names=['movies'])

for i in oscar2['movies']:
    add(root, i)


#print(make_suggestions(root, 'при'))
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello():
    return 'start to type a name of the movie and get suggestions'


@app.route('/get_suggest/<prefix>', methods=['GET'])
def suggestions(prefix):
    suggest = make_suggestions(root, prefix)
    sug_string = ''
    for i in suggest:
        sug_string += i + '<br/>'
    return json.dumps(sug_string[:-1])


if __name__ == "__main__":
    app.run()