#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-8-14 下午2:38
# @Author  : xiaofang
# @Site    : 
# @File    : get_info.py
# @Software: PyCharm Community Edition
"""
从拉勾网获取python爬虫全国职位信息并直接存入mongodb数据库
"""
import requests
import json
from fake_useragent import UserAgent
import time
import pymongo

ua = UserAgent() #使用随机请求头防止被封

class Lagou():
	"""
	a class to get all job info
	"""
	page = 1000  #你想抓取的页数默认设置1000页目的是采集所有相关页面（普遍职位超不过1000页的信息）
	header = {'User-Agent': ua.random}

	def get_all(self):
		"""
		因为电脑版网页比较难爬取，所以选择手机版网页
		"""
		for i in range(1,self.page):
			page_url = 'https://m.lagou.com/search.json?city=%E5%85%A8%E5%9B%BD&positionName=python%E7%88%AC%E8%99%AB&pageNo=' + str(i) + '&pageSize=15'
			time.sleep(2)
			r  = requests.get(page_url, headers=self.header)
			status = r.status_code

			if status == 200:
				html = r.text
				result = json.loads(html)
				info = result['content']['data']['page']['result']
				if info == []:
					return

				else:
					for item in info:
						mongo = pymongo.MongoClient()
						collections = mongo.lagou.pythoner_job
						collections.insert_one(item)
						print("数据成功采集并插入数据库")

if __name__ == "__main__":
	lagou = Lagou()
	lagou.get_all()

for i in range(1,20):
	print(i)