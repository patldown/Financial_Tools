from stock_pull_A_0 import *

port_file = 'full_port.txt'

t1, t2, high_perf, low_perf = set_params(__file__)

clear_folder()

assets = port_read(port_file)

stock_objs = []
for item in assets:
    y = asset(item, t1, t2)
    if y.market == True:
        index = y
    else:
        stock_objs.append(y)

##for item in stock_objs:
##    if low_perf == True:
##        if item.returns[]

