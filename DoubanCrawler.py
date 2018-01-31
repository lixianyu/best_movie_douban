import expanddouban

gMyCategory = ['科幻', '动作', '悬疑']
gMyLocation = ['大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']
"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影," + category + "," + location
    return url

# for test Task1
# for cat in gMyCategory:
#     for loc in gMyLocation:
#         print(getMovieUrl(cat, loc))

# for test Task2
# url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,喜剧,美国"
# html = expanddouban.getHtml(url, True, 2.4)
# print('html = {}\n'.format(html))
# print('type(html) = {}'.format(type(html)))
