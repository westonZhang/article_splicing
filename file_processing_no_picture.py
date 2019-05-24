# coding:utf-8
import os
import re
import time
import copy
import shutil
import traceback
import codecs
import openpyxl
from openpyxl import load_workbook
import random
from utils import Util
# import docx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from file_processing import File_processing1

class File_processing2():

    def __init__(self):
        self.util = Util()
        self.file_process = File_processing1()
        # 每次运行需要修改的点
        self.domain_name = self.file_process.domain_name
        self.kw_excel_name = self.file_process.kw_excel_name
        # 读取路径
        self.read_path = self.file_process.read_path
        self.keyword_path = self.file_process.keyword_path
        # 保存路径
        self.save_article_path = r'./data/save_path/{}_articles_no_picture'.format(self.domain_name)
        # self.save_img_path = r'./data/save_path/{}_imgs_with_no_picture'.format(self.domain_name)
        # self.domain_name = 'uni_technology'
        # self.keywords_num = 180  # 关键词数量
        # 已使用的关键字
        self.used_keyword = []
        # 未使用的段落
        # self.unused_paragraphs = []
        # 已使用的图片
        # self.used_pictures = []
        # 所有的段落
        # self.paragraphs = []
        # self.keywords = self.read_xlsx(self.read_path + '\keyword.xlsx')


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

    def get_file_dir(self, filepath):
        '''获取（"E:\workSpace\article_splicing\data\technology_article"）路径下的所有文件夹'''
        try:
            file_dir_list = os.listdir(self.util.to_gbk(filepath))
            file_dir_list = [file.decode('gbk').encode('utf-8') for file in file_dir_list]
            return file_dir_list
        except:
            print('get file dir error', traceback.print_exc())

    def get_file_list(self, filepath):
        '''获取（"反射型光电传感器"）目录下的所有文件及文件夹'''
        return os.listdir(self.util.to_gbk(filepath))


    def operate_picture(self, filepath):
        """
        处理图片
        :param filepath:
        :return: 所有图片的路径
        """
        try:
            imgs = []
            for file in os.listdir(self.util.to_gbk(filepath)):
                img = file.decode('gbk').encode('utf-8')
                # imgs.append(os.path.join(filepath, img))
                imgs.append(img)
            return imgs
        except:
            print('operate picture error', traceback.print_exc())


    def write_article(self, path, article):
        """保存文章为txt格式"""
        try:
            with open(path.decode('utf-8'), 'w') as f:
                f.write(article)
        except:
            print('write article error', traceback.print_exc())


    def read_xlsx(self):
        '''读取表格'''
        workbook = load_workbook(self.keyword_path)  # 工作表
        sheet = workbook.get_sheet_by_name("Sheet1")  # sheet1
        keyword_list = [i.value for i in sheet['A']]  # 读取A列的值
        if keyword_list[0] == 1:
            keyword_list = [i.value for i in sheet['B']]  # 读取A列的值
        return keyword_list


    def get_all_article(self, dir_list):
        '''获取所有的文章列表'''
        all_articles = []
        for floder in dir_list:
            filepath = self.read_path + '/' + floder
            if os.path.isdir(unicode(filepath,"utf-8")) and floder != 'image' and floder != 'video':
                file_list = [file.decode('gbk').encode('utf-8') for file in self.get_file_list(filepath) if file]

                for file in file_list:
                    t_filepath = filepath + '/' + file
                    filename = t_filepath.split('/')[-1]
                    if filename.endswith(u'首段.txt'):
                        start_paragraph_list = self.util.start_end_paragraph(t_filepath)  # 首段所有段落
                    elif filename.endswith(u'中段.txt'):
                        middle_paragraph_list = self.util.middle_paragraph(t_filepath)
                        all_mid_list = self.util.mid_permutation_and_combination(middle_paragraph_list)  # 中段所有排列组合之后的情况
                    elif filename.endswith(u'尾段.txt'):
                        end_paragraph_list = self.util.start_end_paragraph(t_filepath)  # 尾段所有段落
                articles = self.util.article_permutation_and_combination(start_paragraph_list, all_mid_list, end_paragraph_list)
                article_list = []
                article_list = self.util.get_article_list(articles, article_list)  # 存储最终的所有的文章（无图）【单个文件夹下的】

                for _ in article_list:
                    all_articles.append(_)
        return all_articles


    def get_article_str(self, paragraph_list, keyword):
        '''对每一段进行拼接，包括插入关键词和插入图片'''
        article_str = ''
        for i in range(len(paragraph_list)):
            # first_keyword = keyword
            if i == 0 or i == len(paragraph_list) - 1:  # 添加首段/尾段
                paragraph_list[i] = self.util.insert_keyword(keyword, paragraph_list[i])  # 插入关键词
                article_str += '<p>%s</p>\n' % paragraph_list[i]
            else:  # 添加其他段落
                article_str += '<p>%s</p>\n' % paragraph_list[i]
        return article_str

    def get_article_len(self, article):
        '''求文章长度'''
        article_len = 0
        for i in article:
            article_len += len(i.decode('utf8'))
        return article_len

    def splice_article(self, all_articles):
        # img_list = self.operate_picture(self.read_path + '/imgs')  # 获取所有图片
        ## 每次循环生成一篇文章
        for _ in range(len(self.keywords)):
            print(_)
            keyword = self.get_keyword()  # 每一篇文章使用一个关键词
            if keyword == None:  # 关键词使用完之后退出循环
                break
            print(keyword)
            # 随机抽取文章，要求文章字数在730~870
            while True:
                article = random.choice(all_articles)  # 随机抽一篇文章
                article_len = self.get_article_len(article)
                if 730 < article_len < 870:
                    break

            temp_article = copy.deepcopy(article)  # 深拷贝，对新数据进行处理，不改变原数据
            # try:
            #     img = random.sample(img_list, 2)  # 随机取两张图
            # except:
            #     break
            article_str = self.get_article_str(temp_article, keyword)
            # 从图片list移除图片，实现图片的不复用
            # img_list.remove(img[0])
            # img_list.remove(img[1])

            save_path = os.path.join(self.save_article_path, keyword + '.txt')
            self.write_article(save_path, article_str.decode('utf-8').encode('gbk'))
        # 重置已使用的关键词
        # self.used_keyword = []


    def main(self):
        '''拼接，生成一篇文章'''
        if not os.path.exists(self.save_article_path):
            os.mkdir(self.save_article_path)
        # 拷贝文件夹
        # if not os.path.exists(self.save_img_path):
        #     shutil.copytree(self.read_path + '/imgs', self.save_img_path)

        self.keywords = self.read_xlsx()[0:30]  # 取关键词
        file_dir_list = self.get_file_dir(self.read_path)  # 获取所有文件夹及文件
        # every_article_num = len(self.keywords) // len(file_dir_list) + 1  # 平均每个文件夹中需要生成多少篇文章
        all_articles = self.get_all_article(file_dir_list)
        self.splice_article(all_articles)

