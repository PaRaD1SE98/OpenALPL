import cv2
import cv2 as cv
import os


def get_filenames(in_dir):
    """
    获得文件夹内的所有文件名

    :param str in_dir: 源文件夹
    :return: filenames： 文件名列表
    """
    filenames = os.listdir(in_dir)
    filenames = sorted(filenames, key=lambda x: os.path.getmtime(os.path.join(in_dir, x)))
    for i, j in zip(filenames, range(len(filenames))):
        filenames[j] = i[:4]
    # print(filenames)
    return filenames


def get_filedate(in_dir):
    """
    获得文件夹内所有文件的修改日期

    :param in_dir: 源文件夹
    :return: 文件日期列表
    """
    filedates = os.listdir(in_dir)
    filedates = sorted(filedates, key=lambda x: os.path.getmtime(os.path.join(in_dir, x)))
    for i, j in zip(filedates, range(len(filedates))):
        filedates[j] = i[5:-5]
    # print(filedates)
    return filedates


def seperate_filename(filename):
    """
    分离文件名

    :param str filename: 文件名
    :return: li: 文件名分离后的列表
    """
    li = []
    for i in filename:
        li.append(i)
        # print(li)
    return li


def crop_jpeg(in_dir, out_dir):
    """
    切割图片

    :param str in_dir: 输入文件夹
    :param str out_dir: 输出文件夹
    """
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    for i, j in zip(get_filenames(in_dir), get_filedate(in_dir)):
        letter = seperate_filename(i)
        im = cv.imread(f'{in_dir}/{i}_{j}.JPEG', cv.IMREAD_GRAYSCALE)
        # 裁剪坐标为[y0:y1, x0:x1]
        width = 34
        height = 46
        code_length = 4
        for k in range(code_length):
            out = im[0:height, width * k:width * (k + 1)]
            try:
                cv.imwrite(f'{out_dir}/{letter[k]}_{i}_{j}.JPEG', out)
            except cv2.error:
                print('\n出错图像', i, j)
        print('\rImage cropped!', i, j, end='')
    print('')
