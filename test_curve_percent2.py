import csv
from numpy import median

filename = "/Users/gengdongjie/WorkSpace/Bitbucket/optimization_antenna/data5/" \
           "data-20180611 17:14-pt-office-room11-1m-a2-b5--20dbm-3.csv"

rssi = []
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for row in reader:
        rssi.append(int(row[-1]))
print("原始数据有 %s个" % len(rssi))
avg = sum(rssi) / len(rssi)
print("平均值 %s" % avg)

rssi.sort(reverse=True)

num5 = 500 * 0.05

rssi_remain = rssi[int(num5):]
num_remain10 = len(rssi_remain) * 0.10
num_remain15 = len(rssi_remain) * 0.15

median10 = median(rssi_remain[:int(num_remain10)])
median15 = median(rssi_remain[:int(num_remain15)])
print("截取后百分之10中位数 %s" % median10)
print("截取后百分之15中位数 %s" % median15)
print("平均值 %s" % ((median10 + median15) / 2))