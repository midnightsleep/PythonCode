# -*- coding: utf-8 -*- 
import urllib2
import re
import sqlite3
import time
import global_variable
import threading
	
def find_message():
	#连接数据库
	conn=sqlite3.connect("E:/test.db")
	#创建表
	sql = "CREATE TABLE IF NOT EXISTS Tieba(id integer PRIMARY KEY autoincrement,title varchar(100),time varchar(50),url varchar(100) UNIQUE)"
	#执行建表语句
	conn.execute( sql )
	cs = conn.cursor()
	#循环
	while True:
		print '<<<<<<<<<<<<<<<<<<<<<<<<go on>>>>>>>>>>>>>>>>>>>>>>>:'
		#page表示页码
		page=1

		while page<10:
			#打印循环次数
			print 'start: '+str(global_variable.foreach)			
			#读取网页源代码
			response=urllib2.urlopen('http://tieba.baidu.com/f/search/ures?kw=&qw=&rn=10&un='
				+chaxun_id+'&only_thread=&sm=1&sd=&ed=&pn='+str(page))
			html=response.read()
			#使用正则表达式获取数据
			#发帖主题
			myItems = re.findall('_blank" >.*?</a>',html)
			#发帖时间
			myTimes = re.findall('date">.*?</font>',html)
			#帖子url
			myHrefs = re.findall('bluelink" href=".*?"',html)			
			#记录数据条数
			message=1
			try:						
				for i in myItems:
					print u""" 
------------------------------------------------------------------------------   """
					#主题切片
					message_title=i[15:-4]
					#时间切片
					message_time=myTimes[message-1][6:-7]
					#url切片
					message_url="http://tieba.baidu.com"+myHrefs[message-1][16:-1]

					#将title转成gb2312格式，因为命令提示行与sqlite都是gb2312编码
					message_title = unicode(message_title,"gb2312")
					#将数据插入到数据库
					cs.execute("INSERT INTO Tieba values(null,?,?,?)",(message_title,message_time,message_url))
					#将加入的记录保存到磁盘，非常重要！
					conn.commit() 

					print str(message)+":TITLE:  "+message_title
					print "  TIME :  "+message_time
					print "  URL  :  "+message_url
					#打印一次，记录加1
					message=message+1
					#循环次数加1
					global_variable.foreach=global_variable.foreach+1
					if message>10:
						break
			except Exception:
				global_variable.foreach=int(global_variable.foreach)+1
				pass
			#程序一直运行不需要关闭数据库	
			# cs.close()
			# conn.close()
			#延时60秒
			time.sleep(10)

if __name__=='__main__':
	print u"""  
------------------------------------------------------------------------------  
   程序：贴吧爬虫  
   版本：V1.1  
   作者：wh01096046 
   日期：2015/8/10
   语言：Python 2.7.9

------------------------------------------------------------------------------ 
"""  
	print 'Enter id:'
	chaxun_id=raw_input()
	find_message()