# -*- coding: utf-8 -*-

import platform
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
from subprocess import Popen
import matplotlib.ticker as mticker
import os


def generate_data(times=10):
    """生成性能分析数据
    """
    time_data = []
    # 每次先把tmp.txt文件删掉
    if os.path.exists("tmp.txt"):
        os.remove("tmp.txt")
    # 保证每次产生一条数据
    with open("execute_time.txt", "w") as f:
        for _ in range(times):
            # 调用top命令
            # result = Popen("adb shell top -n 1 -b| {} com.jifen.qukan".format("findstr" if platform.system()=="Windows" else "grep"))
            result = os.system("adb shell top -n 1 -b| {} com.jifen.qukan >> tmp.txt".format("findstr" if platform.system()=="Windows" else "grep"))
            # 记录时间
            # f.write(str(datetime.now().timestamp())+"\n")
            time_data.append(datetime.now())

    return time_data

def gather_statistic_data():
    """从统计结果中提取相应信息
    """
    memory_data = []
    cpu_data = []

    with open("tmp.txt") as f:
        for line in f:
            columns = line.split()
            if columns[-1] == "com.jifen.qukan":
                memory_data.append(int(columns[6].strip().replace("M", "")) + int(columns[6].strip().replace("M", "")))
                cpu_data.append(float(columns[8].strip()))

    return cpu_data, memory_data
# time_data = []
# with open("execute_time.txt")  as g:
#     for line in g:
#         time_data.append(datetime.fromtimestamp(float(line.strip())))

def visualization(x, y, current_number, label_name, title):
   
    plt.subplot(2, 2, current_number)
    plt.plot(x, y, label=label_name, marker='o', markersize=5,color='r')
    plt.legend(loc="upper right")
    plt.title(title)


def main():
    time_data = generate_data()
    cpu_data, memory_data = gather_statistic_data()
    date_time = dates.date2num(time_data)
    visualization(date_time,  cpu_data, 1, "cpu", "CPU Usage")
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f %%'))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(dates.DayLocator())
    
    visualization(date_time, memory_data, 3, "memory", "memory usage")
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f MB'))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(dates.DayLocator())
    plt.show()


if __name__ == "__main__":
    main()
