import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

url_1st = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=waste+OR+by-product+OR+byproduct%29+AND+%28%22valorisation%22+OR+%22valorization%22+OR+%22conversion%22+OR+%22recycling%22&startPage='
#https://onlinelibrary.wiley.com/action/doSearch?AllField=waste+OR+by-product+OR+byproduct%29+AND+%28%22valorisation%22+OR+%22valorization%22+OR+%22conversion%22+OR+%22recycling%22&pageSize=50&startPage=0&Ppub=%5B20200301%20TO%2020220301%5D
url_3nd = '&pageSize=50'
url_4th = '&Ppub=%5B20200301%20TO%2020220301%5D'
user_agent = {'User-agent': 'Mozilla/5.0'}  # 反反爬虫
count = 0

'''
点开abstract
'''
abs_url_1st = 'https://onlinelibrary.wiley.com/action/PB2showAjaxAbstract?doi='
abs_url_4th = '&isItemAbstract=true'

'''
爬取的信息，标题，摘要和doi号
'''
titles = []
abstract = []
links = []
doilist = []

for i in range(5):
    print(f'====page{count}====')
    '''
    获取到初始页面
    '''
    #url = url_1st + str(count) + url_3nd + url_4th
    url = url_1st + str(count) + url_3nd
    content_html = requests.get(url, headers=user_agent)
    content_text = content_html.text

    '''
    解析网页
    '''
    soup = BeautifulSoup(content_text, 'lxml')
    title_tags = soup.find_all('a', class_='publication_title')
    # abstract_tags = soup.find_all('div', class_ = 'abstract-group')

    '''
    针对一个页面的爬取
    '''
    #tqdm进度条
    for tag in tqdm(title_tags):
        print(end='\r')
        #type: str
        doi = tag.get('href')
        doilist = doi.split('/')
        abs_url_2nd = doilist[2]
        abs_url_3rd = doilist[3]
        abs_url = abs_url_1st + abs_url_2nd + '%2F' + abs_url_3rd + abs_url_4th
        abs_content_html = requests.get(abs_url, headers=user_agent)

        abs_content_text = abs_content_html.text
        soup2 = BeautifulSoup(abs_content_text, 'lxml')
        abstract_tag = soup2.find('p') #不能用find_all

        '''
        异常处理，可以出现没有摘要的情况
        '''
        try:
            abstract_tag = abstract_tag.get_text()
        except:
            abstract_tag = 'no abstract'

        abstract.append(abstract_tag)
        links.append(tag.get('href'))
        titles.append(tag.get_text())


    '''
    翻页
    '''
    count += 1

dict = {'title': titles, 'abstract': abstract, 'link': links}
df = pd.DataFrame(dict)
df.to_csv('reault1000.csv', encoding='UTF-8')