# -*- coding:UTF-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy #导入scrapy包
from bs4  import  BeautifulSoup
from scrapy.http import Request
from items import DingdianItem



class Myspider(scrapy.Spider):

    name='dingdian'
    allow_domains=['23us.com']
    bash_url='http://www.23us.com/quanben/'


    def start_requests(self):
        yield Request('http://www.23us.com/quanben/1',self.parse)



    def parse(self,response):
        # max_num=BeautifulSoup(response.text,'lxml').find('div',class_='pagelink').find_all('a')[-1].get_text()
        number=BeautifulSoup(response.text,'lxml').find('div', class_='pagelink')
        max_num=number.find('a',class_='last').get_text()
        print max_num
        for num in range(1,int(max_num)+1):
            url=self.bash_url+str(num)
            # print url
            yield Request(url,callback=self.get_name)



    def get_name(self,response):
        tdf = BeautifulSoup(response.text, 'lxml').find_all('tr',bgcolor='#FFFFFF')
        for td in tdf:
            novelname=td.find('a').get_text()
            novelurl=td.find('a')['href']
            # print novelname,novelurl
            yield Request(novelurl,callback=self.get_chapterurl,meta={'name':novelname,'url':novelurl})



    def get_chapterurl(self,response):
        item = DingdianItem()
        item['name'] = str(response.meta['name']).replace('\xa0', '').decode('utf-8', 'ignore')
        # item['novelurl'] = response.meta['url']
        category = BeautifulSoup(response.text, 'lxml').find('table').find('a').get_text()
        author = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')[1].get_text()
        # print category,author
        bash_url = BeautifulSoup(response.text, 'lxml').find('p', class_='btnlinks').find('a', class_='read')['href']
        name_id = str(bash_url)[-6:-1].replace('/', '')
        item['category'] = str(category).replace('/', '').decode('utf-8', 'ignore')
        item['author'] = str(author).replace('/', '').decode('utf-8', 'ignore')
        item['name_id'] = name_id.decode('utf-8', 'ignore')
        # print item['name'],item['novelurl'],item['category'],item['author'],item['name_id']
        return item

