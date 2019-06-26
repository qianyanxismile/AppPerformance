# -*- coding: utf-8 -*-

import platform
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
from subprocess import Popen
import os


time_data = []
memory_data = []
cpu_data = []

# 每次先把tmp.txt文件删掉
if os.path.exists("tmp.txt"):
    os.remove("tmp.txt")
# 保证每次产生一条数据
with open("execute_time.txt", "w") as f:
    for _ in range(10):
        # 调用top命令
        # result = Popen("adb shell top -n 1 -b| {} com.jifen.qukan".format("findstr" if platform.system()=="Windows" else "grep"))
        result = os.system("adb shell top -n 1 -b| {} com.jifen.qukan >> tmp.txt".format("findstr" if platform.system()=="Windows" else "grep"))
        # 记录时间
        # f.write(str(datetime.now().timestamp())+"\n")
        time_data.append(datetime.now())

# 读取提取三列数据

with open("tmp.txt") as f:
    for line in f:
        columns = line.split()
        if columns[-1] == "com.jifen.qukan":
            memory_data.append(int(columns[5].strip().replace("M", "")) + int(columns[6].strip().replace("M", "")))
            cpu_data.append(float(columns[8].strip()))

# time_data = []
# with open("execute_time.txt")  as g:
#     for line in g:
#         time_data.append(datetime.fromtimestamp(float(line.strip())))


date_time = dates.date2num(time_data)
plt.subplot(1, 2, 1)
plt.plot(date_time, cpu_data, label="cpu", marker='o', markersize=15)

plt.legend()
plt.title("cpu line")

plt.subplot(1, 2, 2)
plt.plot(date_time, memory_data, color="blue", label="memory", marker="*", markersize=10)
plt.title("memory line")
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.legend()
plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y %H:%M:%S'))
plt.gca().xaxis.set_major_locator(dates.DayLocator())
plt.show()