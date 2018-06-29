from stock_pull_A_0 import *
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

assets = []
for ticker in tickers.split(','):
    target = write_loop(ticker, t1, t2)

print('Download complete for:\n' + '\n'.join(tickers.split(',')))

print(time.time() - start)

regression_analysis_file_write()

for item in os.listdir(os.getcwd()):
    if 'csv' in item:
        if 'combination' not in item:
            os.remove(os.path.join(os.getcwd(), item))


reg_call()
