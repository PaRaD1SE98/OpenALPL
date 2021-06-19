广州车牌摇号小助手
===
介绍
---
你是否厌倦了常年摇号不中，还得定期去更新申请的繁琐步骤？那么这个项目也许能帮到你。
本项目利用爬虫和机器学习图像识别实现了自动化获取广州车牌摇号官网的每个月摇号结果，能根据结果帮你自动更新摇号申请。每个月摇号结束后结果将以邮件形式发送到你指定的邮箱，如果你摇中了，程序会自动结束。

基本用法
---
### 本项目在CentOS7测试部署成功，建议使用相同系统增加部署成功率
### 安装虚拟环境和依赖
#### venv
```python -m venv venv```

```source venv/bin/activate```

```pip install -r requirements/base.txt```
### 配置帐号
把```_credentials.sample```后缀改为```.py```并填入相关值

### 尝试运行定时任务
运行```schedule.py```

跑起来后配置帐号里填写的邮箱会收到服务启动邮件

### 部署到linux服务器，用supervisor后台托管
### 安装 supervisor
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
修改配置文件 supervisor.conf，注意将路径改为符合自己系统的，下面的配置文件同理
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

### 创建 GZCPYHXZS 项目配置文件

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
##### 启动 supervisor
```
supervisord -c ~/etc/supervisord.conf
```
##### 进入 supervisor 控制台
```
supervisorctl -c ~/etc/supervisord.conf
```
##### 在控制台内运行
```
supervisor>
supervisor> update
supervisor> 
```

额外功能
---
### 训练自己的验证码识别器
安装开发依赖```pip install -r requirements/dev.txt```

将获取到的验证码按命名格式```2AHN_20210504-171258.JPEG```放在```src/success_image```

运行```python train_my_model.py```

生成的logs文件夹可用```tensorboard```打开，评估训练结果
```tensorboard --logdir logs```