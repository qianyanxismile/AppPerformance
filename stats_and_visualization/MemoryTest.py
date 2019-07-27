#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-26 11:16
# @Author  : Rocky Zhao
import subprocess
import re
import time
import pandas as pd


# 执行shell
def shell(cmd):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    (stdout_output, err_output) = p.communicate()
    if err_output is not None and len(err_output) != 0:
        print("Shell err_output: " + str(err_output))
    # print(str(stdout_output))
    return str(stdout_output)


def data_resolve():
    data_origin = shell('adb shell dumpsys meminfo com.jifen.qukan')
    # 通过正则拿到各个内存的数据
    java_heap = int(re.findall(r"Java Heap:(.+?)\\n", data_origin)[0])
    native_heap = int(re.findall(r"Native Heap:(.+?)\\n", data_origin)[0])
    graphics = int(re.findall(r"Graphics:(.+?)\\n", data_origin)[0])
    # unknown比较特殊，单独处理
    unknown_string = re.findall(r"Unknown(.+?)\\n", data_origin)[0]
    unknown = int(re.findall(r'\d+', unknown_string)[0])
    total = int(re.findall(r"TOTAL:(.+?)TOTAL", data_origin)[0])
    return java_heap, native_heap, graphics, unknown, total


def df_append():
    n = 60
    df = pd.DataFrame(index={'java_heap': 0, 'native_heap': 0, 'graphics': 0, 'unknown': 0, 'total': 0},
    columns=['suggestion', 'average'])
    file = '/Users/wangqianwen/Desktop/test.csv'
    while n > 0:
        now = time.strftime('%m.%d %H:%M:%S ', time.localtime(time.time()))
        df[now] = list(data_resolve())
        time.sleep(1)
        n = n-1
    plt.plot(time.localtime(time.time()),df(now))
    plt.show()
    df.to_csv(file)


if __name__ == "__main__":
    df_append()
