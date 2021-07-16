import sys, json, time

from pyarrow import csv
import pyarrow.parquet as pq

sys.path.append('/source/R2S/src/util')

import fileHandler as fh


def import_dataset(args):

    imported_files = []
    
    files = fh.read_folder(args.folderIn, args.extension)
    
    fh.create_folder(args.folderOut)
    for FILE in files:
       imported_files.append(convert2parquet(args.folderIn + '/' + FILE, args.folderOut + '/' + FILE.split('.')[0] + '.parquet'))
    
    return imported_files



def convert2parquet(fileIn,fileOut):

    #  filecsv = "/source/datasets/movielens/ml-25m/ratings.csv"
    #  fileparquet = "/source/datasets/movielens/ml-25m/ratings.parquet"

    file_converted = json.loads('{ "fileIn":"", "fileOut": "", "fileInSize": 0, "fileOutSize": 0 , "et": 0}') 

    t0 = time.process_time()
    table = csv.read_csv(fileIn)
    t1 = time.process_time()
    pq.write_table(table, fileOut)
    t2 = time.process_time()

    file_converted['fileIn'] = fileIn
    file_converted['fileOut'] = fileOut
    file_converted['et'] = t2 - t0
    file_converted['fileInSize'] = fh.file_size(fileIn)
    file_converted['fileOutSize'] = fh.file_size(fileOut)


    return file_converted


