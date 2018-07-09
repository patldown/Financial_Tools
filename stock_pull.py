################################################################################
# ---------------------------------------------------------------------------- #
# Created 2/5/2018 by Patrick Downey ----------------------------------------- #
# ---------------------------------------------------------------------------- #
################################################################################

import os
import time, datetime
import matplotlib.dates as mdates
import urllib
from urllib import request
import csv
from tkinter.filedialog import askopenfilename, asksaveasfilename
import threading

def file_grab():
    location = os.getcwd()
    file = askopenfilename(initialdir = location)
    handle = open(file, 'r')
    reader = handle.readlines()
    item = ''
    for line in reader:
        item = item + line.strip() + ','

    return item.strip(',')           

def procure_data(ticker, t1, t2):

    if '^' in ticker:
        download_link = r'https://finance.yahoo.com/quote/%5E'+ticker[1:].strip()+'/history?period1=' + str(int(t1)) + '&period2=' + str(int(t2)) + '&interval=1d&filter=history&frequency=1d'
        global market
        market = ticker
    else:
        download_link = r'https://finance.yahoo.com/quote/'+ticker.strip()+'/history?period1=' + str(int(t1)) + '&period2=' + str(int(t2)) + '&interval=1d&filter=history&frequency=1d'
    
    dates = []
    close_prices = []  

    response = urllib.request.urlopen(download_link)
    html = response.readlines()
    response.close()
    for line in html:
        line = str(line)
        items = line.split('{')
        for item in items:
            if '"date"' and '"open"' and '"high"' in item.lower():
                if 'symbol' not in item.lower():
                    try:
                        item = item.strip('},')
                        data = item.split(':')
                        datum_string = ''
                        for datum in data:
                            datum_string += datum
                        data = datum_string.split(',')
                        datum_string = ''
                        for datum in data:
                            datum_string += datum
                        
                        data = datum_string.strip('"').split('"')

                        close_prices.append(float(data[9]))
                        dates.append(mdates.datestr2num(datetime.datetime.fromtimestamp(int(data[1])).strftime('%m-%d-%Y')))

                    except:
                        0
                    
    ### error catcher
    if len(close_prices) == 0:
        print(ticker, 'missed due to error in ticker symbol denotation')
        return

    handle = open(ticker + '.csv', 'w', newline = '')
    csvwriter = csv.writer(handle)
    x = len(close_prices) - 1

    while x >= 0:
        csvwriter.writerow([dates[x], close_prices[x]])
        x -= 1
    handle.close()
    
def combine_files():
    combined = []
    ticker_name = ['DATE']
    x = True
    for file in os.listdir(os.getcwd()):
        if 'csv' in file and 'combination' not in file:
            ticker_name.append(file.split('.')[0])
            handle = open(file, 'r', newline = '')
            reader = handle.readlines()
            handle.close()
            if x == True:
                num = len(reader)
                for line in reader:
                    if 'PRICE' in line.upper():
                        continue
                    combined.append([line.strip().split(',')[0], line.strip().split(',')[1]])
                old_num = num
                x = False
            else:
                num = len(reader)
                if num != old_num:
                    print('error in length of data:', file)
                    del ticker_name[ticker_name.index(file.split('.')[0])]
                    continue
                x = 0
                while x <= (num-1):
                    if 'PRICE' not in line.upper():
                        combined[x].append(reader[x].split(',')[1].strip())
                    x += 1
                        
                old_num = num
    
    handle = open('combination_data.csv', 'w', newline = '')
    csvwriter = csv.writer(handle)
    csvwriter.writerow(ticker_name)
    for line in combined:
        csvwriter.writerow(line)
    handle.close()

mnths = int(input('How many months back would you like to grab?'))

for item in os.listdir(os.getcwd()):
    if 'csv' in item:
        if 'combination' not in item.lower():
            os.remove(os.path.join(os.getcwd(), item))

tickers = file_grab()
y = 0
start = time.time()
for ticker in tickers.split(','):
    print(ticker)
    #procure_data(ticker, int(time.time() - (60*60*24*mnths*30)), int(time.time()))
    
    if y < 10:
        x = threading.Thread(target = procure_data, args = [ticker, int(time.time() - (60*60*24*mnths*30)), int(time.time())])
        x.start()
        y += 1
    else:
        y = 0
        time.sleep(5)
print(time.time() - start)

##x.join()
time.sleep(10)
input("When?")
combine_files()

for item in os.listdir(os.getcwd()):
    if 'csv' in item:
        if 'combination' not in item:
            os.remove(os.path.join(os.getcwd(), item))
