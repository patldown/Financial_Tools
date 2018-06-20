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

class asset:
    def __init__(self, ticker, t1, t2):
        '''
        param: -ticker as string stock ticker
        '''

        self.ticker = ticker
        self.t1 = t1
        self.t2 = t2

        self.link()
        self.c_returns()

    def link(self):

        if '^' in self.ticker:
            download_link = r'https://finance.yahoo.com/quote/%5E'+self.ticker[1:].strip()+\
                                 '/history?period1=' + str(int(self.t1)) + '&period2=' + str(int(self.t2)) +\
                                 '&interval=1d&filter=history&frequency=1d'
            self.market = True
        else:
            download_link = r'https://finance.yahoo.com/quote/'+self.ticker.strip()\
                                 +'/history?period1=' + str(int(self.t1)) + '&period2=' + str(int(self.t2)) +\
                                 '&interval=1d&filter=history&frequency=1d'
            self.market = False

        response = urllib.request.urlopen(download_link)
        html = response.readlines()
        response.close()

        self.procure_data(html)

    def procure_data(self, html):
        self.dates = []
        self.close_prices = []  

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

                            self.close_prices.append(float(data[9]))
                            self.dates.append(mdates.datestr2num(datetime.datetime.fromtimestamp(int(data[1])).strftime('%m-%d-%Y')))

                        except:
                            0
        
                        
        ### error catcher
        if len(self.close_prices) == 0:
            print(self.ticker, 'missed due to error in ticker symbol denotation')
            return

    def c_returns(self):

        self.returns = []
        x = 0
        max_v = len(self.close_prices) - 1
        while x <= max_v:
            if x == 0:
                self.returns.append(0)
            else:
                self.returns.append(round((self.close_prices[x] - self.close_prices[x-1])/self.close_prices[x-1],2))
            x+=1

        try:
            self.avg_return = sum(self.returns[1:])/len(self.returns[1:])
            self.max_return = max(self.returns)
            self.min_return = min(self.returns)
            self.ret_spread = (self.max_return - self.min_return)
        except:
            self.avg_return = False
            self.max_return = False
            self.min_return = False
            self.ret_spread = False

    def write_out(self):

        handle = open(self.ticker + '.csv', 'w', newline = '')
        csvwriter = csv.writer(handle)
        x = len(self.close_prices) - 1

        while x >= 0:
            csvwriter.writerow([self.dates[x], self.close_prices[x]])
            x -= 1
        handle.close()
        
        
def file_grab(file = False):
    
    if file == False:
        location = os.getcwd()
        file = askopenfilename(initialdir = location)

    handle = open(file, 'r')
    reader = handle.readlines()
    item = ''
    for line in reader:
        item = item + line.strip() + ','

    return item.strip(',')           


def regression_analysis_file_write():
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


def reg_call():
    import subprocess
    os.system(r'start excel.exe "' + os.getcwd() + '\FORMATTING.xlsm"')
