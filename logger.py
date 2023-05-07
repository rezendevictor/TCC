from datetime import datetime
from pandas import DataFrame

def data_logger(process):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #print(dt_string)
    #print(process)

def write_results(results, bad_smell,file):
    data_logger('Writing results....')
    bad_smell = bad_smell.replace('.csv', '')
    file = file.replace('.csv', '')
    results.to_csv(f'./results/results_{bad_smell}_{file}.csv',index=False)