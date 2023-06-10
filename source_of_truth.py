import pandas
from os import listdir
from os.path import isfile, join
from pandas import DataFrame


def generate_sot_dict():
    class_files = [f for f in listdir('source-of-truth') if isfile(join('source-of-truth', f))]  
    dict = {}

    for class_file in class_files:
        file =  class_file.split('-')[1].split('.')[0]
        dict[file] = pandas.read_csv(f'source-of-truth/{class_file}', sep=',')

    return dict

