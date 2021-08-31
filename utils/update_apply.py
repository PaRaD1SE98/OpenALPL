from lxml import etree
from utils.login import login, HOST


def update_apply():
    """
    执行延期申请
    """
    while True:
        s, res_account_page = login()
        wb_pg = etree.HTML(res_account_page)
        # 获取申请表链接
        apply_chart_link = wb_pg.xpath(
            '//*[@id="myManage"]/div[2]/div/div[3]/div[2]/table/tbody/tr[2]/td[9]/a[1]//@href'
        )[0]
        apply_chart_link = HOST + apply_chart_link
        res_apply_page = s.get(apply_chart_link).text
        wb_pg = etree.HTML(res_apply_page)
        try:
            # 检测是否有确认延期按钮，id为 keepUpButton, 若已经延期，此xpath报错IndexError
            wb_pg.xpath('//*[@id="keepUpButton"]/text()')[0]
        except IndexError:
            # print(repr(IndexError))
            print('延期确认成功，查看确认信息和申请状态')
            confirm_note = wb_pg.xpath('//*[@class="confirmNote"]/text()')[1]
            confirm_note = confirm_note.replace('	', '').replace('\r', '').replace('\n', '')
            print('确认信息:', confirm_note)

            apply_status = wb_pg.xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div/table/tr[2]/td/div/dl/dt/span/text()'
            )[0]
            try:
                apply_status = apply_status.replace('	', '').replace(' ', '').replace('\n', '').replace('\r', '')
                print('申请状态:', apply_status)
                return apply_status
            except IndexError as e:
                print(repr(e))
                continue
        else:
            # 最重要的一步，模拟点击确认延期按钮，实际上是get访问这个链接，并获得返回页面
            keepup_res = s.get(HOST + '/apply/person/keepUp.do').text
            keepup_pg = etree.HTML(keepup_res)
            confirm_note = keepup_pg.xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div/table/tr[2]/td/div/p[2]/text()'
            )[0]
            confirm_note = confirm_note.replace('	', '').replace('\r', '').replace('\n', '')
            print('确认信息:', confirm_note)
            return confirm_note


if __name__ == '__main__':
    update_apply()
