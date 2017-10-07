# -*- coding:utf-8 -*-


#http请求设置
HTTP_CONFIG = {
                'timeout':5,
                'use_tor_proxy': False,
                'tor_proxy_port': 9050
}


#自定义http请求头
HEADERS = [
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'},
    {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'},
    {'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'},
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'},
    {'User-Agent':'Mozilla/5.0 (Android; Tablet; rv:14.0) Gecko/14.0 Firefox/14.0'},
    {'User-Agent':'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0'},
    {'User-Agent':'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'},
    {'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25'},
    {'User-Agent':'Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.2)'},
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'},
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
    {'User-Agent':'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)'},
]


API_ = {
    'youku': "http://api.2m.vc/caij/inc/youku.php",
    'mgtv': "http://api.2m.vc/caij/inc/mgtv.php",
    'letv': "http://api.2m.vc/caij/inc/letv.php",
    'qiyi': "http://api.2m.vc/caij/inc/qiyi.php",
    'qq'  : "http://api.2m.vc/caij/inc/qq.php",
    'sohu': "http://api.2m.vc/caij/inc/sohu.php",
    'pptv': "http://api.2m.vc/caij/inc/pptv.php",
}


#绑定分类
VOD_CLASS = {
    u'动作': 5,
    u'喜剧': 6,
    u'爱情': 7,
    u'科幻': 8,
    u'恐怖': 9,
    u'剧情': 10,
    u'战争': 11,
    u'国产剧': 12,
    u'港台剧': 13,
}


# 播放器组
PLAY_GROUP = ['youku', 'tudou', 'mgtv', 'le', 'sohu', 'qiyi', 'qq', 'pptv']



# 360kan采集电影类型
CAT_360 = {
    u'喜剧': 103,
    u'爱情': 100,
    u'动作': 106,
    u'恐怖': 102,
    u'科幻': 104,
    u'剧情': 112,
    u'犯罪': 105,
    u'奇幻': 113,
    u'战争': 108,
    u'悬疑': 115,
    u'动画': 107,
    u'文艺': 117,
    u'伦理': 101,
    u'纪录': 118,
    u'传记': 119,
    u'歌舞': 120,
    u'古装': 121,
    u'历史': 122,
    u'惊悚': 123,
}
