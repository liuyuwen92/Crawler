#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Filename:
# Author: Bowen
# Create at 2017\9\23 0023
import time,sys,os
from multiprocessing import Process
from common import *
from config import *
from logger import *

reload(sys)
sys.setdefaultencoding('utf-8')

logger = Logger('crawler%s.log' % time.strftime('%Y%m%d%H',time.localtime(time.time())), 'main', logging.INFO, logging.DEBUG)

# 初始化Mysql数据库
db = init_client()
cur = db.cursor()


def main(flag="", max=None, hour=None):

    if flag == "":
        try:
            flag = sys.argv[1]
        except:
            print("必选参数flag:{}\tmax:可选参数、数值类型、要抓取多少页\thour:可选参数、数值类型、获取每天的数据hour=24".decode('utf-8').format(API_.keys()))
            return

    try:
        max = sys.argv[2]
    except:
        pass

    try:
        hour = sys.argv[3]
    except:
        pass

    run(flag, API_[flag], max, hour,)

    db.close()
    cur.close()
    print "All crawling are finished."


def run(flag, url, max, hour):

    # 获取接口初始数据
    url_c = '{}?ac=videolist'.format(url)

    # 获取最新抓取列表
    c_body = get_body(url_c)

    if c_body == "":
        logger.cri('[%s]初始化失败，网络错误。[URL:%s]'.decode('utf-8') % (flag, url_c))
        return

    vod_list = parse_video(c_body)

    rd = int(vod_list['recordcount'])
    pt = int(vod_list['pagecount'])

    if max <> None:
        max = pt if int(max) > pt else int(max)
    elif max == None:
        max = pt
    else:
        max = int(max)

    hour = str(hour) if hour <> None else ""

    if rd == 0:
        logger.warn('[%s]当前api接口资源记录为空，暂无更新。'.decode('utf-8') % flag)
        return
    logger.debug("max:{}".format(max))
    c = consume()
    produce(c, flag, url, max, hour).next()


def get_data(url):
        body = get_body(url)
        if body == "":
            logger.cri('获取数据失败，接口失效或访问受限[get_body is None][URL:%s]'.decode('utf-8') % url)
            return []
        data = parse_video(body)['video']
        return data


def produce(c, apiflag, apiurl, max, hour):
    """抓取任务列表data
    max:采集总页数
    hour:采集日期
    """
    c.next()
    data = []
    n = 0
    while n < max:
        n = n + 1
        url = '{}?ac=videolist&pg={}&h={}'.format(apiurl, n, hour)
        logger.debug("[PRODUCER-%s]page:%s:crawling...%s" % (apiflag, n, url))

        data = get_data(url)
        if data:
            c.send(data)

        # except StopIteration, e:
        #     logger.error("{}".format(repr(e)))
        #     raise

        logger.debug("[PRODUCER-%s]page:%s:crawling finished." % (apiflag, n))

        logger.info("[PRODUCER-%s]采集次数:%s,新增入库:%s条,新增加播放组:%s条,更新播放组:%s条。".decode('utf-8') %
                     (apiflag, G.running, G.crawled_num, G.update_group_num, G.update_num))
    c.close()
    yield


def consume():
    '''produce生产完的数据传到这负责提取数据并保存数据库中'''
    r = ''
    while True:
        data = yield
        if not data:
            return
        for _item in data:
            G.running += 1
            # 保存数据
            add_items(**_item)
            time.sleep(0.00000001)


