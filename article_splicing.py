# -*- coding: utf-8 -*-
import os
import random
import codecs
import numpy
import shutil
import traceback
import chardet
from docx import Document

class ArticleInsertImg():
    """
    从众多图片中随即抽取一些图片插入到txt文档中
    段落添加"p"标签
    """

    def __init__(self):
        self.domain_name = 'meijiapeixun'
        self.read_article_path = r'./data/read_path/{}'.format(self.domain_name)
        self.read_img_path = r'./data/read_path/{}/img'.format(self.domain_name)
        self.save_article_path = r'./data/save_path/{}_articles'.format(self.domain_name)
        self.save_img_path = r'./data/save_path/{}_imgs'.format(self.domain_name)

    def get_file(self, path):
        files = os.listdir(path)
        if files:
            return files

    def insert_img(self, paragraphs, imgs, article_name):
        """
        将图片插入文章
        """
        article = ''
        try:
            random_p1 = numpy.random.randint(2, high=(len(paragraphs)/2), size=None, dtype='l')
        except:
            random_p1 = numpy.random.randint(1, high=(len(paragraphs) / 2)+1, size=None, dtype='l')
        for p in range(len(paragraphs)):
            # 在第二段到倒数第二段之间插入图片
            if p == random_p1:
                img = random.choice(imgs)
                article += '<img src={imgpath}/%s_imgs/%s>\n' % (self.domain_name, img.encode('gbk'))
                imgs.remove(img)
                i = 1
                while i < 5:
                    random_p2 = numpy.random.randint(random_p1, high=len(paragraphs)-1, size=None, dtype='l')
                    if random_p2 != random_p1:
                        break
                    i += 1
            elif 'random_p2' in dir() and p == random_p2:
                img = random.choice(imgs)
                article += '<img src={imgpath}/%s_imgs/%s>\n' % (self.domain_name, img.encode('gbk'))
                imgs.remove(img)
            try:
                if paragraphs[p] != '​\n':
                    article += paragraphs[p].decode('utf8').encode('gbk')
            except Exception:
                try:
                    article += paragraphs[p].encode('gbk')
                except:
                    traceback.print_exc()

        article_path = self.save_article_path + '/' + article_name
        if os.path.exists(article_path):
            os.remove(article_path)
        try:
            with codecs.open(article_path.replace('docx', 'txt'), 'w', "gbk") as w:
                w.write(article.decode('gbk'))
        except:
            traceback.print_exc()


    def run(self):
        if not os.path.exists(self.save_article_path):
            os.mkdir(self.save_article_path)
        if not os.path.exists(self.save_img_path):
            os.mkdir(self.save_img_path)
        articles = self.get_file(self.read_article_path)
        all_imgs = self.get_file(self.read_img_path)
        for img in all_imgs:
            shutil.copy(self.read_img_path + '/' + img, self.save_img_path)

        for article in articles:
            if article != 'img':
                insert_imgs = random.sample(all_imgs, 2)
                article_path = self.read_article_path + '/' + article
                if 'txt' in article:
                    with open(article_path, 'r') as f:
                        paragraphs = f.readlines()
                    paragraphs = ['{}\n'.format(p.strip('\n')) for p in paragraphs if p is not None]
                elif 'docx' in article:
                    document = Document(article_path)
                    paragraphs = [p.text for p in document.paragraphs if p.text != '\n']
                self.insert_img(paragraphs, insert_imgs, article)


if __name__ == '__main__':
    article_insert_pic = ArticleInsertImg()
    article_insert_pic.run()

