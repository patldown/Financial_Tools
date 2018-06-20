from stock_pull_A_0 import *

def unique_function(ticker, t1, t2):
    y = asset(ticker, t1, t2)
    y.write_out()



mnths = 50

for item in os.listdir(os.getcwd()):
    if 'csv' in item:
        if 'combination' not in item.lower():
            os.remove(os.path.join(os.getcwd(), item))

tickers = file_grab(r"C:\usr\FinancialAnalysisTool_Portfolio\Financial_Tools\dividend_aristocrats.txt")
y = 0
start = time.time()

print('###############################################')
print('--------------------STATUS---------------------')
print('###############################################')

container = []

print('Downloading Data...')

for ticker in tickers.split(','):
    assets = []
    x = unique_function(ticker, int(time.time() - (60*60*24*mnths*30)), int(time.time()))

print('Download complete for:\n' + '\n'.join(tickers.split(',')))

print(time.time() - start)


regression_analysis_file_write()

for item in os.listdir(os.getcwd()):
    if 'csv' in item:
        if 'combination' not in item:
            os.remove(os.path.join(os.getcwd(), item))


reg_call()
