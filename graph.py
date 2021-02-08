#!/bin/python

import matplotlib.pyplot as plt
import csv
import sys

timestamps = []
channel0 = []
channel1 = []
diff = []
delays = []
start_time = 0

with open(sys.argv[1], 'r') as csvfile:
  csvreader = csv.reader(csvfile)
  
  for i, row in enumerate(csvreader):
    if i > 0:
      delays.append(float(row[0]) - timestamps[-1])

    if i > 0:
      timestamps.append(float(row[0]) - start_time)
    else:
      timestamps.append(0)
      start_time = float(row[0])

    channel0.append(float(row[1]))
    channel1.append(float(row[2]))
    diff.append(float(row[2]) - float(row[1]))
  
  total_time = timestamps[len(timestamps) - 1] - timestamps[0]
  print(f"Processed {csvreader.line_num} entries over {total_time / 1000000.0} ms")

for stamp in timestamps:
  print(stamp)

plt.plot(timestamps, channel0)
plt.ylabel('Channel 0 Readings')
plt.show()
