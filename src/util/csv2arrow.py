import time
import os
import json
import sys
import fileshandler as f

from pyarrow import csv
import pyarrow.parquet as pq

def csv2arrow(args):

    #args.fileIn = "/source/movielens/ml-25m/*.csv"
    #args.fileOut = "/source/movielens/ml-25m/ratings.parquet"

    ret = json.loads('{ "r2sPid": 0, "return": 1000, "csvRT": 0, "parquetWT": 0, "et": 0, "fileInSize": 0, "fileOutSize": 0}') 

    t0 = time.process_time()

    table = csv.read_csv(args.fileIn)

    t1 = time.process_time()

    pq.write_table(table, args.fileOut)

    t2 = time.process_time()

    ret['csvRT'] = t1 - t0
    ret['parquetWT'] = t2 - t1
    ret['et'] = t2 - t0
    ret['fileInSize'] = f.file_size(args.fileIn)
    ret['fileOutSize'] = f.file_size(args.fileOut)
    
    return ret



