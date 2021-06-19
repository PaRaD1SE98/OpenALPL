"""
开发小工具，一键快捷上传代码及更新部署

需要将git帐号密码写入_credentials.py
"""
from fabric import task
from invoke import Responder
from _credentials import gitee_username, gitee_password


def _get_gitee_auth_responders():
    """
    返回 Gitee 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://gitee.com':",
        response='{}\n'.format(gitee_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@gitee.com':".format(gitee_username),
        response='{}\n'.format(gitee_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = ['GZCPYHXZS', ]

    project_root_path = '~/apps/GZCPYHXZS/'

    # 先停止应用
    with c.cd(supervisor_conf_path):
        for i in supervisor_program_name:
            cmd = '~/.local/bin/supervisorctl stop {}'.format(i)
            c.run(cmd)

    # 进入项目根目录，从 Gitee 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull https://gitee.com/PaRaD1SE98/GZCPYHXZS.git'
        responders = _get_gitee_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装新依赖
    with c.cd(project_root_path):
        c.run('venv/bin/pip install -r requirements/base.txt')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        for i in supervisor_program_name:
            cmd = '~/.local/bin/supervisorctl start {}'.format(i)
            c.run(cmd)
