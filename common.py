# -*- coding:utf-8 -*-
import MySQLdb
import requests
import requesocks
import random

from xml.etree import ElementTree as et
from config import *


#获得数据库连接对象
def init_client():
    db = MySQLdb.connect(
                            host="127.0.0.1",
                            port=3306,
                            user="root",
                            passwd="305405",
                            db="dianying",
                            charset="utf8"
                         )
    return db


# 根据是否使用tor代理，来获取http客户端
def get_http_client():
    if HTTP_CONFIG['use_tor_proxy']:
        session = requesocks.session()
        session.proxies = {'http': 'socks5://127.0.0.1:%d' % HTTP_CONFIG['tor_proxy_port'],
                           'https': 'socks5://127.0.0.1:%d' % HTTP_CONFIG['tor_proxy_port']}
        return session
    else:
        return requests.session()


# 发送get请求
def get_body(url):
    retry_times = 0
    client = get_http_client()
    while retry_times < 5:
        try:
            content = client.get(url, headers=random.choice(HEADERS), timeout=HTTP_CONFIG['timeout']).content
            return content
        except:
            retry_times += 1
    return ''

# 检查播放器组
def check_p(**k):
    isck = False
    for g in PLAY_GROUP:
        if k['flag'].find(g) > -1:
            if k['dd'].find(g) > -1:
                isck =  True
    return isck


# 根据电影类型查询对应的序列号id
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
        root = et.XML(xmlbody)
        et_list = root.getiterator("list")
        et_vod_list = root.getiterator("video")
        et_ty_list = root.getiterator("ty")

        vod_dict = et_list[0].attrib
        # 解析电影分类
        vod_class = {}
        for et_ty in et_ty_list:
            vod_class[et_ty.text] = et_ty.attrib["id"]

        vod_dict["class"] = vod_class
        # 解析电影列表
        for et_vod in et_vod_list:
            vod = {}
            for cd in et_vod:
                vod[cd.tag] = cd.text
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
        try:
            vod_list = []
            root = et.XML(xmlbody)
            et_vod_list = root.getiterator("video")
            et_list = root.getiterator("list")
            # 获取list节点的属性参数
            data = et_list[0].attrib

            for et_vod in et_vod_list:
                vod_dict = {}
                cd_list = et_vod.getchildren()
                if not len(cd_list):
                    break
                for cd in cd_list:
                    if cd.tag == "dl":
                        dl_list = []
                        for et_dd in cd.getchildren():
                            dl_dict = et_dd.attrib
                            dl_dict[et_dd.tag] = et_dd.text if et_dd.text is not None else ""
                            dl_list.append(dl_dict)
                        vod_dict["dl"] = dl_list
                        continue

                    vod_dict[cd.tag] = cd.text

                vod_list.append(vod_dict)

            data['video'] = vod_list

            return data
        except:
            return {"pagecount": 0, "recordcount": 0, "video": []}

