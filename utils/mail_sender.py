import yagmail
import datetime

from settings import DEBUG
from utils.search import data_formatter
from _credentials import EMAIL_USER, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_LIST
from utils.init import get_init_vars

# 连接服务器
# 用户名、授权码、服务器地址
YAG_SERVER = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASSWORD, host=EMAIL_HOST)

# 周期仅用于改变发送邮件的内容，并不改变更新申请的频率
APPLY_UPDATE_CYCLE = 3


# START_DATE = '2020-12'  # test 已到更新月份


def get_previous_month(str1):
    """
    获取输入日期的上一个月份

    :return: int: 月份
    """
    first_day_this_month = datetime.datetime.strptime(str1, '%Y-%m-%d').replace(day=1)
    end_day_last_month = first_day_this_month - datetime.timedelta(days=1)
    return end_day_last_month.month


def process_start_date(start_date):
    """
    处理将月份减1用于计算

    :param str start_date: 首次摇号年月
    :return: datetime: 日期对象
    """
    date = start_date + '-26'
    result = datetime.datetime.strptime(date, '%Y-%m-%d').replace(month=get_previous_month(date))
    return result


def months(str1, str2):
    """
    月份转换器，获取两个日期的月份相差数

    :param str str1: %Y-%m-%d
    :param str str2: %Y-%m-%d

    :return: int: 相差的月份数
    """
    year1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").year
    year2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").year
    month1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").month
    month2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").month
    num = (year1 - year2) * 12 + (month1 - month2)
    return num


def send_email(content, result):
    """
    根据不同条件发送不同邮件

    :param str content: 邮件通用内容
    :param tuple|bool result: 查询中签返回的结果，未中签返回False
    """
    start_date = get_init_vars('START_DATE')
    today = datetime.date.today()

    # 发送对象列表
    email_to = EMAIL_LIST
    # 邮件标题
    email_title = '车牌摇号报告'

    email_content = content
    extra_content = '\n未中签，已更新申请了,验证更新结果：https://jtzl.jtj.gz.gov.cn/'
    extra_content2 = '\n未中签，暂时不需要更新申请,更多查询：https://jtzl.jtj.gz.gov.cn/'
    bingo_content = '\n中签了！去官网查询结果：https://jtzl.jtj.gz.gov.cn/'

    # 如果未中签
    if not result:
        print('未中签。')
        # 如果到了更新月份
        if months(str(today), str(process_start_date(start_date))) % APPLY_UPDATE_CYCLE == 0:
            email_content = email_content + extra_content
        else:
            print('还没到更新月份')
            email_content = email_content + extra_content2
    else:
        print('中签了！')
        email_content = email_content + bingo_content

    # 附件列表
    # email_attachments = ['./attachments/report.png', ]

    # 发送邮件
    # YAG_SERVER.send(email_to, email_title, email_content, email_attachments)
    YAG_SERVER.send(email_to, email_title, email_content)
    if DEBUG:
        print('中签结果邮件已发送', flush=True)


if __name__ == '__main__':
    formatted, raw = data_formatter()
    send_email(formatted, raw)
