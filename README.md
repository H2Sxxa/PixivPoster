# PixivPoster
支持WordPress、Typecho、Hexo、Flarum网站的每日Pixiv TOP50文章发布

高度可自定义的配置，自定义文章样式表

## 快速开始
编辑task.txt改为以下内容，然后运行main.py，根据提示查看教程填入Pixiv Code回车即可

```json
{"task":"use_config","name":"local delopy","args":"./setting/flarum"}

{"task":"run","name":"local run"}
```

如遇任何问题，请先尝试删除.cfg文件再次运行，如果还是不行，将.cfg内的savelog改为true，在issue粘贴日志即可

## 新建配置

1. 在setting包中新建名字为配置名称(例如poster)的文件夹

2. 在你刚才创建的文件夹中新建base.md(必须)和config.cfg(如果找不到，程序将自动生成)

3. 编辑base.md改为你需要的样式，例子查看setting/default/base.md，具体查看下方自定义文章

4. 手动编辑config.cfg改为你需要的配置，具体看下方自定义配置

5. 编辑task.txt加入以下内容后即可

```json
#读取配置
{"task":"use_config","name":"任务名称（随便取）","args":".../setting/你的文件夹名称（最好使用绝对路径）"}
#运行
{"task":"run","name":"任务名称（随便取）"}
```

## 自定义配置
web_type: 有local,wordpress,typecho,flarum多种选项

web_local_name: 变量名称用于下方dir和root

web_local_dir: .md文件存储的位置

web_local_root: local网站根目录

web_local_deploy: web_local_root下脚本名称

web_address: 网站地址(xmlrpc)，.../xmlrpc.php

web_title: 自定义标题 $date 为日期

web_flarum_tagid: flarum下板块的ID

web_account: wordpress,typecho...账户

web_password: wordpress,typecho...密码

use_forward_proxy 正向代理服务器地址，如果设置反代则会被忽略

use_reverse_proxy 反代服务器地址，详见https://pixiv.cat/reverseproxy.html

reserve_proxy_qulity 反代模式下的图片质量，有square_medium,medium,large,original

clean_cache: 清除缓存（生成的markdown以及html）

sock_proxy: 默认为空，填入则启用代理

sni: 默认true绕过SNI

savelog: 默认false不生成日志

pixiv_mode: ↓

- mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]

- mode[Past]: [day, week, month, day_male, day_female, week_original, week_rookie,day_r18, day_male_r18, day_female_r18, week_r18,week_r18g]

refresh_token: 第一次启动输入code程序会自动填写，用于登录

以上是所有默认配置，当然你也可以创建新的键值并使用$键名称$来在其他地方调用

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

:tag 标签，建议设计样式后使用
### 创建样式
:warning: 注意：所有样式必须为一行

#### 部分样式
:style>{"function":作用域,键1:值1,键2:值2...}

illust

 - rpimgtext 替换文本

 - imgtext 悬浮文本

```base.md
:style>{"function":"illust","rpimgtext":"PID:illustid","imgtext":":illustname"}
```

illusttags

 - tagshow #todo

 - illustmaxtag 主体样式中tag数量

 - rand_maxtag :tag标签最大tag数量[1,2,3]

 - tagslang 不建议更改

```base.md
:style>{"function":"illusttags","tagshow":"#todo","illustmaxtag":5,"rand_maxtag":3,"tagslang": 0}
```

illustshow

 - prefix 每张图片前添加的文本

 - ImgSlide 不建议使用

```base.md
:style>{"function":"illustshow","prefix":">! "}
```

#### 主体样式
?>img,最大图片数(None为全部),主体(部分变量生效)<?

```base.md
?>img,None,>! ## Title [:illustname](https://www.pixiv.net/artworks/:illustid)$n>!$n>! ### :tag$n>!$n>! ### Artist [:artistname](https://www.pixiv.net/users/:artistid)$n>!$n:illust$n>!$n<?
```