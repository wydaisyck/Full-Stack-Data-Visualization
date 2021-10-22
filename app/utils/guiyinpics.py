import os
import base64
from app.utils.const import pic_path


def getNameListsGuiyin():
    file_dir = pic_path
    guiyindict = {}
    product_list = []
    for dir in os.listdir(file_dir):
        productname = dir[:-22]
        timeperiod = dir[-22:]
        if not guiyindict.get(productname):
            guiyindict[productname] = []
            guiyindict[productname].append(timeperiod)
        else:
            guiyindict[productname].append(timeperiod)

        if productname not in product_list:
            product_list.append(productname)
    return guiyindict


def getGuiyinpics(product_name, time_period):
    dirname = product_name+time_period
    path1 = pic_path+'/'
    path = os.path.join(path1, dirname)
    pics_list = []
    for pic in os.listdir(path):
        if pic.endswith('.png'):
            pics_list.append(pic)
    return path, pics_list


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """

    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream


def get_img_list(guiyindict, product_name):
    datelist = guiyindict[product_name]
    img_list = {}
    # 默认显示date最近的一个周
    path, picslist = getGuiyinpics(product_name, datelist[-1])
    for pic in picslist:
        img_path = os.path.join(path, pic)
        img_stream = return_img_stream(img_path)
        img_list[pic[:-4]] = img_stream
    return img_list, datelist