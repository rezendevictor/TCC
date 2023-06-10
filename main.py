import pandas
import numpy as np
from pandas import DataFrame
from os import listdir
from os.path import isfile, join
from logger import data_logger, write_results
from source_of_truth import generate_sot_dict
import file_manipulation
import shutil
import os


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
        write_results(results, bad_smell, files)


def generate_bad_smells_dict(archive_dict):
    class_files = [f for f in listdir('results') if isfile(join('results', f))] 
    archive_dict = {}
    for class_file in class_files:
        source = class_file.split('_')[2].split('.')[0] 
        archive_dict[source] = None

    for class_file in class_files:
            dict = {}
            bad_smell = class_file.split('_')[1]    
            source = class_file.split('_')[2].split('.')[0]

            if(archive_dict[source]) == None:
                dict[bad_smell] = pandas.read_csv(f'results/{class_file}', sep=',')
                archive_dict[source] = dict
            else:
                internal_dict = archive_dict[source]
                internal_dict[bad_smell] = pandas.read_csv(f'results/{class_file}', sep=',')
                archive_dict[source] = internal_dict

    return archive_dict

def compare_results_with_sot(bad_smell_dict,sot_dict):
    final_dict = {}
    
    for key in bad_smell_dict.keys():
        final_dict[key] = {}
    
    for key in bad_smell_dict.keys():
        bad_smell_candidates = bad_smell_dict[key]        
    
        for bad_smell_key in bad_smell_candidates:
            final_dict[key][bad_smell_key] = None

        if(key in sot_dict.keys()):
            for bad_smell_key in bad_smell_candidates:
                sot_by_file = sot_dict[key]
                filtered_sot_by_code_smell = sot_by_file.loc[sot_by_file['Bad smell'] == bad_smell_key]

                if filtered_sot_by_code_smell.empty:
                    continue

                for item in bad_smell_candidates:
                  file_results = bad_smell_candidates[item]

                  if(not file_results.empty):
                    df1 = pandas.merge(file_results,filtered_sot_by_code_smell,on=['class'], how='inner')
                    final_dict[key][bad_smell_key] = df1

    return final_dict


def calculate_precision(true_positives, false_positives):
    if(true_positives + false_positives > 0):
        precision = true_positives/( true_positives + false_positives)
        print(f"Precision: ${precision}")
    else:
        print(f"Precision: 0")
    

def calculate_recall(true_positives, false_negatives):
    if(true_positives + false_negatives > 0):
        recall = true_positives/( true_positives + false_negatives)
        print(f"Recall: ${recall}")
    else:
        print(f"Recall: 0")

def load_base_data():
    base_dict = {}
    class_files = [f for f in listdir('class') if isfile(join('class', f))] 
    for filename in class_files:
        methods = pandas.read_csv(f'class/{filename}', sep=',')
        clean_filename = filename.replace('class.csv', '')
        base_dict[clean_filename] = methods[['class']]
    return base_dict

def calculate_final_results(final_dict, sot_dict, bad_smell_dict):
    base_dict = load_base_data();  
    for file in final_dict:
        bad_smell_list_by_file = bad_smell_dict[file]
        base_dict_by_file = base_dict[file]  
        for bad_smell in bad_smell_list_by_file.keys():
            if(file not in sot_dict.keys()):
                continue

            result_by_file_by_bad_smell = final_dict[file][bad_smell]
            sot_by_file = sot_dict[file]
            sot_by_file_by_code_smell = sot_by_file.loc[sot_by_file['Bad smell'] == bad_smell]
            bad_smell_dict_by_file_by_bad_smell = bad_smell_dict[file][bad_smell]

            ########### Positivos    
            
            positives_by_threshold = bad_smell_dict_by_file_by_bad_smell.shape[0]
            true_positives = 0
            if type(result_by_file_by_bad_smell) != type(None) :
                true_positives = result_by_file_by_bad_smell.shape[0]
            else:
                continue
            print('------------------------------------------------------------------------------------------')
            print('file : ' + file)
            print('bad smell : '+ bad_smell)

            false_positives = positives_by_threshold - true_positives

            ############ Negativos
            base_dict_items = base_dict_by_file.shape[0]            
            
            negatives_by_sot = find_negative_list(sot_by_file_by_code_smell, base_dict_by_file) 
            ## é o que ta no geral mas nao ta no SOT, positivo com certeza
            
            negatives_by_threashold = find_negative_list(bad_smell_dict_by_file_by_bad_smell, base_dict_by_file)[['class']] 
            ## é o que ta no geral mas nao ta no Threashold, candidato a ser negativo


            true_negative_dataframe = pandas.merge(negatives_by_sot,negatives_by_threashold,on=['class'], how='inner')[['class']]
            false_negative_dataframe = find_negative_list(true_negative_dataframe, negatives_by_threashold)

            false_negatives = false_negative_dataframe.shape[0]


            print(f"true_positives: {true_positives}")
            print(f"false_positives: {false_positives}")
            print(f"false_negatives: {false_negatives}")
            calculate_precision(true_positives, false_positives)
            calculate_recall(true_positives, false_negatives)

    return

def find_negative_list(dict_to_compare, base_dict):
    df_total =  base_dict.merge(dict_to_compare.drop_duplicates(), on=['class'], 
                   how='left', indicator=True)
    return df_total[df_total['_merge'] == 'left_only']

def clean_negatives(dict_to_be_clean):
    return dict_to_be_clean[['class']]


def setup():
   shutil.rmtree('./results')
   os.mkdir('./results')


def main():    
    
    setup()

    [threashold_files,class_files] = file_manipulation.reading_data_from_files()
    bad_smell_dict = {}

    for bad_smell in threashold_files:
        threash = pandas.read_csv(f'./threasholds/{bad_smell}', sep=',')
        run_threasholds(threash, class_files, bad_smell)
    
    for class_file in class_files: 
        bad_smell_dict[class_file.replace('.csv', '').replace('class', '')] = None

    bad_smell_dict = generate_bad_smells_dict(bad_smell_dict)
    sot_dict = generate_sot_dict()
    final_dict = compare_results_with_sot(bad_smell_dict, sot_dict)
    calculate_final_results(final_dict, sot_dict, bad_smell_dict)


if __name__ == '__main__':
    main()