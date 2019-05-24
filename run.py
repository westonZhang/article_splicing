# coding:utf-8
import traceback
from utils import Util
from file_processing import File_processing1
# from file_processing_no_picture import File_processing2
# from file_processing_pic_no_multiplex import File_processing3
# from file_processing_with_video import File_processing4

util = Util()
file_process1 = File_processing1()
# file_process2 = File_processing2()
# file_process3 = File_processing3()
# file_process4 = File_processing4()

def run():
    try:
        file_process1.splice_article()  # 最原始的
        # file_process2.main()  # 纯文本，不加图片
        # file_process3.main()  # 图片不复用
        # file_process4.main()  # 视频
    except Exception, e:
        print traceback.print_exc(e)


if __name__ == '__main__':
    run()
    # raw_input('-- press ENTER to exit --')