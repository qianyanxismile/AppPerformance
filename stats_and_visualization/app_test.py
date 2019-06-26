# -*- coding: utf-8 -*-

import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import dates


time_data=[]
# 保证每次产生一条数据
with open("execute_time.txt", "a") as f:
    for _ in range(10):
        # 调用top命令
        os.system("adb shell top -n 1 -b|grep com.jifen.qukan>>tmp.txt")
        # 记录时间
        f.write(str(datetime.now().timestamp())+"\n")
#         time_data.append(datetime.now())
        #f.write("\n")

# 读取提取三列数据
memory_data = []
cpu_data = []
with open("tmp.txt") as f:
    for line in f:
        columns = line.split()
        if columns[-1] == "com.jifen.qukan":
            memory_data.append(int(columns[6].strip().replace("M", "")))
            cpu_data.append(float(columns[8].strip()))


with open("execute_time.txt")  as g:
    for line in g:
        time_data.append(datetime.fromtimestamp(float(line.strip())))
#         time_data.append(datetime.now())

date_time = dates.date2num(time_data)   #date2num将日期转换为matplotlib格式
#fig = plt.figure()#定义一个画布，分辨率设置为80
plt.subplot(1,2,1)#创建一个1行2列子图，图样绘制在第一块
plt.plot(date_time,cpu_data, color="green",linewidth=1.0,linestyle="--")
plt.title("cpu line")   #设置标题 
plt.xlabel("time")#设置x标签
plt.ylabel("cpu")#设置y标签
#plt.legend(loc="upper right")#设置图例
#plt.show()


#plt.figure(dpi=80)#定义一个画布，分辨率设置为80
plt.subplot(1,2,2)#创建一个子图，图样绘制在第二块
plt.plot(date_time,memory_data, color="blue",linewidth=1.0,linestyle="*",label="memory")
plt.title("memory line")   #设置标题 
plt.xlabel("time")#设置x标签
plt.ylabel("memory")#设置y标签
plt.legend(loc="upper right")#设置图例
plt.show()


#绘制图
#date_time = dates.date2num(time_data)
#plt.plot_date(date_time, cpu_data)
#plt.title("cpu line")

#plt.plot_date(date_time, memory_data)
#plt.title("memory line")
