# -*- coding:utf-8 -*-
# import pymysql as MySQLdb
import MySQLdb
import requests
# import requesocks
import random
from lxml import etree

from config import *


#获得数据库连接对象
def init_client():
    db = MySQLdb.connect(
                            host="127.0.0.1",
                            port=3306,
                            user="root",
                            passwd="liu305405",
                            db="dianying",
                            charset="utf8"
                         )
    return db


# 根据是否使用tor代理，来获取http客户端
# def get_http_client():
#     if HTTP_CONFIG['use_tor_proxy']:
#         session = requesocks.session()
#         session.proxies = {'http': 'socks5://127.0.0.1:%d' % HTTP_CONFIG['tor_proxy_port'],
#                            'https': 'socks5://127.0.0.1:%d' % HTTP_CONFIG['tor_proxy_port']}
#         return session
#     else:
#         return requests.session()


# 发送get请求
def http_get(url):
    # 设置超时时间和超时次数 5次超时返回空
    retry_times = 0
    # client = get_http_client()
    while retry_times < 5:
        try:
            content = requests.get(url, headers=random.choice(HEADERS), timeout=HTTP_CONFIG['timeout']).content
            return content
        except:
            retry_times += 1
    return ''


# 检查播放器组
def check_p(*args):
    is_ck = False
    if len(args) < 2:
        return is_ck

    for g in PLAY_GROUP:
        if args[0].find(g) > -1:
            if args[1].find(g) > -1:
                is_ck =  True
    return is_ck


# 根据电影类型查询对应的电影分类id
def find_tid(str_type):

    for t in VOD_CLASS.keys():
        if str_type.find(t) > -1:
            return VOD_CLASS[t]

    return None


def parse_vodlist(xmlbody):
    '''
    解析电影列表数据取得电影ID的集合
    返回形式:{"pagecount": 0, "recordcount":0, "video": [], "class": {}}
    '''
    try:
        vod_list = []
        tree = etree.XML(xmlbody)
        et_vods = tree.xpath("//video")
        et_list = tree.xpath("//list")
        et_tys = tree.xpath("//ty")

        # 获取list节点的属性参数
        vod_dict = et_list[0].attrib

        # 解析电影分类
        vod_class = {}
        for et_ty in et_tys:
            vod_class[et_ty.text] = et_ty.attrib["id"]

        vod_dict["class"] = vod_class

        # 解析电影信息到列表
        for et_vod in et_vods:
            vod = {}
            for et in et_vod:
                vod[et.tag] = et.text
            vod_list.append(vod)

        vod_dict['video'] = vod_list

        return vod_dict
    except:
        return {"pagecount": 0, "recordcount": 0, "video": [], "class": {}}


def parse_video(xmlbody):
        """
        解析获取电影列表数据
        返回形式:{"pagecount": 0, "recordcount": 0, "video": [{},{},{}]}
        """

        vod_list = []

        tree = etree.XML(xmlbody)
        et_vods = tree.xpath("//video")
        et_list = tree.xpath("//list")

        # 获取list节点的属性

        data = dict(et_list[0].attrib)

        for et_vod in et_vods:
            vod_dict = {}
            if not len(et_vod):
                break
            for cd in et_vod:
                if len(cd) > 0:
                    dl_dict = {}
                    for et_dd in cd:
                        flag = et_dd.attrib
                        dl_dict[flag['flag']] = et_dd.text if et_dd.text is not None else ""

                    vod_dict["dl"] = dl_dict
                    continue

                vod_dict[cd.tag] = cd.text if cd.text is not None else ""

            vod_list.append(vod_dict)

        data['video'] = vod_list
        return data