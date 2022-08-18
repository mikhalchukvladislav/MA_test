import logging
import collections
import csv
import pandas as pd
import requests
import bs4
import unicodedata
# from main import final_result

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('https://www.detmir.ru/')

HEADERS = (
    'id',
    'title',
    'price',
    'promo_price',
    'city',
    'url'
)

ParseResult = collections.namedtuple('ParseResult', ('product_id',
                                                    'title',
                                                    'price',
                                                    'promo_price',
                                                    'city',
                                                    'url'))


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent':
                                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
                                'Accept-Language': 'ru'}

        self.result = []

        
    
    def load_page(self, url, cookies):
        res = self.session.get(url=url, cookies=cookies)
        res.raise_for_status()
        return res.text
      
    def parse_page(self, text: str, city):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select_one('div.ow.oz').select('a.PN.PZ')
    
        for block in container:
            self.parse_block(block=block, city=city)

    def parse_block(self, block, city):

        url = block.get('href')

        try:
            title = block.select_one('p.PR').text
        except:
            title=None
        
        try:
            product_id = url.split('/')[-2]
        except:
            product_id=None


        try:
            price = (unicodedata.normalize("NFKD", 
                                            block.select_one('span.P_3').text).split('₽')[0].strip())
            promo_price = ''.join(unicodedata.normalize("NFKD", 
                                                  block.select_one('p.P_1').text).split('₽')[0].strip().split(' '))
        except:
            price = ''.join(unicodedata.normalize("NFKD", 
                                                  block.select_one('p.P_1').text).split('₽')[0].strip().split(' '))
            promo_price = None

        self.result.append(ParseResult(
            product_id=product_id,
            title=title,
            price=price,
            promo_price=promo_price,
            city=city,
            url=url))


    def save_results(self, path=str(input('Введите путь, куда вы хотите сохранить отчет'))):

        filename = 'ДетскийМир' + str(pd.to_datetime('today').day) + '.' + str(pd.to_datetime('today').month) + '.' + str(
                 pd.to_datetime('today').year) + '.csv' #прописываем путь для сохранения csv файла
        path += '/' + filename 


        with open(path, 'a', encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)


    def run(self, url, cookies, city):
        text = self.load_page(url, cookies)
        self.parse_page(text=text, city=city)