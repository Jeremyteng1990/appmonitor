# -*- coding: utf-8 -*-
import ConfigParser
import string
import wmi
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib,datetime
import time
import os,shutil
import codecs
import psutil
import re
import gc,sys
import objgraph





######   删除BOM     #####
def	delbom(file):
	data = open(file).read()
	if data[:3] == codecs.BOM_UTF8:
		data = data[3:]
		f = open(file,'w')
		f.write(data)
		f.close()
		
		
#####    写日志内容      ###### 
def  writetext():
	logname = 'applog'+ time.strftime("%Y%m%d") + '.txt'
	fp = open(logname,'a')
	logtext = 'app is restart ,mail have send' + str(datetime.datetime.now()) + '\n'
	fp.write(logtext)
	fp.close()
	os.chdir(path)
	
	
#####    重启app     #######	
def startapp(dir):
	dir = '\"' + dir + '\"'
#	os.system(dir)
	os.startfile(dir)


#####   日志   ######## 	
def log():
	logdir = []
	logdir = os.listdir(path)
	if 'log' in logdir and os.path.isdir('log'):
		os.chdir('.\\log')
		writetext()
	elif 'log' in logdir and  os.path.isfile('log'):
		os.remove('.\\log')
		os.mkdir('log')
		os.chdir('.\\log')
		writetext()
	else:		
		os.mkdir('log')
		os.chdir('.\\log')
		writetext()
			
			

######      发邮件       #######
def sendmail():
	msg = MIMEText(mailtext, 'plain', 'utf-8')
	msg['From'] = from_addr
	to_addr = []
	to_addr = to.split(',')
	msg['To'] = to
	msg['Subject'] = Header(mailtitle, 'utf-8').encode()
	server = smtplib.SMTP(smtp_server, 25)   
	server.login(from_addr, passwd)
	server.sendmail(from_addr, to_addr, msg.as_string())
	server.quit()
	log()
	



def memdect(each_pro,eachmem):
		rss,vms = each_pro.get_memory_info()
		if rss > eachmem:
			each_pro.kill()
		else:
			return
	




#####     	
def  sortpro(eachapp,eachmem):
	all_pro = psutil.get_process_list()
	for each_pro in all_pro:
		r_each_pro = str(each_pro)
		pro_n = re.search(r'\'.+\..+\'',r_each_pro)	
		if pro_n:
			p_ln = pro_n.group()
			p_ln = p_ln[1:-1]
			if p_ln.lower() == eachapp:
				memdect(each_pro,eachmem)
			else:
				pass
		else:
			pass
	gc.collect()
	f1 = open("D:\\pylog.txt",'a')
	sys.stdout = f1
	objgraph.show_most_common_types(limit=30)
	print "================================="
	return




def prolst():
	c = wmi.WMI()
	Prolist = []
	for process in c.Win32_Process():
		Prolist.append(str(process.Name).lower())
	return Prolist



		
	
	
	

def main(applst,apppathlst,memlst):
	n = 0
	Prolist = prolst()
	for eachapp in applst:
		eachapp = eachapp.lower()
		if eachapp in Prolist:
			eachmem = int( memlst[n])
			eachmem = eachmem * 1024 * 1024
			sortpro(eachapp,eachmem)
		else:
			sendmail()
			startapp(apppathlst[n])
		n = n + 1
	return
		
		
		
path = os.getcwd()
dirpath = path + '\\config.ini'
config = ConfigParser.ConfigParser()
delbom(dirpath)
config.read(dirpath)
from_addr = config.get('email','fromm')
from_name = config.get('email','fromn')
passwd = config.get('email','pass')
smtp_server = config.get('email','smtp')
to = config.get('email','to')
mailtext = config.get('email','mailtext')
mailtitle = config.get('email','mailtitle')
app = config.get('app','appname')
apppath = config.get('app','apppath')		
mem = config.get('app','maxmem')
applst = app.split(',')
apppathlst = apppath.split(',')
memlst = mem.split(',')




if __name__ == "__main__": 
    while True: 
		main(applst,apppathlst,memlst)
		time.sleep(1)

	