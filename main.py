import requests
from parsing.parsing import Client
import pandas as pd


if __name__ == '__main__':
    #num_of_page = 1
    url = 'https://www.detmir.ru/catalog/index/name/kukly_i_aksessuary/'  # Выбор категории, бyдем добавлять число в конец
    session = requests.Session()
    session.headers = {'User-Agent':
                           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
                       'Accept-Language': 'ru'}
    parser = Client()
    city_dict = [{
        'geoCityDM': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%20%D0%B8%20%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C', 
        'geoCityDMIso': 'RU-SPE', 
        'geoCityDMCode': '7800000000000'
    }, 
                 {
        'geoCityDM':'%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%20%D0%B8%20%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
        'geoCityDMIso': 'RU-MOW',
        'geoCityDMCode': '7700000000000'
                 }
    ]

    for city in city_dict:
        i = 0
        while True:  # Сколько страниц столько и итераций цикла
            i += 1
            try:
                parser.run(url=(url + 'page/' + str(i) + '/'), cookies=city, city=city['geoCityDMIso'].split('-')[1])
            except:
                break
        parser.save_results()

    filename_read = 'ДетскийМир' + str(pd.to_datetime('today').day) + '.' + str(pd.to_datetime('today').month) + '.' + str(
                 pd.to_datetime('today').year) + '.csv' #прописываем путь для сохранения csv файла

    filename_write = 'ДетскийМир(по МСК и СПБ)' + str(pd.to_datetime('today').day) + '.' + str(pd.to_datetime('today').month) + '.' + str(
                 pd.to_datetime('today').year) + '.csv' #прописываем путь для сохранения csv файла

    df = pd.read_csv(filename_read, sep=',')
    df = df.drop_duplicates(subset=['id', 'title', 'price', 'promo_price'], keep='first')
    df = df.drop(['city'], axis=1)

    df.to_csv(filename_write, sep='\t', encoding="utf-8", index=False)