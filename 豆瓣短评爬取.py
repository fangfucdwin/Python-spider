import requests
#from bs4 import BeautifulSoup
import pandas as pd
import re


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
     
def parsePage(movies_data, html):
    try:    
        search_pattern = re.compile('<a title="(.*?)"')
        search_pattern2 = re.compile('<span class="allstar(.*?) rating"')
        search_pattern3 = re.compile('<p class=""> (.*)')
        name_list = re.findall(search_pattern, html)
        grade_list = re.findall(search_pattern2, html)
        comments_list = re.findall(search_pattern3, html)
        for i in range(len(name_list)):
            name = name_list[i]
            grade = grade_list[i]
            comments = comments_list[i]
            movies_data.append([name, grade,comments])
    except:
        print('')
      
def main():
    movieID = '4920389' #各个电影的ID号，该ID号为头号玩家
    depth = 3 #爬取的评论页数
    start_url = 'https://movie.douban.com/subject/'+ movieID +'/comments?start=' 
    movies_data = []
    for i in range(depth):
        try:
            page = 0 + i*20
            url = start_url + str(page) + '&limit=20&sort=new_score&status=P&percent_type='
            html = getHTMLText(url)
            parsePage(movies_data, html)
        except:
            continue
    movies_datalist = pd.DataFrame(movies_data,index=range(1,len(movies_data)+1),columns=['用户','评分','评论'])
    print(movies_datalist)

main()
