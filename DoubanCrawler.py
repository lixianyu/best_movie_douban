import expanddouban
import requests
import bs4
import csv
import time

gMyCategory = ['科幻', '动作', '悬疑']
gMyLocation = ['大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']

class Movie(object):
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def __str__(self):
        return '''name = %s
        rate = %s
        location = %s
        category = %s
        info_link = %s
        cover_link = %s''' % (self.name, self.rate, self.location, self.category, self.info_link, self.cover_link)

"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影," + category + "," + location
    return url

"""
return a list of Movie objects with the given category and location.
"""
def getMovies(category, location):
    movieList = []
    url = getMovieUrl(category, location)
    html = expanddouban.getHtml(url, True, 2.4)
    soup = bs4.BeautifulSoup(html, "html.parser")

    all_a = soup.find(class_="list-wp")
    # print('all_a = {}\r\n'.format(all_a))
    if not all_a:
        print('Just return because all_a is None')
        return movieList

    for element in all_a.find_all("a", recursive=False):
        name = element.find(class_="title").get_text()
        rate = element.find(class_="rate").get_text()
        cover_link = element.find('img').get('src')
        info_link = element.get('href')
        m = Movie(name, rate, location, category, info_link, cover_link)
        movieList.append(m)
    return movieList

fcsv = open('movies.csv', 'w')
csv_writer = csv.writer(fcsv)
fo = open('output.txt', 'w')
for cat in gMyCategory:
    dictL = {}
    for loc in gMyLocation:
        ms = getMovies(cat, loc)
        length = len(ms)
        dictL[loc] = length
        if length == 0:
            continue
        for movie in ms:
            csv_writer.writerow([movie.name, movie.rate, movie.location, movie.category, movie.info_link, movie.cover_link])
        time.sleep(1.9)

    sorted_dictL = sorted(dictL, key=dictL.get, reverse=True)
    movieCounts = 0
    for value in dictL.values():
        movieCounts += value
    # print('movieCounts = {}'.format(movieCounts))
    rate1 = (dictL[sorted_dictL[0]]/movieCounts)
    rate2 = (dictL[sorted_dictL[1]]/movieCounts)
    rate3 = (dictL[sorted_dictL[2]]/movieCounts)
    outputStr = '在类别\'{}\'中，排名前三的分别是：{}、{}、{}，占比分别为：{:.2%}、{:.2%}、{:.2%}\n'.format(cat, sorted_dictL[0],sorted_dictL[1],sorted_dictL[2],rate1,rate2,rate3)
    fo.write(outputStr)

fcsv.close()
fo.close()
