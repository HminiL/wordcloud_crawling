import csv

from selenium import webdriver
from bs4 import BeautifulSoup

chromedriver = 'C:\\Users\\bitcamp\\PycharmProjects\\crawling\\okky\\data\\chromedriver.exe'
path = 'C:\\Users\\bitcamp\\PycharmProjects\\crawling\\okky\\data\\'

class find_word(object):
    def __init__(self):
        self.driver = webdriver.Chrome(chromedriver)

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
        for i in range(0, 25, 24):
            driver.get(f'https://okky.kr/articles/community?offset={i}&max=24&sort=id&order=desc')
            driver.implicitly_wait(3)
            for j in range(1, 4):
                driver.find_element_by_xpath(f'//*[@id="list-article"]/div[4]/ul/li[{j}]/div[1]/h5/a').click()
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                all_divs = soup.find_all('article', attrs={'class', 'content-text'})
                # [[print(p.string) for p in div] for div in all_divs]
                contents.append([[p.string for p in i] for i in all_divs])
                driver.back()
        print(contents)
        with open(f'{path}okky_v3.csv', 'w', newline='', encoding='UTF-8') as f:
            wr = csv.writer(f)
            wr.writerows(contents)
        driver.close()

    def page_loop(self):
        # driver = self.driver
        page = [f'https://okky.kr/article/{i}' for i in range(1094831, 1094841)]
        print(page)

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



if __name__ == '__main__':
    word = find_word()
    # word.okky()
    # word.page_loop()
    # word.okky_v2()
    # word.real_trip()
    word.okky_v3()