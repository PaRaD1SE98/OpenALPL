"""
每个月执行 search， update_apply 和 send_mail
"""
from time import strftime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from _credentials import EMAIL_USER
from settings import DEBUG
from utils.init import get_init_vars
from utils.mail_sender import YAG_SERVER
from utils.mail_sender import send_email
from utils.search import data_formatter
from utils.update_apply import update_apply

DO_JOB_DAY = '28'
DO_JOB_HOUR = '23'


# 定义任务
def job_function():
    # 查询是否中签
    formatted, raw = data_formatter()
    send_email(formatted, raw)
    print(f'{strftime("%Y/%m/%d %T")} 报告邮件已发送!', flush=True)
    # 如果未中签
    if not raw:
        update_apply()
    else:
        # 如果中签，使用后台调度器的任务关闭阻塞式调度器进程
        wrapper.shutdown(wait=False)


# 定义阻塞式调度器的任务，使用阻塞式调度器管理后台调度器
def schedule_wrapper():
    # 定义后台调度器
    scheduler = BackgroundScheduler()

    # 添加任务
    scheduler.add_job(
        job_function,
        # Cron表达式生成工具：https://www.freeformatter.com/cron-expression-generator-quartz.html
        # Day Of Month = day, '?' = None, 默认就是None,忽略就好
        # 测试用，10秒执行一次
        trigger=CronTrigger(
            year='*',
            month='*',
            hour='*',
            minute='*',
            second='0/10'
        ) if DEBUG else CronTrigger(
            year='*',
            month='*',
            day=DO_JOB_DAY,
            hour=DO_JOB_HOUR,
            minute='0',
            second='0'
        ),
        id="search_and_update_job",
        max_instances=5,
        replace_existing=True,
    )
    # 任务开始前开始时先立即执行一次
    job_function()
    scheduler.start()


# 定义阻塞式调度器，配置任务
wrapper = BlockingScheduler()
wrapper.add_job(
    schedule_wrapper,
    id="schedule_wrapper",
    max_instances=1,
    replace_existing=True,
)

if __name__ == '__main__':
    print(f'{strftime("%Y/%m/%d %T")} 服务已启动！', flush=True)

    YAG_SERVER.send(
        EMAIL_USER,
        '广州车牌摇号小助手',
        f'自动中签检测和延长申请服务已启动！\n'
        f'您的申请编码是{get_init_vars("APPLY_CODE")}\n'
        f'首次摇号年月是{get_init_vars("START_DATE")}'
    )
    if DEBUG:
        print(f'{strftime("%Y/%m/%d %T")} 启动通知邮件已发送!', flush=True)

    try:
        wrapper.start()
        print(f'{strftime("%Y/%m/%d %T")} 任务完成！', flush=True)
    except (KeyboardInterrupt, SystemExit):
        print(f'{strftime("%Y/%m/%d %T")} 服务已停止！', flush=True)
