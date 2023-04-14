#!/usr/bin/env python3

import socket
import sys
import os
import re
import signal
import hashlib


STATUS_OK=(100,b'OK')
STATUS_BAD_REQUEST=(200,b'Bad request')
STATUS_NO_SUCH_MAILBOX=(203,b'No such mailbox')
STATUS_NO_SUCH_MESSAGE=(201,b'No such message')
STATUS_READ_ERROR=(202,b'Read error')
STATUS_UNKNOWN_METHOD=(204,b'Unknow method')

def send_response(f,status,method,heads,content):
	f.write(b'%d %s\n' % status)
	if method=='LS':
		f.write(b'Number-of-messages: %d\n\n' % heads)
		for line in content:
			f.write(b'%s\n' % line.encode())
	else :
		if method=='READ':
			f.write(b'Content-length:%d\n' % heads) 
		content=str(content)
		for line in content:
			f.write(b'%s' % line.encode())
	f.write(b'\n')
	f.flush()
	return	

def read_request(f):
	lines=[]
	heads=[]
	content1=[]
	
	method=f.readline().decode('ascii')
	method=method.strip()
	
	if method not in METHODS:
		return STATUS_UNKNOWN_METHOD,[],[]
	
	line=f.readline().decode('ascii')
	line=line.strip()
	heads.append(line)
	
	if method=='LS':
		line=f.readline()
		return method,heads,[]
	else:
		line=f.readline().decode('ascii')
		line=line.strip()
		heads.append(line)
	
		line=f.readline()
	
		if not heads:
			return STATUS_BAD_REQUEST,[],[]
	
	
		if heads[1].split(':')[0]=='Content-length':
			num=int(heads[1].split(':')[1])
			content=f.readline(num)
			return method,heads,content
		elif heads[1].split(':')[0]!='Message':
			return STATUS_BAD_REQUEST,[],[]
		else:
			return method,heads,[]

	

def method_WRITE(heads,content):
	#kontrola hlavicky
	mbox=heads[0].split(':')[1]
	if '/' in mbox:
		return STATUS_BAD_REQUEST,[],[]
	if heads[1].split(':')[0]!='Content-length':
		return STATUS_BAD_REQUEST,[],[]
	if int(heads[1].split(':')[1])<0:
		return STATUS_BAD_REQUEST,[],[]
	#ak mailbox neexistuje
	if not os.path.exists(mbox):
		return STATUS_NO-SUCH_MAILBOX,[],[]
	m=hashlib.md5()
	m.update(b'{content}')
	m.hexdigest()
	mbox=heads[0].split(':')[1]
	with open(f'{mbox}/{m.hexdigest()}',mode='bw') as f:
		f.write(content)
	f.close()
	return STATUS_OK,[],[]

def method_READ(heads,content):
	mbox=heads[0].split(':')[1]
	mbox2=heads[1].split(':')[1]
	#kontrola hlavicky
	if '/' in mbox2:
		return BAD_REQUEST,[],[]
	#ak sprava alebo mailbox neexistuje
	try:	
		with open(f'{mbox}/{mbox2}',mode='rb') as f1:
			content=f1.read()
	except FileNotFoundError:
		return STATUS_NO_SUCH_MESSAGE,[],[]
	except OSError as error:
		return STATUS_READ_ERROR,[],[]
	f1.close()
	#sprava sa neda precitat
	return STATUS_OK,len(content),content

def method_LS(heads,content):
	#kontrola hlavicky
	mbox=heads[0].split(':')[1]
	if '/' in mbox:
		return BAD_REQUEST,[],[]
	if not heads:
		return STATUS_BAD_REQUEST,[],[]
	#ci existuje
	try:
		with os.scandir(mbox) as entries:
			content_n=os.listdir(mbox)
	except FileNotFoundError:
		return STATUS_NO_SUCH_MAILBOX,[],[]
	for line in content_n:
		content.append(line)
	return STATUS_OK,len(content),content
	

def handle_request(method,heads,content):
	if method in METHODS:
		return METHODS[method](heads,content)
	elif method not in METHODS:
		return STATUS_BAD_REQUEST,[],[]

METHODS={
	'WRITE':method_WRITE,
	'READ':method_READ,
	'LS':method_LS,
}	

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',9999))
s.listen(5)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
	cs,address=s.accept()
	print('spojil sa',address)
	pid_child=os.fork()
	if pid_child==0:
		s.close()
		f=cs.makefile(mode='rwb',encoding='utf-8')
		while True:
			#precita poziadavku
			method,heads,content=read_request(f)
			#ak neni metoda
			if not method:
				send_response(f,STATUS_UNKNOWN_METHOD,[],[])
				break
			#vybavi poziadavku
			status,heads,reply_content=handle_request(method,heads,content)
			if status[0]!=100:
				f.write(b'%d %s\n' % status)
				break
			send_response(f,status,method,heads,reply_content)
		f.close()
		cs.close()
		sys.exit(0)
	else:
		cs.close()
				
