#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Filename: 
# Author: Bowen
# Create at 2017\9\29 0029


import logging

class Logger:
    def __init__(self, path, name, clevel = logging.ERROR,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        #设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        #设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message):

        self.logger.warn(message)

    def error(self,message):
        self.logger.error(message)

    def cri(self,message):
        self.logger.critical(message)

if __name__ =='__main__':
    logyyx = Logger('yyx.log', 'logger', logging.WARNING,logging.DEBUG)
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.warn('一个warning信息')
    logyyx.error('一个error信息')
    logyyx.cri('一个致命critical信息')
