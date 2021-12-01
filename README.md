广州车牌摇号小助手
===
###2021.12.2更新：由于官网操作延期申请添加了手机验证码步骤，本工具目前不再支持自动延期，但是仍然支持每月自动查询和邮件通知

#### 本文均用CentOS7部署，建议使用相同系统增加部署成功率

1.基本用法，直接使用python运行
---

### 安装虚拟环境和依赖
#### venv
```python -m venv venv```

```source venv/bin/activate```

```pip install -r requirements/base.txt```
### 配置账号
把```_credentials.sample```后缀改为```.py```并填入相关值

### 尝试运行定时任务
运行```schedule.py```

跑起来后配置账号里填写的邮箱会收到服务启动邮件

### 部署到linux服务器，用supervisor后台托管
### 安装supervisor
```
pip3 install supervisor
```
创建目录
```
mkdir -p ~/etc/supervisor/conf.d
mkdir -p ~/etc/supervisor/var/log
```
生成 supervisor 配置文件
```
cd ~/etc
echo_supervisord_conf > supervisord.conf
```
修改配置文件 supervisor.conf
```
[unix_http_server]
file=/home/parad1se/etc/supervisor/var/supervisor.sock   ; the path to the socket file

[supervisord]
logfile=/home/parad1se/etc/supervisor/var/log/supervisord.log ; main log file; default $CWD/supervisord.log
pidfile=/home/parad1se/etc/supervisor/var/supervisord.pid ; supervisord pidfile; default supervisord.pid
user=parad1se            ; setuid to this UNIX account at startup; recommended if root```

[supervisorctl]
serverurl=unix:///home/parad1se/etc/supervisor/var/supervisor.sock ; use a unix:// URL  for a unix socket

[include]
files = /home/parad1se/etc/supervisor/conf.d/*.ini
```

### 创建GZCPYHXZS项目配置文件
```注意将路径改为符合自己系统的```
```
cd /home/parad1se/etc/supervisor/conf.d
sudo vim GZCPYHXZS.ini
```
粘贴并保存
```
[program:GZCPYHXZS]
command=python schedule.py
directory=/home/parad1se/apps/GZCPYHXZS
environment= PATH="/home/parad1se/apps/GZCPYHXZS/venv/bin/"
autostart=true
autorestart=unexpected
user=parad1se
stdout_logfile=/home/parad1se/etc/supervisor/var/log/GZCPYHXZS-stdout.log
stderr_logfile=/home/parad1se/etc/supervisor/var/log/GZCPYHXZS-stderr.log
```
##### 启动supervisor
```
supervisord -c ~/etc/supervisord.conf
```
##### 进入supervisor控制台
```
supervisorctl -c ~/etc/supervisord.conf
```
##### 在控制台内运行
```
supervisor>
supervisor> update
supervisor> 
```

2.使用docker部署并使用tensorflow-serving
---
#### 为了提高运行效率和稳定性，同时也为增加部署成功率，使用docker部署本项目
### 安装docker和docker-compose,将当前用户添加到docker组，启动docker服务
```
$ sudo yum install -y docker docker-compose
$ sudo usermod -aG docker ${USER}
$ sudo systemctl start docker
```
退出并重新连接服务器（这一步很重要）
### 项目设置
如果没有配置账号，请先[配置账号](#配置账号)

在```settings.py```中添加或更改```ENABLE_TF_SERVING = True```
### supervisor设置
使用前面supervisor[安装](#安装supervisor)和[设置](#创建GZCPYHXZS项目配置文件)方法安装并配置， 将配置文件修改为
```
[program:GZCPYHXZS]
command=docker-compose -f production.yml up --build  
directory=/home/parad1se/apps/GZCPYHXZS
autostart=true
autorestart=unexpected
user=parad1se
stdout_logfile=/home/parad1se/etc/supervisor/var/log/GZCPYHXZS-stdout.log
stderr_logfile=/home/parad1se/etc/supervisor/var/log/GZCPYHXZS-stderr.log
```
如果你已经用[基本用法](#1基本用法直接使用python运行)部署好了，现在改为docker部署，需要执行```reread```和```update```使配置生效
```
$ supervisorctl -c ~/etc/supervisord.conf
supervisor> reread
supervisor> update
```
#### 如果容器不能启动，可以尝试重启服务器
重启后记得执行下面的命令启动docker和supervisor进程
```
$ sudo systemctl start docker
$ supervisord -c ~/etc/supervisord.conf
```
#### 再执行下面的命令查看进程运行情况
```
$ supervisorctl -c ~/etc/supervisord.conf
supervisor> status
```
#### 也可以进入[supervisor设置](#supervisor设置)里的stdout和stderr文件查看日志
```
vim /home/parad1se/etc/supervisor/var/log/GZCPYHXZS-stdout.log
```

额外功能
---
### 训练自己的验证码识别器
安装开发依赖```pip install -r requirements/dev.txt```

将获取到的验证码按命名格式```2AHN_20210504-171258.JPEG```放在```src/success_image```

运行```python train_my_model.py```

生成的logs文件夹可用```tensorboard```打开，评估训练结果
```tensorboard --logdir logs```