import csv
import re
import pandas as pd
from icecream import ic
from konlpy.tag import Okt
from datetime import datetime
from matplotlib import pyplot as plt
from nltk import word_tokenize, FreqDist
from wordcloud import WordCloud
from selenium import webdriver
from bs4 import BeautifulSoup

chromedriver = 'C:\\Users\\bitcamp\\PycharmProjects\\crawling\\okky\\data\\chromedriver.exe'
path = 'C:\\Users\\bitcamp\\PycharmProjects\\crawling\\okky\\data\\'

class find_word(object):
    def __init__(self):
        self.driver = webdriver.Chrome(chromedriver)

    def real_trip(self):
        driver = self.driver
        driver.get('https://www.myrealtrip.com/offers?t=llp&qct=Jeju&qcr=Korea,%20Republic%20of&ext_categories=activity')
        driver.implicitly_wait(3)
        # driver.find_element_by_xpath('//*[@id="ExperienceList-react-component-52e1e919-08f7-49bf-a760-80411524593c"]/div/main/div[3]/div/li[3]/button').click()
        # driver.find_element_by_xpath('//*[@id="ExperienceList"]/div/main/div[2]/div[1]').click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(driver.page_source)
        # all_divs = soup.find_all('span', attrs={'class','css-q5xhtf'})
        # [print(i.string) for i in all_divs]
        driver.close()

    def okky(self):
        driver = self.driver
        # driver.get('https://okky.kr/articles/community')
        driver.get('https://okky.kr/article/1094841')
        soap = BeautifulSoup(driver.page_source, 'html.parser')
        driver.implicitly_wait(3)
        # driver.find_element_by_xpath('//*[@id="list-article"]/div[4]/ul/li[5]/div[1]/h5/a').click()
        # print(driver.page_source)
        all_divs = soap.find_all('article', attrs={'class', 'content-text'})
        # [[print(p.string) for p in i] for i in all_divs]
        contents = [[p.string for p in i] for i in all_divs]
        print(contents)
        with open(f'{path}okky2.csv', 'w', newline='', encoding='UTF-8') as f:
            wr = csv.writer(f)
            wr.writerows(contents)
        driver.close()

    def okky_v2(self):
        driver = self.driver
        driver.get(f'https://okky.kr/articles/community?offset=0&max=24&sort=id&order=desc')
        # driver.get('https://okky.kr/article/1095134')
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//*[@id="list-article"]/div[4]/ul/li[24]/div[1]/h5/a').click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup)
        # contents = soup.select('div.main > ')
        # print(driver.page_source)
        all_divs = soup.find_all('article', attrs={'class', 'content-text'})
        [[print(p.string) for p in i] for i in all_divs]
        contents = [[p.string for p in i] for i in all_divs]
        with open(f'{path}okky_v2.csv', 'w', newline='', encoding='UTF-8') as f:
            wr = csv.writer(f)
            wr.writerows(contents)
        driver.close()

    def okky_v3(self):
        driver = self.driver
        contents = []
        while range(10000):
            try:
                for i in range(0, 4801, 24):
                    driver.get(f'https://okky.kr/articles/community?offset={i}&max=24&sort=id&order=desc')
                # driver.implicitly_wait(3)
                    for j in range(1, 25):
                        driver.find_element_by_xpath(f'//*[@id="list-article"]/div[4]/ul/li[{j}]/div[1]/h5/a').click()
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        all_divs = soup.find_all('article', attrs={'class', 'content-text'})
                        # [[print(p.string) for p in div] for div in all_divs]
                        [[contents.append(p.string) for p in i] for i in all_divs]
                        driver.back()
                    print(i)
                break
            except:
                driver.back()
                print("오류 발생" + TypeError)
                pass
        print(contents)
        with open(f'{path}okky_v3.2.csv', 'w', newline='', encoding='UTF-8') as f:
            wr = csv.writer(f)
            wr.writerow(contents)
        driver.close()


    def page_loop(self):
        # driver = self.driver
        page = [f'https://okky.kr/article/{i}' for i in range(1094831, 1094841)]
        print(page)


    def okky_wordcloud(self):
        okt = Okt()
        with open('./data/okky_v3.csv','r', encoding='UTF-8') as f:
            full_texts = f.read()
        # ic(full_texts)
        line_remove_texts = full_texts.replace('\n','')
        # ic(line_remove_texts)
        tokenizer = re.compile(r'[^ ㄱ-힣]+')
        tokenized_texts = tokenizer.sub('', line_remove_texts)
        tokens = word_tokenize(tokenized_texts)
        # print(tokens)
        noun_tokens = []
        for token in tokens:
            token_pos = okt.pos(token)
            noun_token = [txt_tag[0] for txt_tag in token_pos if txt_tag[1] == 'Noun']
            if len(''.join(noun_token)) > 1:
                noun_tokens.append(''.join(noun_token))
        noun_tokens_join = " ".join(noun_tokens)
        tokens = word_tokenize(noun_tokens_join)
        print(noun_tokens_join)
        # ic(tokens)
        # with open( './data/stopwords.txt', 'r', encoding='utf-8') as f:
        #     stopwords = f.read()
        stopwords = ['완료항상']
        texts_without_stopwords = [text for text in tokens if text not in stopwords]
        freq_texts = pd.Series(dict(FreqDist(texts_without_stopwords))).sort_values(ascending=False)
        ic(f':::::::: {datetime.now()} ::::::::\n {freq_texts}')
        wcloud = WordCloud('./data/D2Coding.ttf', relative_scaling=0.2,
                           background_color='white').generate(' '.join(texts_without_stopwords))
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('./data/wcloud.png')
        with open(f'{path}freq_texts.csv', 'w', newline='', encoding='UTF-8') as f:
            wr = csv.writer(f)
            wr.writerow(freq_texts)

    def a(self):
        a = {'a':1,'b':3}
        pd.
        with open(f'{path}test.csv', 'w', newline='', encoding='UTF-8') as f:
            wr = csv.writer(f)
            wr.writerow(a)



if __name__ == '__main__':
    word = find_word()
    # word.okky()
    # word.page_loop()
    # word.okky_v2()
    # word.real_trip()
    # word.okky_v3()
    # word.okky_wordcloud()
    word.a()