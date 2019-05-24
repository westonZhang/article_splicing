# -*- encoding: utf-8 -*-
import re
import os
import random
import traceback
import openpyxl
import itertools
from itertools import combinations
from functools import reduce


class Util():

    def __init__(self):
        pass

    def to_gbk(self, filepath):
        """
        转码包含中文的文件路径
        :param filepath:
        :return:
        """
        try:
            filepath = filepath.decode('utf-8').encode('gbk')
        except:
            pass
        return filepath


    def start_end_paragraph(self, filename):
        '''首段/尾段'''
        with open(filename.decode('utf-8'), 'r') as f:
            start_lines = [line.decode('gbk').encode('utf-8') for line in f.readlines() if line!='\n' and line != '\r\n']
        return start_lines

    def middle_paragraph(self, filename):
        '''中段'''
        with open(filename.decode('utf-8'), 'r') as f:
            middle_lines = [line.decode('gbk').encode('utf-8') for line in f.readlines() if line!='\n' and line != '\r\n']
        return middle_lines

    def mid_permutation_and_combination(self, t_list):
        '''针对中段的排列组合，返回所有可能生成的段落组合'''
        all_list = list(combinations(t_list, 3))
        if not all_list:
            all_list = list(combinations(t_list, 2))
        if not all_list:
            all_list = list(combinations(t_list, 1))
        all_list = [list(_) for _ in all_list]
        return all_list

    def article_permutation_and_combination(self, lista, listb, listc):
        '''针对整篇文章的排列组合'''
        return list(itertools.product(lista, listb, listc))

    def get_article_list(self, all_article, article_list):
        for i in all_article:
            article = []
            article.append(i[0])
            for _ in i[1]:
                article.append(_)
            article.append(i[2])
            article_list.append(article)
        return article_list

    def insert_keyword(self, keyword, paragraph):
        """往段落中插入关键字"""
        rangnum = random.randint(0, 1)
        # 在逗号后面插入关键字
        try:
            if rangnum == 0:
                paragraph_split = re.split('，', paragraph)
                if len(paragraph_split) == 1:
                    paragraph_split = re.split(u'，', paragraph)
                paragraph_split = [p for p in paragraph_split if p != '\n']
                if len(paragraph_split) <= 1:
                    index = 0
                elif len(paragraph_split) == 2:
                    index = 1
                else:
                    index = random.randint(1, len(paragraph_split) - 2)

                paragraph_split.insert(index, keyword)
                data = '，'.join([p for p in paragraph_split if p != '\n']).replace(u'%s，' % keyword, keyword)
                return data
                # return u'，'.join([p for p in paragraph_split if p])
            # 在句号后面插入关键字
            else:
                paragraph_split = re.split('。', paragraph)
                if len(paragraph_split) == 1:
                    paragraph_split = re.split(u'。', paragraph)
                paragraph_split = [p for p in paragraph_split if p != '\n']
                if len(paragraph_split) <= 1:
                    index = 0
                elif len(paragraph_split) == 2:
                    index = 1
                else:
                    index = random.randint(1, len(paragraph_split) - 2)

                paragraph_split.insert(index, keyword)
                data = '。'.join([p for p in paragraph_split if p != '\n']).replace(u'%s。' % keyword, keyword)
                return data
        except:
            pass

if __name__ == '__main__':
    util = Util()
    lista = [1,2]
    listb = [3,4,5]
    listc = [6,7]
    all_list = util.article_permutation_and_combination(lista, listb, listc)
    print all_list