import os
import matplotlib.pyplot as plt
import numpy as np

sections = {}

ans = False
handle = open('data.csv', 'r')
reader = handle.readlines()

for line in reader:
    if 'Date' in line:
        x = line.split(',')[1:]
        ans = True
    elif ans == True:
        line = line.split(',')
        sections[line[0]] = line[1:]



subplt = 311

plt.subplot(subplt)
x_nums = np.array(range(0, len(x)))
plt.xticks(x_nums, x, rotation='45')
plt.plot(x_nums, y)
subplt += 1

plt.show()
