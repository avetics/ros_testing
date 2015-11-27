#!/usr/bin/env python
import csv
import sys

csv_joy = []
csv_rcin = []
offset = 0

def load_gps_joy():
    global csv_joy
    with open('/home/jinahadam/catkin_ws/src/testing/gps_joy.csv', 'rb') as f:
        reader = csv.reader(f)
        csv_joy = list(reader)

def load_rcin():
    global csv_rcin
    with open('/home/jinahadam/catkin_ws/src/testing/rc_in.csv', 'rb') as f:
        reader = csv.reader(f)
        csv_rcin = list(reader)
    

load_gps_joy()
load_rcin()
print("Joy  Records: "+str(len(csv_joy)))
print("RcIn Records: "+str(len(csv_rcin)))


if len(sys.argv) > 1:
    offset = int(sys.argv[1])   
else:
   pass

def offset_calc(val):

    k = val
    matched = 0
    no_match = 0
    for line in csv_joy:
        if k < len(csv_rcin):
            data = csv_rcin[k]
            channel_3 = round(float(line[1])-float(data[1]),2)
            channel_1 = round(float(line[2])-float(data[2]),2)
            channel_0 = round(float(line[3])-float(data[3]),2)
            channel_2 = round(float(line[4])+float(data[4]),2)
            k = k + 1
            if channel_3 < 0.01 and channel_1 < 0.01 and channel_0 < 0.01 and channel_2 < 0.01:
                matched = matched + 1
            else:
                no_match = no_match + 1
    return matched

def conversion_loss_calc(val):

    k = 1
    matched = 0
    no_match = 0
    for line in csv_joy:
        if k < len(csv_rcin):
            data = csv_rcin[k]
            channel_3 = round(float(line[1])-float(data[1]),2)
            channel_1 = round(float(line[2])-float(data[2]),2)
            channel_0 = round(float(line[3])-float(data[3]),2)
            channel_2 = round(float(line[4])+float(data[4]),2)
            k = k + val
            #print(k)
            if channel_3 < 0.01 and channel_1 < 0.01 and channel_0 < 0.01 and channel_2 < 0.01:
                matched = matched + 1
            else:
                no_match = no_match + 1
    return matched

max_match = 0
j = 0
for m in range(600):
    if offset_calc(m) > max_match:
        j = m
        max_match = offset_calc(m)

print(str((float(max_match)/float(len(csv_joy)))*100.0)+"% matched for offset: "+str(j))

print("---------------")
print("data_loss_testing")

loss_match = 0
p = 0
for q in range(1000):
    result = conversion_loss_calc(q)
    if  result > loss_match:
        p = q
        loss_match = result
       
print(str((float(loss_match)/float(len(csv_joy)))*100.0)+"% matched for data_loss: "+str(p))
