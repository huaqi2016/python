#coding:utf-8

import subprocess
import os, sys, shutil

fList=['ivollo-tools-0.0.1-SNAPSHOT.jar','ivollo-data-access-0.0.1-SNAPSHOT.jar']
config=['RestAPIConfig.properties', 'jdbc.properties']
fnList=[]

#path=os.getcwd()
path='/opt/9iCloud/common_lib'
srcList = ['192.168.1.240','192.168.1.245']
dstList = ['192.168.22.62']
matchDict=dict(zip(fList, config))

for f in fList:
	filename, fileext=os.path.splitext(f)
	fnList.append(filename)
matchfDict=dict(zip(fList, fnList))

cpcmd='cp /opt/9iCloud/RestAPIConfig.properties /opt/9iCloud/common_lib/ivollo-tools-0.0.1-SNAPSHOT'
for k in matchfDict.keys():
	os.chdir(path)
	cmd = 'unzip '+ k +' -d '+matchfDict[k]
	os.system(cmd)
	if matchfDict[k] == 'ivollo-tools-0.0.1-SNAPSHOT':
		os.system(cpcmd)
	for i in srcList:
		modifycmd = 'sed -i "s/' + i + '/192.168.22.62/g" '+matchfDict[k]+'/'+matchDict[k] 
		#os.system(modifycmd)
		portcmd = 'sed -i "s/8888/8887/g" '+matchfDict[k]+'/'+matchDict[k] 
		#os.system(portcmd)
	os.chdir(path + '/' +matchfDict[k])
	jarcmd='/opt/9iCloud/third/java/jdk/bin/jar -cvf '+ k +' .'
	os.system(jarcmd)
	movecmd = 'mv ' + k +' ..'
	os.system(movecmd)
	#os.system('rm -rf '+path+ '/' +matchfDict[k])
	shutil.rmtree(os.path.join(path, matchfDict[k]), True)
