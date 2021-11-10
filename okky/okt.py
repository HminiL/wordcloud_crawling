from konlpy.tag import Okt

class WordCloud(object):
    def __init__(self):
        pass

    def okky(self):
        okt = Okt()
        daddy_bag = okt.pos('아버지 가방에 들어가신다', norm=True, stem=True)
        print(f':::::::: {datetime.now()} ::::::::\n {daddy_bag}')


if __name__ == '__main__':
    wc = WordCloud()
    wc.okky()