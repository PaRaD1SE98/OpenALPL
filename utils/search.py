import requests
from lxml import etree
from utils.init import get_init_vars
from settings import SIMULATE_BINGO


def search():
    """
    搜索根据账号密码获取的申请编码

    :return: 返回元祖(结果表头，结果列表)
        t_head: 结果表头元祖（申请编号， 姓名）
        t_content: 结果元祖（申请编号， 姓名）
    """
    if not SIMULATE_BINGO:
        apply_code = get_init_vars('APPLY_CODE')
    else:
        apply_code = '8529103402320'  # test 中签

    host = 'https://apply.jtj.gz.gov.cn/apply/norm/personQuery.html'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'pageNo=1&issueNumber=000000&applyCode={apply_code}'

    wb_data = requests.post(host, headers=headers, data=data).text
    html = etree.HTML(wb_data)

    t_head = (
        html.xpath('/html/body/div[2]/div/div/div[1]/div/table/tr[1]/td/table/tr/th[1]/text()')[0],
        html.xpath('/html/body/div[2]/div/div/div[1]/div/table/tr[1]/td/table/tr/th[2]/text()')[0]
    )
    try:
        t_content = (
            html.xpath('/html/body/div[2]/div/div/div[1]/div/table/tr[1]/td/table/tr[2]/td[1]/text()')[0],
            html.xpath('/html/body/div[2]/div/div/div[1]/div/table/tr[1]/td/table/tr[2]/td[2]/text()')[0]
        )
    except IndexError:
        t_content = ()

    return t_head, t_content


def data_formatter():
    """
    格式化查询结果

    :return: 元祖
        formatted: 格式化后的str
        raw: 结果元祖（申请编号，姓名），无结果则为空元祖
    """
    t_head, t_content = search()
    raw = t_content
    if raw:
        formatted = '{}-{}\n{}-{}'.format(t_head[0], t_head[1], t_content[0], t_content[1])
        return formatted, raw
    else:
        return '没有查询到结果。', raw


if __name__ == '__main__':
    print(data_formatter())
