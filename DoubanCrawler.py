import expanddouban
import bs4
import csv
import requests

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
    #html = expanddouban.getHtml(url, True, 2.4)
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    all_a = soup.find(class_="list-wp")
    #print('all_a = {}\r\n'.format(all_a))
    #print(type(all_a))
    # for element in all_a.find_all("img", recursive=True):
        # print('cover_link = {}'.format(element.get('src')))
        # print(type(element))

    for element in all_a.find_all("a", recursive=False):
        # print('name = {}'.format(element.find(class_="title").get_text()))
        # print('rate = {}'.format(element.find(class_="rate").get_text()))
        # print('location = {}'.format(location))
        # print('category = {}'.format(category))
        # print('cover_link = {}'.format(element.find('img').get('src')))
        # print('info_link = {}'.format(element.get('href')))
        # print('....................................................................................................................................')
        name = element.find(class_="title").get_text()
        rate = element.find(class_="rate").get_text()
        cover_link = element.find('img').get('src')
        info_link = element.get('href')
        m = Movie(name, rate, location, category, info_link, cover_link)
        movieList.append(m)
    return movieList

# for test Task1
# for cat in gMyCategory:
#     for loc in gMyLocation:
#         print(getMovieUrl(cat, loc))

# for test Task2
# url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,喜剧,美国"
# html = expanddouban.getHtml(url, True, 2.4)
# print('html = {}\n'.format(html))
# print('type(html) = {}'.format(type(html)))

# for test Task3
# aMovie = Movie()
# aMovie.name = 'lxy'
# print(aMovie.name)

f = open('movies.csv', 'w')
csv_writer = csv.writer(f)
for cat in gMyCategory:
    for loc in gMyLocation:
        ms = getMovies(cat, loc)
        if len(ms) == 0:
            continue
        for movie in ms:
            csv_writer.writerow([movie.name, movie.rate, movie.location, movie.category, movie.info_link, movie.cover_link])
        time.sleep(1.9)

f.close()
