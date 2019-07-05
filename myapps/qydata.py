#! -*- coding:utf8 -*-
"""
    按关键字抓取企查查网站免费数据
    require python 3.7.1
    作者：潘达叔
"""
import pickle
import requests
import logging
import pandas as pd
import argparse
import sys
from bs4 import BeautifulSoup as bs
from random import choice

class GetQyData(object):
    """
        抓取企业信息数据
    """
    def __init__(self, keywords=[]):
        self.RequestInfo = {
            'headers':[],
            'cookies':[],
            }
        self.fromsite = ''
        self.keywords=keywords
        self.QyList=[]
        self.QyDf = pd.DataFrame()
    def to_pandas(self):
        """
            将self.QyList转换成pandas对象
        """
        self.QyDf=pd.DataFrame(self.QyList, columns=['Name','Status','Capital','estDate','Addr','LxName','Email','Tel','Detail'])
    def get_keywords(self,keywords=[]):
        self.keywords = keywords
    def save_pkl(self, filename='tmp.pkl'):
        """
            保存对象到pkl
        """
        with open (filename, 'wb') as f:
            pickle.dump(self, f)
    def load_pkl(self, filename='tmp.pkl'):
        """
            从pkl恢复对象
        """
        with open(filename, 'rb') as f:
            self = pickle.load(f)
    def save_xls(self, filename='GetQyData.xls'):
        """
            保存记录到 excel 文件
        """
        self.QyDf.to_excel(filename)
    def save_csv(self, filename='QyData.csv'):
        """
            保存记录到 CSV 文件
        """
        self.QyDf.to_csv(filename)
    def save_mysql(self):
        """
            保存记录到 mysql 数据
        """
        pass
    def get_list_one(self,pageno=1):
        """
            按关键词list抓取列表页
        """
        pass
    def get_list_all(self,pagenum=1):
        """
            按页码抓取多个列表页
        """
        pass    
    def get_page(self,url,header=''):
        """
            抓取单个页面, 返回bs对象
        """
        url = requests.utils.requote_uri(url)
        print(url)
        if header:
            html = requests.get(url, headers=header)
        else:
            html = requests.get(url, headers=choice(self.RequestInfo['headers']), cookies=choice(self.RequestInfo['cookies']))
        page = bs(html.content, features='html5lib')
        return page
    def get_detail(self,url):
        """
            抓取单个企业资料页面内容
        """
        pass

class GetQyDataQichacha(GetQyData):
    def __init__(self, keywords=[], conditions={}):
        super(GetQyDataQichacha,self).__init__(keywords)
        self.RequestInfo['headers'] = [{
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
            },]
        # Cookie 需要登陆后从控制台获取
        self.RequestInfo['cookies'] = [{
            'acw_tc':'7ce8aa4515604780315067440eea2094b6a5ae583a85f6f925b12c48b9',
            'UM_distinctid':'16b53bd1b1220-046c55b3ba9fba8-4c312d7d-144000-16b53bd1b13491',
            'CNZZDATA1254842228':'1669062529-1560475100-https%253A%252F%252Fwww.baidu.com%252F%7C1561463419',
            'zg_did':'%7B%22did%22%3A%20%2216b53bd1b2125c-0f934ff654ef26-4c312d7d-144000-16b53bd1b24c%22%7D',
            'zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f':'%7B%22sid%22%3A%201561468521005%2C%22updated%22%3A%201561468729606%2C%22info%22%3A%201561468521053%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22e22c0f2a6d0bcf34a5ecf0e104d87493%22%7D',
            '_uab_collina':'156047803086740505858948',
            'Hm_lvt_3456bee468c83cc63fb5147f119f1075':'1560478031,1560478284,1560922659,1561468521',
            'QCCSESSID':'f6okt11k20c7702ihg68qldn84',
            'Hm_lpvt_3456bee468c83cc63fb5147f119f1075':'1561468585',
            'hasShow':'1'
            },]
        self.RequestInfo['conditions'] = conditions if conditions else {
            'province':'HUN',                   # 省份:湖南
            # 'county':'430111',                  # 雨花区
            # 'sortField':'startdate-false',      # 排序方式:成立时间从晚到早
            'statusCode':'20',                  # 企业状态:存续, 注意 状态存续和 有限责任公司不能并存
            'coyType':'10',                     # 企业类型:有限责任
            'city':'430100',                    # 城市:长沙
            # 'registfund':'0-500',               # 注册资本: 0-500万元
            }
        self.fromsite = 'Qichacha'
        self.lastPage=1
    def get_list_one(self,pageno=1,getLastPage=False):
        # url = 'https://www.qichacha.com/search?key=%s#%s' % (
        #     '+'.join(self.keywords), 
        #     '&'.join(['%s:%s' % (i,self.RequestInfo['conditions'][i]) for i in self.RequestInfo['conditions'].keys()])
        #     )
        url = 'https://www.qichacha.com/search_index?key=%s&ajaxflag=1&%s' % (
            '+'.join(self.keywords),
            '&'.join(['%s=%s' % (i,self.RequestInfo['conditions'][i]) for i in self.RequestInfo['conditions'].keys()])
            )
        if pageno > 1:url = '%s&p=%d' % (url,pageno) 
        page = self.get_page(url=url)
        # 提取出总页数
        if getLastPage:
            self.lastPage = int(page.find('ul', class_='pagination').find_all('a')[-2].text.strip().replace('.',''))
        info_list = page.find('tbody', id='search-result')
        if not info_list:
            print('找不到数据')
            return False
        info_list = info_list.find_all('tr')
        for i in info_list:
            QyInfo = [j.text.split() for j in i.find_all('p',class_='m-t-xs')]
            print(QyInfo)
            self.QyList.append({
                'Name':i.find('a', class_='ma_h1').text,
                'Status':i.find('td', class_='statustd').span.text,
                'Detail':'https://www.qichacha.com%s' % i.find('a', class_='ma_h1').get('href'),
                'LxName':QyInfo[0][1],
                'Capital':QyInfo[0][2],
                'estDate':QyInfo[0][3][5:],
                'Email':'' if QyInfo[1][0][3] == '-' else QyInfo[1][0][3:],
                'Tel':'' if QyInfo[1][1][3] == '-' else QyInfo[1][1][3:],
                'Addr':QyInfo[2][0][3:]
                })            
    def get_list_all(self,pageNum=6):
        self.get_list_one(getLastPage=True)
        if pageNum > self.lastPage: pageNum = self.lastPage
        for pageno in range(2,pageNum+1):
            self.get_list_one(pageno=pageno)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='从企查查获得企业数据, cookies使用登录后的网络请求记录中获取，求好心人给个付费账号测试下cookies')
    parser.add_argument('--keywords', '-k', help='添加关键字列表,注意使用","号分隔')
    parser.add_argument('--csv', '-c', help='指定保存的csv文件名, 否则不保存')
    parser.add_argument('--excel', '-e', help='指定保存excel文件名, 否则不保存')
    args = parser.parse_args()
    if args.keywords:
        keywords = args.keywords.split()
        qicc = GetQyDataQichacha(keywords)
        qicc.get_list_all()
        print('get_list_all, %d logs' % len(qicc.QyList))
        qicc.to_pandas()
    else:
        print('Please input keywords')
        sys.exit(0)
    if args.csv:
        qicc.save_csv(args.csv)
    if args.excel:
        print(args.excel)
        qicc.save_xls(args.excel)