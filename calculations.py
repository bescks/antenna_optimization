import csv
from numpy import median

filename = "/Users/gengdongjie/WorkSpace/Bitbucket/optimization_antenna/data4/" \
           "data-20180611 14:07-pt-office-room11-1m-a2-b1--16dbm-2.csv"

rssi = []
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for row in reader:
        rssi.append(int(row[-1]))
print("原始数据有 %s个" % len(rssi))
avg = sum(rssi) / len(rssi)
print("平均值 %s" % avg)
print("中位数 %s" % median(rssi))

rssi_top = []
for r in rssi:
    if r > avg:
        rssi_top.append(r)
print("平均值截取后的中位数%s" % median(rssi_top))
rssi.sort(reverse=True)
num5 = 500 * 0.05
num10 = 500 * 0.10
num15 = 500 * 0.15
num20 = 500 * 0.2
print("前百分之5中位数%s" % median(rssi[0:int(num5)]))
print("前百分之10中位数%s" % median(rssi[0:int(num10)]))
print("前百分之15中位数%s" % median(rssi[0:int(num15)]))
print("前百分之20中位数%s" % median(rssi[0:int(num20)]))
