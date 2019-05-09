import requests as req
from lxml import etree


def get_a(word):
    s = etree.HTML(req.get('https://www.youdao.com/w/eng/{word}/'.format(word=word)).text)
    x = s.xpath('//*[@id="phrsListTab"]/div/ul//*')
    return "".join(i.text + ";" for i in x)


def gen_words(words):
    c = "".join(get_a(i) + "\n" for i in words)
    return c
