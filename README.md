# movie_spider
用于自动将最新电影(来自[电影港](http://www.dygang.com/))下载([迅雷离线](http://yuancheng.xunlei.com/))到路由器硬盘

## Installation

```bash
git clone git@github.com:yangwe1/movie_spider.git
cd movie_spider
sudo -H pip install -r requirements.txt
cd pwd_http
# nodejs 搭建的简易 http 服务，用于生成迅雷登陆密码加密后的内容，由迅雷登陆页 js 稍加改写而来
sudo npm install
```
## Setup
编辑 movie_spider/config.json 文件

### thunder
迅雷远程下载登陆部分

* username: 迅雷用户名
* pwd: 密码
* device_name: 迅雷远程下载中要指定的设备名称

### moviebay
电影港爬取监控部分

* category:
    * 可选值有 ys/bd/gy/gp/dsj/dsj1/yx/zy/dmq/jilupian/1080p/720p/3d 等
    * 分别对应 最新电影/BD高清/国配电影/.../3D电影(详见[电影港](http://www.dygang.com/)横栏)   
* page: 值为整数，需要监控的页数，建议3页之内

### time_schedule
脚本每天运行的起止时间，24小时制

* start: 开始
* stop: 停止

一直运行则分别为"0:00","24:00"

### interval
扫描电影网站的时间间隔，比如1则代表每隔1小时扫描电影港指定类别的电影是否有新片加入

### mail
邮箱通知的设置

* server 用于设置发件箱smtp服务器
    * isSSL: 是否加密
    * smtp: smtp地址
    * port: smtp端口
    * user: 登陆用户名
    * password: 登陆密码
* mail 用于设置邮件相关内容
    * subject: 邮件主题
    * from: 发件人地址，如weiyang512@gmail.com
    * to: 收件人地址，如weiyang512@gmail.com
    
## Run

```
cd pwd_http
nohup node pwd_http.js > http.out 2>&1 &
cd ..
nohup python start.py &
```
## To-do
将 pwd_http 改写，或者会加到 python 里，或者会用 Ice; 加一些硬盘空间监控，考虑一下比较智能些的删除老片释放空间的方式