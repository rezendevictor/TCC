import pandas

from pandas import DataFrame
from os import listdir
from os.path import isfile, join


def get_data(date_frame, operator, threshold_value, name) -> DataFrame:
    if operator == '>':
        return date_frame.loc[date_frame[name] > threshold_value]
    elif operator == '<':
        return date_frame.loc[date_frame[name] < threshold_value]
    elif operator == '=':
        return date_frame.loc[date_frame[name] == threshold_value]


def read_threasholds_names(threash):
    marks_list = threash['name'].tolist()
    marks_list.insert(0,'class')
    return marks_list


def get_data_and_clean_data(filename, threash):
    methods = pandas.read_csv(f'class/{file}', sep=',')
    threashold_names = read_threasholds_names(threash)
    methods = methods[threashold_names]
    return methods

def filter_data(threash, method_data):
    filtered_data = DataFrame()
    for x in range(0, len(threash)):
        limit = threash.iloc[x]
        filtered_data = get_data(method_data, limit['sign'],limit['value'],limit['name'])

    return filtered_data


class_files = [f for f in listdir('class') if isfile(join('class', f))]
threash = pandas.read_csv(f'threashold.csv', sep=',')
files_dict = {}

for file in class_files:
    methods = get_data_and_clean_data(file,threash)
    files_dict[file] = methods

for files in files_dict:
    print(files)
    print(files_dict[files])
    filter_data(threash, files_dict[files])
    break