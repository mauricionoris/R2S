
def arrowTest(args):

    import time
    import json
    import sys

    filecsv = "/source/datasets/movielens/ml-25m/ratings.csv"
    fileparquet = "/source/datasets/movielens/ml-25m/ratings.parquet"

    from pyarrow import csv
    import pyarrow.parquet as pq

    t0 = time.process_time()
    table = csv.read_csv(filecsv)
    t1 = time.process_time() - t0

    table2 = pq.read_table(fileparquet)

    t2 = time.process_time() - t1

    ret = json.loads('{ "r2sPid": 0, "return": 1000, "tCSV": 0, "tParquet": 0, "tCompare": false}') 

    ret["tCSV"] = t1
    ret["tParquet"] = t2
    ret["tCompare"] = table.equals(table2)


    ret["exitCode"] = ret["return"]
    return ret
    