import pandas

from pandas import DataFrame
from os import listdir
from os.path import isfile, join
from logger import data_logger, write_results
import file_manipulation

def compute_data_against_threshold_metrics(date_frame, operator, threshold_value, name) -> DataFrame:
    if operator == '>':
        return date_frame.loc[date_frame[name] > threshold_value]
    elif operator == '<':
        return date_frame.loc[date_frame[name] < threshold_value]
    elif operator == '=':
        return date_frame.loc[date_frame[name] == threshold_value]   
    elif operator == '>=':
        return date_frame.loc[date_frame[name] >= threshold_value]
    elif operator == '<=':
        return date_frame.loc[date_frame[name] <= threshold_value]


def filter_data(threash, method_data):
    filtered_data = method_data
    for x in range(0, len(threash)):
        limit = threash.iloc[x]
        filtered_data = compute_data_against_threshold_metrics(filtered_data, limit['sign'],limit['value'],limit['name'])
    return filtered_data



def run_threasholds(threash, class_files, bad_smell):
    files_dict = {}

    for file in class_files:
        methods = file_manipulation.get_data_and_clean_data(file,threash)
        files_dict[file] = methods


    for files in files_dict:
        results = filter_data(threash, files_dict[files])
        print(files)
        write_results(results, bad_smell, files)


def main():    
    [threashold_files,class_files] = file_manipulation.reading_data_from_files()
    for bad_smell in threashold_files:
        threash = pandas.read_csv(f'./threasholds/{bad_smell}', sep=',')
        run_threasholds(threash, class_files, bad_smell)


if __name__ == '__main__':
    main()