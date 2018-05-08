import requests
import re
import jieba.posseg as pseg
from wordcloud import WordCloud
from scipy.misc import imread
import matplotlib.pyplot as plt



def getHTMLText(url):
    try:
        kv = {'User-Agent': 'Mozilla/5.0','cookie': 'bid=GnjdCDhLpTU; __yadk_uid=MTIk2dGsJCmNTGCzd9bnig6CAFEEe8CA; ll="118318"; _vwo_uuid_v2=D78124E41BF9CB8C399A7E7E542ADAA3B|858b856b608251c6b4c7b45291852a50; viewed="1084336"; ps=y; push_noty_num=0; push_doumail_num=0; ap=1; __utmc=30149280; _ga=GA1.2.67448164.1525064425; _gid=GA1.2.177907817.1525751447; ue="fangfucdwin@QQ.COM"; dbcl2="153589233:k12vAS0hXBc"; ck=qQF_; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1525762034%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%3Falias%3D13671601426%26redir%3Dhttps%253A%252F%252Faccounts.douban.com%252Fsafety%252Funlock_sms%252Fcaptcha%253Fconfirmation%253D9d1b8305c7a92743%26source%3DNone%26error%3D1027%22%5D; _pk_id.100001.8cb4=6a9e44735f3ceffe.1525064424.7.1525762034.1525751442.; _pk_ses.100001.8cb4=*; __utma=30149280.67448164.1525064425.1525751447.1525762041.9; __utmz=30149280.1525762041.9.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmt=1; __utmv=30149280.15358; __utmb=30149280.2.10.1525762041'}
        r = requests.get(url,headers=kv, timeout=30)
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
        
def draw_wordcloud():
    with open('movies_data.txt','r',encoding='utf-8') as f:
        movies_subjects = f.readlines()
    stop_words = set(line.strip() for line in open('movies_data.txt', encoding='utf-8'))
    words = []
    for subject in movies_subjects:
        if subject.isspace():
            continue
        word_list =  pseg.cut(subject)
        for word, flag in word_list:
            if not word in stop_words and flag == 'n':
                words.append(word)
    mask_image =  imread( "D:\\Pictures\\catdaidai.jpg")
    wc = WordCloud(background_color="grey",font_path='C:\\WindowsFonts\\STCAIYUN.TTF',mask=mask_image, max_words=300)
    content = ' '.join(words)
    wordcloud = wc.generate(content)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()                  # 展示词云
    wc.to_file('头号玩家词云.png')        # 保存到图片
        
def main():
    movieID = '4920389'
    depth = 20
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
    with open("movies_data.txt",'w',encoding='utf-8') as f:
        for i in movies_data:
            f.write(str(i[2])+"\n")
    draw_wordcloud()
main()
