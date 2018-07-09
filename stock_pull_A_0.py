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
from graphics_A_0 import *

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
        self.create_MAs()

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
                            #print(data)

                            self.close_prices.append(float(data[9]))
                            self.volume = int(data[10])
                            #print(datetime.datetime.fromtimestamp(int(data[1])).strftime('%m/%d/%Y'))
                            self.dates.append(datetime.datetime.fromtimestamp(int(data[1])).strftime('%m/%d/%Y'))

                        except:
                            0
            
        self.close_prices = self.close_prices[::-1]
        self.dates = self.dates[::-1]
                        
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

    def create_MAs(self, MA = 100):
        import numpy
        
        self.MA_prices = []
        self.upper_bollinger = []
        self.lower_bollinger = []
        x = 0
        while x < MA:
            self.MA_prices.append(0)
            self.upper_bollinger.append(0)
            self.lower_bollinger.append(0)
            x += 1

        while x >= MA and x < len(self.close_prices):
            average = sum(self.close_prices[(x - MA):x])/MA
            self.MA_prices.append(average)
            std_dev = numpy.std(self.close_prices[(x - MA):x])
            self.upper_bollinger.append(average + std_dev)
            self.lower_bollinger.append(average - std_dev)            
            x += 1

        self.MA_current = self.MA_prices[len(self.MA_prices) - 1]

    def write_out(self):

        self.dates = self.dates[::-1]
        self.close_prices = self.close_prices[::-1]
        self.MA_prices = self.MA_prices[::-1]
        self.upper_bollinger = self.upper_bollinger[::-1]
        self.lower_bollinger = self.lower_bollinger[::-1]

        handle = open(self.ticker + '.csv', 'w', newline = '')
        csvwriter = csv.writer(handle)
        x = len(self.close_prices) - 1

        while x >= 0:
            csvwriter.writerow([self.dates[x], self.close_prices[x], self.MA_prices[x],
                                self.upper_bollinger[x], self.lower_bollinger[x]])
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

def set_params(file_name):
    ### file_name  == '__file__'
    print('### Portfolio Analyis ###\n')

    t2 = time.time()
    t1 = time.time() - int(input('How many months of data would you like to collect?'))*60*60*24*30
    high_perf = input('Turn on Positive Performance Sort (Y/N): ').upper().strip()
    if high_perf == 'Y':
        high_perf = True
        low_perf = False
    else:
        high_perf = False
        if input('Would you like to choose the reverse criteria (Y/N)? ').upper().strip() == 'Y':
            low_perf = True
        else:
            low_perf = False
    
    w_capital = input('Working capital: ')
    ror = input('What is your desired rate of return (e.g. 10% = 0.1)? ')

    short = input('Would you like to short in addition to longing (Y/N)? ').upper().strip()
    if short == 'N':
        short = False
    elif short == 'Y':
        short = True
        
    handle = open('setup.info', 'w')
    handle.write(os.path.basename(file_name).split('.')[0] + '\n')
    handle.write(w_capital + '\n')
    handle.write(ror + '\n')
    handle.write(str(short) + '\n')
    handle.write(str(high_perf) + '\n')
    handle.write(str(low_perf) + '\n')
    handle.close()
    
    return int(t1), int(t2), high_perf, low_perf

def read_params(file_name):
    ### file_name  == '__file__'
    print('### Portfolio Analyis ###\n')

    handle = open()

    high_perf = input('Turn on Positive Performance Sort (Y/N): ').upper().strip()
    if high_perf == 'Y':
        high_perf = True
        low_perf = False
    else:
        high_perf = False
        if input('Would you like to choose the reverse criteria (Y/N)? ').upper().strip() == 'Y':
            low_perf = True
        else:
            low_perf = False
    
    w_capital = input('Working capital: ')
    ror = input('What is your desired rate of return (e.g. 10% = 0.1)? ')

    short = input('Would you like to short in addition to longing (Y/N)? ').upper().strip()
    if short == 'N':
        short = False
    elif short == 'Y':
        short = True
        
    handle = open('setup.info', 'w')
    handle.write(os.path.basename(file_name).split('.')[0] + '\n')
    handle.write(w_capital + '\n')
    handle.write(ror + '\n')
    handle.write(str(short) + '\n')
    handle.write(str(high_perf) + '\n')
    handle.write(str(low_perf) + '\n')
    handle.close()
    
    return int(t1), int(t2), high_perf, low_perf
       
def write_loop(ticker, t1, t2):
    handle = open('setup.info', 'r')
    reader = handle.read()
    handle.close()

    high_perf = reader.split('\n')[4]
    low_perf = reader.split('\n')[5]
    
    y = asset(ticker, t1, t2)

    if high_perf == 'False':
        0
    else:
        if y.avg_return > 0:
            y.write_out()
        else:
            print(y.ticker, 'does not meet Positive criteria')
    

    if low_perf == 'False':
        y.write_out()
    else:
        if y.avg_return < 0:
            y.write_out()
        else:
            print(y.ticker, 'does not meet Negative criteria')

def port_read(port_file):

    assets = []
    
    handle = open(port_file, 'r')
    reader = handle.readlines()
    for line in reader:
        line = line.strip()
        assets.append(line)

    return assets

def clear_folder():
    for item in os.listdir(os.getcwd()):
        if 'csv' in item:
            if 'combination' not in item.lower():
                os.remove(os.path.join(os.getcwd(), item))
                
def reg_call():
    import subprocess
    os.system(r'start excel.exe "' + os.getcwd() + '\FORMATTING.xlsm"')

if __name__ == '__main__':
    asset('GOOG', (time.time()), (time.time() - (60*60*24*30*50)))