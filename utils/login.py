import requests
# from AipOcr import process_result
from settings import ENABLE_AUTO_SAVE_SUCCESS_IMAGE, DEBUG
from utils.predict import tf_result
from _credentials import personMobile, password
# import execjs
from lxml import etree
from PIL import Image
import os
import datetime
from urllib import parse

HOST = 'https://apply.jtj.gz.gov.cn'


def login():
    """
    执行登陆步骤

    :return: 返回一个元祖（s, res_account_page)
        s: 登陆成功后的会话
        res_account_page: 用户中心html
    """
    login_url = HOST + '/apply/user/login.html'

    valid_code_url = HOST + '/apply/validCodeImage.html?ee=1'

    login_middleware_url = HOST + '/apply/user/person/login.html'

    s = requests.session()
    s.get(login_url)
    # 网站改版，取消了密码加密
    # md5_url = HOST + '/apply/js/md5.js'
    # md5 = s.get(md5_url).content.decode()
    # context = execjs.compile(md5)
    # result = context.call('hex_md5', password)
    result = password

    # 尝试登陆
    while True:
        res_valid_code = s.get(valid_code_url)
        # 将获得的验证码图片保存
        with open('src/code.jpeg', 'wb') as f:
            f.write(res_valid_code.content)
            if DEBUG:
                print('验证码获取成功')
        # img = Image.open('code.jpeg')
        # img.show()

        # valid_code = process_result()
        valid_code = tf_result()
        data = {
            'userType': '0',
            'ranStr': '',
            'userTypeSelect': '0',
            'loginType': 'mobile',
            'unitLoginTypeSelect': '0',
            'unitMobile': '',
            'orgCode': '',
            'personMobile': personMobile,
            'password': result,
            'validCode': valid_code
        }

        res = s.post(login_middleware_url, data=data)
        res_account_page = res.text
        wb_pg = etree.HTML(res_account_page)

        # 验证是否登陆成功
        try:
            success_sign = wb_pg.xpath('//*[@id="myManage"]/div[1]/div[2]/div[1]/text()')[0]
        except IndexError:
            print('登陆失败...')
            # 打印url返回的失败信息
            print('错误信息：' + parse.unquote(res.url[res.url.find('?message=') + 9:]))
            continue
        else:
            success_sign = success_sign.replace('\r', '').replace('\n', '').replace(' ', '')
            print('已进入：', success_sign)
            print('登录成功！')
            if ENABLE_AUTO_SAVE_SUCCESS_IMAGE:
                # 保存验证码样本，提高识别准确率
                image = Image.open('src/code.jpeg')
                if not os.path.exists('src/success_image'):
                    os.mkdir('src/success_image')
                image.save(
                    f'src/success_image/{valid_code.upper()}_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.JPEG'
                )
                print('验证码保存成功！')

            return s, res_account_page


if __name__ == '__main__':
    login()
