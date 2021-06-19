import cv2 as cv
import os
from PIL import Image  # , ImageFilter

from settings import DEBUG


def resize_jpeg():
    """
    改变图像尺寸
    """
    im = Image.open('src/code.jpeg')
    x, y = im.size
    # print('o_size:', x, y)
    x_s = 70 * 2
    y_s = int(y * x_s / x)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    # 转换为黑白，
    # out = out.convert('L')
    # out = out.filter(ImageFilter.SHARPEN).filter(ImageFilter.SHARPEN)
    # out = out[7:39, 0:140 - 6]
    # out = out.crop((0, 39, 134, 7))
    out.save('src/code.jpeg')
    if DEBUG:
        print('Image resized!')


def crop_jpeg():
    """
    切割图片
    """
    if not os.path.exists('/tmp/cropped_image'):
        os.mkdir('/tmp/cropped_image')
    resize_jpeg()
    im = cv.imread('src/code.jpeg', cv.IMREAD_GRAYSCALE)
    # 裁剪坐标为[y0:y1, x0:x1]
    width = 34
    height = 46
    code_length = 4
    for i in range(code_length):
        out = im[0:height, width * i:width * (i + 1)]
        cv.imwrite(f'/tmp/cropped_image/{i}.JPEG', out)
    if DEBUG:
        print('Image cropped!')


if __name__ == '__main__':
    crop_jpeg()
