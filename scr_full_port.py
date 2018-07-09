from stock_pull_A_1 import *
import threading

t1, t2 = set_params(__file__)

for item in os.listdir(os.getcwd()):
    if 'csv' in item:
        if 'combination' not in item.lower():
            os.remove(os.path.join(os.getcwd(), item))

tickers = file_grab(os.path.join(os.getcwd(),"full_port.txt"))
y = 0
start = time.time()

print('###############################################')
print('--------------------STATUS---------------------')
print('###############################################')

print('Downloading Data...')


for ticker in tickers.split(','):
    target = threading.Thread(target =write_loop, args =[ticker, t1, t2])
    target.start()
    while threading.active_count() == 20:
        time.sleep(1)
    

print('Download complete for:\n' + '\n'.join(tickers.split(',')))

print(time.time() - start)

regression_analysis_file_write()

for item in os.listdir(os.getcwd()):
    if 'csv' in item:
        if 'combination' not in item:
            os.remove(os.path.join(os.getcwd(), item))
            
##plot_lgraph('technical_run_chart',
##            '{}_{}-{}'.format(y.ticker, y.dates[0].replace('/', '.'),
##                              y.dates[len(y.dates)-1]).replace('/', '.'),
##            'Time', 'Price', y.dates, y.close_prices[::-1], 'Daily Prices',
##            y.dates, y.upper_bollinger[::-1], 'Upper', y.dates, y.lower_bollinger[::-1],
##            'Lower', y.dates, y.MA_prices[::-1], 'Moving Average', 'y.dates',
##            y.returns[::-1], 'Returns')

reg_call()
