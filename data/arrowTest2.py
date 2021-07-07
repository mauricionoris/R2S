import time

file = "/source/movielens/ml-25m/ratings.csv"
fileout = "/source/movielens/ml-25m/ratings.parquet"

from pyarrow import csv

t0 = time.process_time()

table = csv.read_csv(file)

t1 = time.process_time() - t0


#print(table)
#df = table.to_pandas()
#print(df.head())

import pyarrow.parquet as pq
pq.write_table(table, fileout)

t2 = time.process_time() - t1



print('Time elapsed:', t2, t1)


