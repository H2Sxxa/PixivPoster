# PixivPoster
支持WordPress、Typecho、Hexo...网站的每日Pixiv TOP50页面创建

高度可自定义的配置，自定义文章样式表

使用前请先删除default.cfg来恢复默认配置

## 自定义配置
web_type: 有local,wordpress,typecho三种选项
web_local_name: 变量名称用于下方dir和root
web_local_dir: .md文件存储的位置
web_local_root: local网站根目录
web_local_deploy: web_local_root下脚本名称
web_address: 网站地址(xmlrpc)，.../xmlrpc.php
web_title: 自定义标题 $date 为日期
web_account: wordpress,typecho...账户
web_password: wordpress,typecho...密码
clean_cache: 清除缓存（生成的markdown以及html）
sock_proxy: 默认为空，填入则启用代理
sni: 默认true绕过SNI
savelog: 默认false不生成日志
pixiv_mode: 
    mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    mode[Past]: [day, week, month, day_male, day_female, week_original, week_rookie,
day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
refresh_token: 第一次启动程序会自动填写

当然你也可以创建新的键值并使用$键名称$来在其他地方调用

## 自定义文章
### 替换字符
#### 全局变量
$time 时间
$date 日期
$n 换行符
$br 换行符（不推荐）
#### 部分变量
:artistname: 当前画师名称
:aritstid 当前画师ID
:illust 图片（一连串）
:illustname 当前作品名称
:illustid 当前作品ID
#TODO illusttag
### 创建一个样式
必须为一行，格式为:style>JSON
```base.md
:style>{"function":"illust","rpimgtext":"PID:illustid","imgtext":":illustname"}
```