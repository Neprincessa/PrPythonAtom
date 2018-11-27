from imdb import IMDb
import csv
import pandas as pd

# imbdObj = IMDb()
# top250 = imbdObj.get_top250_movies()
#
# # возвращает список из 250 лучшх фильмов
# # каждое значение списка - кортеж из названия, актеров и жанров
N = 250
# def get_movies():
#     movies = []
#     #  TODO: изменить 30 на 250
#     for i in range(0,N):
#         movie = top250[i]
#         imbdObj.update(movie, info = ['main'])
#         title = movie.get('title')
#         cast = list(map(lambda x: x['name'], movie.get('cast')))
#         #cast[i] = movie.get('cast')
#         #for j in range(len(cast[i])):
#         #    cast[i][j] = cast[i][j].get('name')
#         genres = movie.get('genres')
#         URL = imbdObj.get_imdbURL(movie) #URL for first result
#         movies.append((title, cast, genres, URL))
#     return movies
#
# # сохранение списка в .csv файл
# movies = get_movies()
# dataFrame = pd.DataFrame.from_records(movies, columns=['Title','Cast','Genres','URL'])
# dataFrame.to_csv('top250_movies.csv',index=False)

# чтение из .csv файла
reader = pd.read_csv('top250_movies.csv')

# берем все значениея, вызываем tolist() - получаем фактически то, что возвращает метод get_movies()
loadedMovies = reader.values.tolist()
# это обычный list уже, можно обращаться по индексу
# selectedMovie = loadedMovies[2]
# # может есть какой-то более умный способ по именованию полей в кортеже, на я такого не знаю
# # потому, на нулевом месте - название у нас было, на первом - актеры, на втором - жанры
# # исходя из этого - обращаться можно так же по индексу
# selectedMovieName = selectedMovie[0]
# selectedMovieActors = selectedMovie[1].split(',')
# selectedMovieGenres = selectedMovie[2].split(',')
# selectedMovieURL = selectedMovie[3]
#
# print(selectedMovieName)
# print(selectedMovieActors[0].replace('[', '').replace(']',''))
# print(len(selectedMovieActors))
# print(selectedMovieGenres[1].replace('[', '').replace(']',''))
# print(selectedMovieURL)

name_eng = [' '] * 250
movie_id = {}#[] * 250
cast = [0] * 100000
actorsBase = [0] * 100000
genresBase = [0] * 1000
genres = [0] * 1000


k = 0
z = 0

for i in range(N):
    #print('i')
    #print(i)
    selectedMovie = loadedMovies[i]
    name_eng[i] = selectedMovie[0]  # title
    cast[i] = selectedMovie[1].split(',')  # actors
    for j in range(len(cast[i])):
        cast[i][j] = cast[i][j].replace('[', '').replace(']', '')
    genres[i] = selectedMovie[2].split(',')  # genres
    for j in range(len(genres[i])):
        genres[i][j] = genres[i][j].replace('[', '').replace(']', '')

    #movie_id[i] = selectedMovie[3]  # url
    movie_id[name_eng[i]] = selectedMovie[3]  # url
    for j in range(len(cast[i])):
        actorsBase[k] = cast[i][j]  # записали всех подряд актеров
        k += 1

    for j in range(len(genres[i])):
        genresBase[z] = genres[i][j]
        z += 1

actorSet = set(actorsBase)
actorSet.remove(0)
#print(actorSet)
#print()

genresSet = set(genresBase)
genresSet.remove(0)
#print(genresSet)


def getIndexInSet(string, currentSet):
    resultIndex = 0
    for element in currentSet:
        if (string == element):
            return resultIndex
        resultIndex += 1

# фильм - вектор = берем фильм, смотрим его актерский состав:
# взяли одного актера нашли его индекс во множестве, поставили единичку на месте соответствующей координаты

filmVector = [[0] *( len(actorSet) + len(genresSet))for i in range(251)]
k = 0
filmRec = {}
namedFilms = {}