def add_items(**k):
        '''添加电影记录到数据库'''

        # 不允许None类型字段,过滤特殊字符
        for key,value in k.items():
            if value is None:
                k[key] = ""
            elif isinstance(value, basestring):
                k[key] = value.strip().strip(',').strip('$')
            else:pass


        # 构造数据库字段变量
        item_type = k.get('type', '')
        name = k.get('name', '')
        pic = k.get('pic', '')
        actor = k.get('actor', '')
        director = k.get('director', '')
        area = k.get('area', '')
        year = k.get('year', '')
        state = int(k.get('state', 0))
        note = k.get('note', '')
        des = k.get('des', '')
        last = k.get('last', '')
        dl = k.get('dl', [{'flag':'','dd':''}])

        flag = ""
        dd = ""
        i = 0
        for _ in dl:
            # 校验播放组是否合法
            if not check_p(**_):
                logger.error("[CONSUMER-{}]播放组不合法:{}".decode('utf-8').format(G.running, _))
                return
            if i == 0:
                flag = _['flag']
                dd = _['dd']
                continue
            flag = flag + '$$$' + _['flag']
            dd = dd  + '$$$' + _['dd']
            i += 1


        # 这三个字段的数据不完整将跳过采集
        if name == "" or pic == "" or dd == "" or flag == "":
            logger.error('[Process-{0}][CONSUMER-{1}]数据不完整，跳过。'.decode('utf-8').format(os.getpid(), G.running))
            return

        flag = flag.strip('$')
        dd = dd.strip('$')

        # 绑定分类采集
        tid = find_tid(item_type)
        if tid == None:
            logger.warn('[CONSUMER-%s][%s]%s...未绑定分类，跳过。'.decode('utf-8') % (G.running, item_type, name))
            return

        # 检测数据是否已经存在
        cx_sql = "SELECT d_name, d_playfrom, d_playurl FROM vod_vod WHERE d_name = '%s'" % name

        cur.execute(cx_sql)
        data = cur.fetchone()
        if data <> None:
            if data[1].find(flag) > -1:
                if data[2].find(dd) > -1:
                    logger.warn('[CONSUMER-%s][%s]%s...地址相同，跳过。'.decode('utf-8') % (G.running, item_type, name))
                    return

            flag1 = data[1].split('$$$')
            dd1 = data[2].split('$$$')

            info = "[CONSUMER-{}]{}...".decode('utf-8').format(G.running, name)

            for i in dl:
                if i['flag'] in flag1:
                    if i['dd'] in dd1:
                        info = info + "播放组(%s) 无需更新,".decode('utf-8') % i['flag']
                    else:
                        gx_sql = "REPLACE INTO VOD_VOD (d_playurl) VALUES (%s)"
                        val_list = (i['dd'])
                        try:
                            # 执行SQL语句
                            cur.execute(gx_sql, val_list)
                            # 提交到数据库执行
                            db.commit()
                            # 更新数量
                            G.update_num += 1

                            info = info + "播放组(%s) 更新成功,".decode('utf-8') % i['flag']

                        except Exception, e:
                            db.rollback()
                            logger.error('%s' % repr(e))

                else:
                    val_list = (data[1]+"$$$"+i['flag'], data[2]+"$$$"+i['dd'], name)
                    gx_sql = "UPDATE VOD_VOD SET d_playfrom = '%s', d_playurl = '%s' WHERE d_name = '%s'" % val_list

                    try:
                        # 执行SQL语句
                        cur.execute(gx_sql)
                        # 提交到数据库执行
                        db.commit()
                        # 新增播放组数量
                        G.update_group_num += 1

                        info = info + "新增加播放组(%s) 入库成功,".decode('utf-8') % i['flag']

                    except Exception, e:
                        db.rollback()
                        logger.error('%s' % repr(e))


            logger.info('%s' % info)

            return

        sql_val = (name,pic,actor,director,area,year,last,des,flag,dd,tid,note)
        # SQL 插入语句
        sql = "INSERT INTO vod_vod VALUES (id, %s, %s, %s, %s, %s, %s, 0, 0, %s, %s, %s, %s, '', %s, %s)"
        try:
            # 执行sql语句
            cur.execute(sql, sql_val)
            # 提交到数据库执行
            db.commit()

            G.crawled_num += 1
            logger.info('[CONSUMER-%s][%s]%s...新加入库，成功。'.decode('utf-8') % (G.running, item_type, name))

        except Exception, e:
            db.rollback()
            logger.error('%s' % repr(e))


class G(object):
    # 新增入库数量
    crawled_num = 0
    # 更新数量
    update_num = 0
    # 新增播放组数量
    update_group_num = 0
    # 采集次数
    running = 0


if __name__ == "__main__":
    main()

