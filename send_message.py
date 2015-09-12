# -*- coding: utf-8 -*-
import time
import sqlite3
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
from email.utils import formataddr,parseaddr

def _format_addr(s):
  name, addr = parseaddr(s)
  return formataddr(( \
    Header(name, 'utf-8').encode(), \
    addr.encode('utf-8') if isinstance(addr, unicode) else addr))

sender = 'wh01096045@163.com' 
#receiver = '252878094@qq.com' 
receiver = '347881636@qq.com'  
subject = '来信了'  
smtpserver = 'smtp.163.com'
username = 'wh01096045@163.com'  
password = 'wc19941110' 
conn=sqlite3.connect("E:/test1.db")
sql = "CREATE TABLE IF NOT EXISTS Tieba(id integer PRIMARY KEY autoincrement,title varchar(100),time varchar(50),url varchar(100) UNIQUE)"

conn.execute(sql)
cs = conn.cursor()

id2 = 0
while 1==1:
	note = ''
	print u'<<<<<<<<<<<<<<<<<<<<<<<<go on>>>>>>>>>>>>>>>>>>>>>>>：'
	cs.execute("select max(id) from Tieba")
	for j in cs:
		id1 = j[0]
	print id1
	print id2
	try:

		if id1>id2:
			print id2
			cs.execute("select * from Tieba where id>%s"%id2)
			for i in cs:
				note1 = i
				note=note+note1[1]+" -- "+note1[2]+" -- "+note1[3]+'\n'
				print note

				print u"""
--------------------------------------------------------------------------------"""
			msg = MIMEText(note,_subtype='plain',_charset='utf-8')
			msg['Subject'] = Header(subject, 'utf-8') 
			msg['From'] = _format_addr(u'欢迎订阅我的贴吧动态 <%s>' % sender)
			msg['To'] = _format_addr(u'管理员 <%s>' % receiver)
			conn.commit()  #将加入的记录保存到磁盘，非常重要！
			smtp = smtplib.SMTP()  
			smtp.connect('smtp.163.com')  
			smtp.login(username, password)  
			smtp.sendmail(sender, receiver, msg.as_string())
			id2=id1
			time.sleep(60)
		else:
			time.sleep(60)
	except Exception:
			pass
cs.close()
conn.close()
smtp.quit()