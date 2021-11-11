import re
import pandas as pd
from icecream import ic
from konlpy.tag import Okt
from datetime import datetime
from matplotlib import pyplot as plt
from nltk import word_tokenize, FreqDist
from wordcloud import WordCloud


class WordCloud_okky(object):
    def __init__(self):
        pass

    def okky(self):
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
        print(f':::::::: {datetime.now()} ::::::::\n {freq_texts}')
        wcloud = WordCloud('./data/D2Coding.ttf',
                           background_color='white').generate(' '.join(texts_without_stopwords))
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('./data/wcloud.png')

if __name__ == '__main__':
    wc = WordCloud_okky()
    wc.okky()
