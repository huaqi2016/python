#coding=utf-8
import os, sys, re
__author__ = 'zhoushengqiang'
expectDict={'APPKEY':sys.argv[1], 'APP_CLIENT_ID':sys.argv[2], 'APP_CLIENT_SECRET':sys.argv[3]}
fileList=[]
noSpaceList=[]
noNullLineList=[]
expectList=[]
modifyList=[]
regList=expectDict.keys()
regexpress='|'.join(regList)
f = open('/opt/9iCloud/common_lib/ivollo-tools-0.0.1-SNAPSHOT/RestAPIConfig.properties', 'r')
for l in f.readlines():
    fileList.append(l)
f.close()
'''
reg=re.compile('^#')
pattern=re.compile('\s+')
for line in fileList:     #从文件读出文件行list
    m = reg.match(line)
    if m is None:
        newline=re.sub(pattern, '', line)
        noSpaceList.append(newline)
for i in noSpaceList:
    if i not in ['', '\n']:
        noNullLineList.append(i)
'''
###字典转换list
for k in expectDict.keys():
    modifyList.append(k+'='+expectDict[k]+'\n')
#print modifyList  #要修改的line

for l in fileList:
    reg=re.compile(regexpress)
    m=reg.search(l)
    if m is None:
        expectList.append(l)
#print expectList  #不需要修改的line

#找到插入位置
indexList=[]
for r in regList:
    index=0
    reg=re.compile(r)
    for l in fileList:
        m=reg.search(l)
        index=index+1
        if m is not None:   #匹配到后，跳出循环
            break
    indexList.append(index)

#插入位置与插入值的map
d=dict(zip(indexList, modifyList))
for item in indexList:
    expectList.insert(item-1, d[item])
#print expectList   #最终要写入的文件内容

f=open('/opt/9iCloud/common_lib/ivollo-tools-0.0.1-SNAPSHOT/RestAPIConfig.properties', 'w')
for l in expectList:
    f.write(l)
f.close()
