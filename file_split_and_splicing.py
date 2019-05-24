# -*- encoding: utf-8 -*-
import os
import re
import copy
import chardet
import traceback
import codecs
import shutil
from docx import Document
import openpyxl
from openpyxl import load_workbook
import random
from utils import Util
import docx
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from file_processing import File_processing1


class FileSplitAndSplicing(object):
    """
    将txt或docx的文章拆分下来首段,中段,尾段,然后其按照之前的逻辑拼接文章.
    """

    def __init__(self):
        self.util = Util()
        self.file_paocessing1 = File_processing1()
        self.document = docx
        # 域名
        self.domain_name = 'szlflab_a_4'
        self.kw_excel_name = '{}_keywords.xlsx'.format(self.domain_name)
        # 读取
        self.read_path = r'./data/read_path/{}'.format(self.domain_name)

        # 保存路径
        self.save_article_path = r'./data/save_path/{}_articles'.format(self.domain_name)
        self.save_img_path = r'./data/save_path/{}_imgs'.format(self.domain_name)
        self.start_keyword = 0  # 关键词开始的位置
        self.end_keyword = 50  # 关键词结束的位置
        self.special_keyword = '苏州'
        self.used_keyword = []

    def read_xlsx(self):
        '''读取表格'''
        # filepath = r'E:/workSpace/article_splicing/data/keyword.xlsx'
        workbook = load_workbook(self.keyword_path)  # 工作表
        sheet = workbook.get_sheet_by_name("Sheet1")  # sheet1
        keyword_list = [i.value for i in sheet['A'] if i.value is not None]  #
        if keyword_list[0] == 1:
            keyword_list = [i.value for i in sheet['B'] if i.value is not None]
        return keyword_list

    def get_keywords(self):
        """
        获取关键词
        举例:现需要150个关键词,含有"苏州"的关键词优先,
        如果含有"苏州"的关键词超过150个,则取前150个,
        如果含有"苏州"的关键词不到150,则取完这些词还要再取一些普通关键词凑够150个
        """
        all_keywords = self.read_xlsx()  # 所有的关键词
        special_keywords = [kw for kw in all_keywords if self.special_keyword in kw]  # 特殊关键词,如:含有"苏州"的关键词
        all_keywords = [kw for kw in all_keywords if self.special_keyword not in kw]  # 不含有"苏州"的所有的关键词

        keywords_num = self.end_keyword - self.start_keyword  # 需要的关键词个数
        if len(special_keywords) >= keywords_num:
            needed_keywords = special_keywords[0:keywords_num]
            remaining_keywords = special_keywords[keywords_num:]
            remaining_keywords.extend(all_keywords)
        else:
            needed_keywords = copy.deepcopy(special_keywords)
            needed_keywords.extend(all_keywords[0: keywords_num-len(special_keywords)])
            remaining_keywords = all_keywords[(keywords_num-len(special_keywords)):]
        return needed_keywords, remaining_keywords

    def get_keyword(self):
        """
        获取关键字(不能重复)
        :return:
        """
        try:
            unused_keyword = list(set(self.keywords) ^ set(self.used_keyword))
            if len(unused_keyword) == 0:
                return None
            keyword = random.choice(unused_keyword)
            self.used_keyword.append(keyword)
            return keyword
        except:
            traceback.print_exc()

    def split_article(self, file):
        """
        将文章拆分为首段/中段/尾段
        """
        if file.endswith('txt'):
            with open(file, 'r') as f:
                paragraphs = f.readlines()
        else:
            document = Document(u'{}'.format(file))
            paragraphs = [p.text for p in document.paragraphs if p.text != '\n']
        paragraphs = [p for p in paragraphs if p != '' and p is not None]

        start = paragraphs[0]
        middle = paragraphs[1: -1]
        end = paragraphs[-1]
        return start, middle, end

    def run(self):
        if not os.path.exists(self.save_article_path):
            os.mkdir(self.save_article_path)
        if not os.path.exists(self.save_img_path):
            os.mkdir(self.save_img_path)

        article_list = []
        start_paragraph_list = list()  # 存放所有首段段落
        middle_paragraph_list = list()  # 存放所有中段段落
        end_paragraph_list = list()  # 存放所有尾段段落

        file_dir_list = self.file_paocessing1.get_file_dir(self.read_path)  # 获取所有文件

        for folder in file_dir_list:
            self.keyword_path = r'./data/read_path/{domain_name}/{folder}/{kw_excel_name}'.format(
                domain_name=self.domain_name, folder=folder, kw_excel_name=self.kw_excel_name)
            # self.keywords, self.remaining_keywords = self.get_keywords()

            self.keywords = self.read_xlsx()[self.start_keyword:self.end_keyword]  # 普通的取关键词

            if not os.path.isdir(unicode(self.read_path + '/' + folder, "utf-8")):
                continue
            file_path = self.read_path + '/' + folder
            file_list = [file for file in self.file_paocessing1.get_file_list(file_path) if file]

            # 获取所有首段/中段/尾段
            for file in file_list:
                if file != 'img' and 'xlsx' not in file:
                    t_filepath = file_path + '/' + file
                    start_paragraph, middle_paragraph, end_paragraph = self.split_article(t_filepath)
                    start_paragraph_list.append(start_paragraph)
                    middle_paragraph_list.extend(middle_paragraph)
                    end_paragraph_list.append(end_paragraph)
                elif file == "img":
                    t_filepath = file_path + '/' + file
                    img_list = self.file_paocessing1.operate_picture(t_filepath)  # 获取所有图片
                    for img in img_list:
                        shutil.copy(u"{}".format(self.read_path + '/' + folder + '/img/' + img), self.save_img_path)
            # middle_paragraph_list = middle_paragraph_list if len(middle_paragraph_list) < 100 else random.sample(middle_paragraph_list, 100)
            all_mid_list = self.util.mid_permutation_and_combination(middle_paragraph_list)  # 中段所有排列组合之后的情况
            all_mid_list = all_mid_list if len(all_mid_list) < 2000 else random.sample(all_mid_list, 2000)
            articles = self.util.article_permutation_and_combination(start_paragraph_list, all_mid_list,
                                                                     end_paragraph_list)
            # articles = self.util.article_permutation_and_combination(random.sample(start_paragraph_list, 10), random.sample(all_mid_list, 10) , random.sample(end_paragraph_list, 10))
            article_list = self.util.get_article_list(articles, article_list)  # 存储最终的所有的文章【单个文件夹下的】

            ## 下面每次循环生成一篇文章, 每个文件夹需要生成“every_article_num”篇文章
            # for _ in range(every_article_num):
            i = 1
            while True:
                keyword = self.get_keyword()  # 每一篇文章使用一个关键词
                if keyword is None:  # 关键词使用完之后退出循环
                    break
                print(i)
                print(keyword)

                # 随机抽取文章，要求文章字数在730~870
                # while True:
                #     article = random.choice(article_list)  # 随机抽一篇文章
                #     article_len = self.file_paocessing1.get_article_len(article)
                #     if 730 < article_len < 900:
                #         break
                try:
                    article = random.choice(article_list)  # 随机抽一篇文章
                    temp_article = copy.deepcopy(article)  # 深拷贝，对新数据进行处理，不改变原数据
                    img = random.sample(img_list, 2)  # 随机取两张图
                    article_str = ''
                    ####  段落 -- 对每一段进行处理
                    for num in range(len(temp_article)):
                        first_keyword = keyword
                        if num == 0 or num == len(temp_article) - 1:  # 添加首段/尾段
                            temp_article[num] = self.util.insert_keyword(keyword, temp_article[num])  # 插入关键词
                            article_str += '<p>%s</p>\n' % temp_article[num]
                        elif num == 1:  # 添加第二段，并插入一张图片
                            article_str += '<p>%s</p>\n' % temp_article[num]
                            article_str += '<p><img src={imgpath}/%s_imgs/%s></p>\n' % (
                                self.domain_name, img[0])  # 注意修改站点名称
                        elif num == 3:  # 添加第四段，并插入一张图片
                            article_str += '<p>%s</p>\n' % temp_article[num]
                            article_str += '<p><img src={imgpath}/%s_imgs/%s></p>\n' % (
                                self.domain_name, img[1])  # 注意修改站点名称
                        else:  # 添加第三段
                            article_str += '<p>%s</p>\n' % temp_article[num]
                    save_path = self.save_article_path + '/' + '{}.txt'.format(first_keyword)
                    self.file_paocessing1.write_article(save_path, article_str.decode('utf-8').encode('gbk'))
                    i += 1
                except Exception as e:
                    # 如果遇到错误,就将关键词从"used_keyword"列表中取出,这样就可以重新获取此关键词进行拼接
                    self.used_keyword.remove(keyword)
                    traceback.print_exc()

            # 重置已使用的关键词
            # self.used_keyword = []


if __name__ == '__main__':
    file = FileSplitAndSplicing()
    file.run()
