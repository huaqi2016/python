#coding:utf-8
'''
@copyright: 2016 杭州九爱科技,Inc. All rights reserved.
@summary:  jar compare
@author: zhou shengqiang
'''

import os,sys,time,getopt,zipfile,tarfile,shutil,re
import paramiko
import subprocess
remoteList=[]
localList=[]
localPath=[]
chaList=[]
LocalDir=[]
LibBreak=[]
ListDir=[]
SameList=[]
logtxt = open('/opt/log.txt','a')

user="root"                                                                                                                                                                                                                                  
passwd="123456"
#host="192.168.22.62"
host=sys.argv[1]
port="22"
filename="pro.sh"
SCP_CMD_BASE = r"""
            expect -c "
            set timeout 1;
            spawn scp -P {port} /opt/{filename} {username}@{host}:/opt/{filename};
            expect *assword* {{{{send {password}\r }}}} ;
            expect *\r
            expect \r
            expect eof
            "
    """.format(username=user,password=passwd,host=host,port=port, filename=filename)

cmd = SCP_CMD_BASE.format(filename = filename)
print "cmd=", cmd
child = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
out = child.communicate()
print out

def ssh2(ip, username, passwd, cmd):
	global remoteList
	tmpList=[]
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip, 22, username, passwd, timeout=5)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		tmpList=stdout.read().split()
		for i in tmpList:
			filename, fileext = os.path.splitext(i)
			if fileext != '.jar':
				continue
			remoteList.append(i)
		#print remoteList
		ssh.close()
	except:
		print '%stErrorn'%(ip)

ssh2(sys.argv[1], 'root', '123456', 'sh /opt/pro.sh')

def recursion(path):
	dir_list=[]
	file_list=[]
	list_dirs = os.walk(path)
	for root, dirs, files in list_dirs:
		for d in dirs:
			dir_list.append(d)
		for f in files:
			filename, fileext = os.path.splitext(f)
			if fileext != '.jar':
				continue
			localList.append(f)
			localPath.append(os.path.join(root, f))
	#print localList 
	#print localPath

recursion('/opt/9iCloud/common_lib')
recursion('/opt/9iCloud/app/common_lib')
recursion('/opt/9iCloud/service/common_lib')

def fileCompare(local, remote):
	for i in local:
		if i not in remote:
			chaList.append(i)
	for j in remote:
		if j not in local:
			chaList.append(j)
	print chaList


def comparefile(dir1,dir2):
    global LocalDir,LibBreak,ListDir,SameList
    
    LibBreak = 0                    #错误jar包计数器
     
    for file1 in dir1:              #获取源文件列表，按-分隔成数组
        filename1,fileext = os.path.splitext(file1)
        arrfile1 = filename1.split("-")
 
        for file2 in dir2:          #获取目标文件列表，按-分隔成数组
            filetmp = 1
            filename2,fileext = os.path.splitext(file2)
            arrfile2 = filename2.split("-")
            
            if len(arrfile1) != len(arrfile2):      #按数组长度检查是否匹配
                continue
            
            for i in range(0,len(arrfile1)):        #检查字母段匹配
                if str(arrfile1[i])[0].isdigit() == False and str(arrfile2[i])[0].isdigit() == False:
                    if arrfile1[i] != arrfile2[i]:      
                        filetmp = 0
                        break
                if filetmp == 0:            #字母匹配失败跳出循环
                    print 'Info : No Same File。'
                    logtxt.write('Info : No Same File.')
                    logtxt.write('\n')
                    continue
                
                if str(arrfile1[i])[0].isdigit() == True and str(arrfile2[i])[0].isdigit() == True:     #检查数字段匹配
                    fileversion1 = arrfile1[i].split(".")       #按.分隔数组
                    fileversion2 = arrfile2[i].split(".")
                    
                    if len(fileversion1) == len(fileversion2):      #检查数组长度
                        if fileversion1 == fileversion2:            #数组内容相同与否输出
                            logtxt.write('\n')
                            SameList.append(file1)
                        elif fileversion1 > fileversion2:
                            LibBreak += 1
                            print '---------'
                            print 'Warning : ' + 'SourceFile is too new ! [Sourcefile] ' + file1
                            print '---------'
                            logtxt.write('---------')
                            logtxt.write('Warning : ' + 'SourceFile is too new ! [Sourcefile] ' + file1)
                            logtxt.write('\n')
                            logtxt.write('---------')
                            logtxt.write('\n')
                        elif fileversion1 < fileversion2:
                            LibBreak += 1
                            print '---------'
                            print 'Warning : ' + 'SourceFile is too old ! [Sourcefile] ' + file1
                            print '---------'
                            logtxt.write('---------')
                            logtxt.write('Warning : ' + 'SourceFile is too old ! [Sourcefile] ' + file1)
                            logtxt.write('\n')
                            logtxt.write('---------')
                            logtxt.write('\n')

comparefile(localList, remoteList)

localNotSame = [val for val in localList if val not in SameList]    #locaNotSame 是localList与SameList的差集
remoteNotSame = [val for val in remoteList if val not in SameList]  #remoteNotSame 是remoteList与SameList的差集
print localNotSame
logtxt.write('----------')
logtxt.write('\n')
for i in localNotSame:
	logtxt.write('local exist, and remote not exist list'+i+'\n')
logtxt.write('----------')

