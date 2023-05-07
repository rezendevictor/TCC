import logger
import pandas
from os import listdir
from os.path import isfile, join



def read_threasholds_names(threash):
    marks_list = threash['name'].tolist()
    marks_list.insert(0,'class')
    return marks_list


def get_data_and_clean_data(filename, threash):
    methods = pandas.read_csv(f'class/{filename}', sep=',')
    threashold_names = read_threasholds_names(threash)
    methods = methods[threashold_names]
    return methods



def acquire_threasholds():
    threashold_files = [f for f in listdir('threasholds') if isfile(join('threasholds', f))]
    return threashold_files


def reading_data_from_files():
   logger.data_logger('Acquiring Threasholds....')
   
   threashold_files = acquire_threasholds()
   
   logger.data_logger('Acquiring class files....')
   
   class_files = [f for f in listdir('class') if isfile(join('class', f))]   

   return [threashold_files,class_files]