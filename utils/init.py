from settings import DEBUG
from utils.login import login
from lxml import etree


def save_apply_code_and_start_date():
    """
    初始化，在开启scheduler前要运行一次，获取需要的数据
    """
    if DEBUG:
        print('开始执行初始化！')
    while True:
        s, res = login()
        try:
            account_page = etree.HTML(res)
            apply_code = account_page.xpath(
                '//*[@id="myManage"]/div[2]/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/text()'
            )[0]
            print('申请编码:', apply_code)
            shuffle_page = s.get('https://apply.jtj.gz.gov.cn/apply/person/getIssue.do?applyCode=0794103537472')
            shuffle_page = etree.HTML(shuffle_page.text)
            shuffle_dates = shuffle_page.xpath(
                '//*[@id="content"]/div/div/div/div[4]/div/div[1]/ul[2]/li[contains(@style,"background:#0066FF")]'
                '/text()'
            )

            def find_keyword(word):
                index = word.find('期')
                result = word[index - 6:index]
                return result

            for i in range(len(shuffle_dates)):
                shuffle_dates[i] = find_keyword(shuffle_dates[i])
            # print(shuffle_dates)
            start_date = shuffle_dates[0][:6]
            start_date = start_date[:4] + '-' + start_date[4:6]
            print('首次摇号年月:', start_date, flush=True)
            with open('init.txt', 'w') as f:
                f.write('APPLY_CODE=' + apply_code + '\n')
                f.write('START_DATE=' + start_date + '\n')
            if DEBUG:
                print('初始化成功！', flush=True)
            break
        except IndexError:
            continue


def get_init_vars(var):
    """
    获取需要的变量值

    :param str var: 变量名
    :return: value： 变量值
    """
    try:
        with open('init.txt', 'r') as f:
            content = f.readlines()
    except FileNotFoundError:
        if DEBUG:
            print('未执行过初始化！', flush=True)
        save_apply_code_and_start_date()
        with open('init.txt', 'r') as f:
            content = f.readlines()

    for i in content:
        try:
            index = i.index(f'{var}=')
        except ValueError:
            pass
        else:
            result_var = i[index + len(var) + 1:-1]
            if DEBUG:
                print('初始变量获取成功！ ' + var + '=' + result_var, flush=True)
            return result_var
