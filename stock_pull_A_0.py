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
from operator import *


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

        self.write_out()


    def link(self):

        if '^' in self.ticker:
            self.download_link = r'https://finance.yahoo.com/quote/%5E'+self.ticker[1:].strip()+\
                                 '/history?period1=' + str(int(self.t1)) + '&period2=' + str(int(self.t2)) +\
                                 '&interval=1d&filter=history&frequency=1d'
            self.self.market = True
        else:
            self.download_link = r'https://finance.yahoo.com/quote/'+self.ticker.strip()\
                                 +'/history?period1=' + str(int(self.t1)) + '&period2=' + str(int(self.t2)) +\
                                 '&interval=1d&filter=history&frequency=1d'
            self.market = False



        response = urllib.request.urlopen(self.download_link)
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
                        try:
                            self.dates.append(datetime.datetime.fromtimestamp(int(data[1])).strftime('%m/%d/%Y'))
                        except:
                            continue
                        try:
                            self.close_prices.append(float(data[9]))
                        except:
                            continue
                        try:
                            self.volume = int(data[10])
                        except:
                            continue
                        #print(datetime.datetime.fromtimestamp(int(data[1])).strftime('%m/%d/%Y'))
                        self.dates.append(datetime.datetime.fromtimestamp(int(data[1])).strftime('%m/%d/%Y'))
                        

        self.volume
        self.close_prices = self.close_prices[::-1]
        self.dates = self.dates[::-1]
                        
        ### error catcher
        if len(self.close_prices) == 0:
            print(self.ticker, 'missed due to error in ticker symbol denotation')
            print(self.download_link)
            return

    def c_returns(self):

        self.returns = []
        t = 0
        max_v = len(self.close_prices) - 1
        while t <= max_v:
            if t == 0:
                self.returns.append(0)
            else:
                self.returns.append(round((self.close_prices[t] - self.close_prices[t-1])/self.close_prices[t-1],2))
            t+=1

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
        t = 0
        while t < MA:
            self.MA_prices.append(0)
            self.upper_bollinger.append(0)
            self.lower_bollinger.append(0)
            t += 1

        while t >= MA and t < len(self.close_prices):
            average = sum(self.close_prices[(t - MA):t])/MA
            self.MA_prices.append(average)
            std_dev = numpy.std(self.close_prices[(t - MA):t])
            self.upper_bollinger.append(average + std_dev)
            self.lower_bollinger.append(average - std_dev)            
            t += 1

        self.MA_current = self.MA_prices[len(self.MA_prices) - 1]

    def write_out(self):

        self.dates = self.dates[::-1]
        self.close_prices = self.close_prices[::-1]
        self.MA_prices = self.MA_prices[::-1]
        self.upper_bollinger = self.upper_bollinger[::-1]
        self.lower_bollinger = self.lower_bollinger[::-1]

        handle = open(self.ticker + '.csv', 'w', newline = '')
        csvwriter = csv.writer(handle)
        t = len(self.close_prices) - 1

        while t >= 0:
            try:
                csvwriter.writerow([self.dates[t], self.close_prices[t], self.MA_prices[t],
                                self.upper_bollinger[t], self.lower_bollinger[t]])
            except:
                csvwriter.writerow([self.close_prices[t], self.MA_prices[t], self.upper_bollinger[t], self.lower_bollinger[t]])
            t -= 1
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

def set_params(file_name, *args):
    '''
    -args:
    -param = file_name:=name of the call
    -param = args:= (1)working capital
                    (2)ROR
                    (3)Short?
                    (4)high perf
                    (5)low?
                    (6)months
    '''

    w_capital = args[0]
    ror = args[1]
    short = args[2]
    if short == 0: short = False
    elif short == 1: short = True
    high_perf = args[3]
    if high_perf == 0: high_perf = False
    elif high_perf == 1: high_perf = True
    low_perf = args[4]
    if low_perf == 0: low_perf = False
    elif low_perf == 1: low_perf = True
    months = args[5]
        
    handle = open('setup.info', 'w')
    handle.write(file_name + '\n')
    handle.write(w_capital + '\n')
    handle.write(ror + '\n')
    handle.write(str(short) + '\n')
    handle.write(str(high_perf) + '\n')
    handle.write(str(low_perf) + '\n')
    handle.write(str(months))
    handle.close()

    if __name__ == '__main__':    
        return int(t1), int(t2), high_perf, low_perf

def read_params():
    handle = open('setup.info', 'r')
    reader = handle.readlines()
    handle.close()

    filename = reader[0].strip()
    w_capital = reader[1].strip()
    ror = reader[2].strip()
    short = reader[3].strip()
    high_perf = reader[4].strip()
    low_perf = reader[5].strip()
    months = reader[6].strip()

    return filename,w_capital, ror, short, high_perf, low_perf, months

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

def download_data():
    import time
    from tkinter import filedialog
    
    portfolio = filedialog.askopenfilename(initialdir = os.getcwd())
    file_name,w_capital, ror, short, high_perf, low_perf, months = read_params()
    assets = port_read(portfolio)

    t1 = int(time.time()) - int(months) * 60 * 60 * 24 * 30
    t2 = int(time.time())
    
    for ticker in assets:
        ticker = ticker.split(':')[0]
        print(ticker)
        y = threading.Thread(target = asset, args = [ticker, t1, t2])
        y.start()
        while threading.active_count() > 5:
            time.sleep(1)

    while threading.active_count() > 1:
        time.sleep(1)

    ### combination file is created here
    regression_analysis_file_write()

def update_sector_populations():
    
    import urllib.request

    divisor1 = 'class="Fw(b)"'
    divisor2 = '</a>'
    sector_types = ['healthcare', 'financial', 'services', 'utilities', 'industrial_goods',
                    'basic_materials', 'conglomerates', 'consumer_goods', 'technology']
    for item in sector_types:
        handle = open(item + '_tickers' + '.txt', 'w')
        data = []
        offset = 0
        while offset <= 1000:
            download_link = r'https://finance.yahoo.com/screener/predefined/' + item + '?offset=' + str(offset) +'&count=100'
            response = urllib.request.urlopen(download_link)
            html = response.readlines()
            response.close()

            for line in html:
                line = str(line)
                if divisor1 in line:
                    objs = line.split(divisor1)

                    for obj in objs:
                        sobj = obj.split('>')[1].split('<')[0].strip()
                        name = obj.split('>')[5].split('<')[0].strip()
                        p_e = obj.split('>')[33].split('<')[0].strip()
                        if p_e.strip() == 'N/A':
                            p_e = '0'
                        p_e = p_e.replace(',', '')
                        if sobj != '':
                            data.append([sobj, name, float(p_e)])
            offset += 100
        data.sort(key = itemgetter(2), reverse=False)
        for line in data:
            line[2] = str(line[2])
            handle.write(':'.join(line) + '\n')
        handle.close()

def reg_overlay(function = reg_call):
    reg_file_loc = os.path.join(os.getcwd(), 'Results')
    files = os.listdir(reg_file_loc)
    function()
    time.sleep(45)
    for file in os.listdir(reg_file_loc):
        if file not in files:
            handle = open(os.path.join(reg_file_loc, file), 'r', newline = '')
            reader = handle.readlines()
            handle.close()
            for line in reader:
                nline = line.strip().split(',')
                if nline[0] == 'Weights':
                    z = reader.index(line) - 1
            new_dict = {}
            x = 1
            y = len(reader[z].split(','))
            while x < y:
                new_dict[reader[z].split(',')[x]] = reader[z + 4].split(',')[x]
                x += 1
    print(new_dict)


#if __name__ == '__main__':
#   reg_overlay()