#build vectors
for i in range(0,N):
    movie = loadedMovies[i]
    currentCast = movie[1].split(',')
    for j in range(len(currentCast)):
        if (currentCast[j].replace('[', '').replace(']','') in actorSet):
            index = getIndexInSet(currentCast[j].replace('[', '').replace(']',''),actorSet)
            filmVector[i][index] = 1
    #filmRec[name_eng[i-1]] = filmVector[i-1]
    ###
    #k = len(filmVector) - len(cast[i-1]) +1;
    k = 0
    currentGenre = movie[2].split(',')
    for z in range(len(filmVector[i])-len(currentGenre)+1):
        if (k<len(currentGenre) and currentGenre[k].replace('[', '').replace(']','') in genresSet):
            index = getIndexInSet(currentGenre[k].replace('[', '').replace(']',''), genresSet)
            filmVector[i][z+index] = 1
        k += 1
    filmRec[movie[0]] = filmVector[i] #dictionary with titles and vectors

import math

def get_key(d, value):
    j = 0
    for k in d.keys():
        for v in d.values():
            if d[k] == value:
                return k

# build norma
#film = str(input())  # добавить функцию чтоб ввел название, а он находит номер фильма
#while (film < 0 or film > 250):
    #film = int(input())

#print('fd')
#print(film)
def get_norma(id):
    norma = {}
    # film = id
    index = id #getFilmIndex(film)
    currentFilm = filmVector[index]
    for i in range(1, N+1):
        if (i - 1 != index):
            sum = 0
            for j in range(1, len(actorSet)):
                sum += (filmVector[i - 1][j - 1] - currentFilm[j - 1]) * (filmVector[i - 1][j - 1] - currentFilm[j - 1])
            norma[get_key(filmRec, filmVector[i - 1])] = math.sqrt(sum)
        else:
            norma[get_key(filmRec, filmVector[i - 1])] = 800000
    return norma
#print("Norma")
#print(norma)

def getFilmIndex(string):
    for i in range(len(loadedMovies)):
        if (string == loadedMovies[i][0]):
            return i
#print(get_norma(getFilmIndex(film)))

top20Recom = ['']*20
resultTitles = ['']*250

#find 20 films
def get_recommendation_list(string):
    currentIndex = getFilmIndex(string)
    from operator import itemgetter
    curList = []
    curList = get_norma(currentIndex)

#TODO change N


    #print('start')
    #print(curList)

    for j in range(0, len(curList) - 1):
        # вложенный цикл сравнивает i-ый c i+1 -ым элементом и при необходимости меняет их местами
        # количество сравнений каждый раз уменьшается на величину j
        for i in range(0, len(curList) - j - 1):
            if curList[name_eng[i]] < curList[name_eng[i + 1]]:
                tmp = curList[name_eng[i+1]]
                curList[name_eng[i + 1]] = curList[name_eng[i]]
                curList[name_eng[i]] =  tmp
    #curList = sorted(curNorma.items(), key=itemgetter(1))
    # TODO вывод только 20 элементов

    endL = get_norma(currentIndex)

    tmpNorma = [0]*250
    for z in range(len(curList)):
        tmpNorma[z] = curList[name_eng[z]]

    for z in range(len(tmpNorma)):
        for g in range(len(endL)):
            if (tmpNorma[z] == endL[name_eng[g]]):
                resultTitles[z] = name_eng[g]

    k = len(curList) - 1
    j = 0
    for i in range(len(curList)):
        if (k >= len(curList) - 20 + 1):
            top20Recom[j] = resultTitles[k]
            k -= 1
            j += 1
    return top20Recom

#get_recommendation(film)

result = ['']*20
def getUrlArr(arr):
    #result = ['']*len(arr)
    j = 0
    cur =['']*20
    for i in range(len(arr)):
        cur[j] = movie_id[arr[i]]
        j += 1
    tmp = set(cur)
    if ('' in tmp):
        tmp.remove('')
    result = list(tmp)
    return result

resultSet = set()
def get_recom_set(string):
    tmp = set(get_recommendation_list(string))
    if ('' in tmp):
        tmp.remove('')
    resultSet = list(tmp)
    return  resultSet

#print(get_recom_set("The Godfather: Part II"))
#print(get_recommendation_list("The Godfather: Part II"))
#print('EEEEEEEE')
print(getUrlArr(get_recom_set("The Godfather: Part II")))