
"""
 extracted and adapted from Lenskit dataset.py
    
    1) changed to read Parquet files instead of CSV - done
    2) simplification for R2S purposes  --done
    3) TODO: Allowing to split the users among agents 
    4) multi-databases --done
 
"""
"""
Code to import commonly-used RecSys data sets into LensKit-compatible data frames.
"""

import logging
import importlib
import sys 
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from pyarrow import json
import numpy as np
from argparse import Namespace
import scipy.sparse as spa

sys.path.append('/source/R2S/src/environment/recommender/algorithms')

log = logging.getLogger(__name__)


"""
Example of use:
ml = R2S(dataset={'name':"MovieLens", 'path':"/source/R2S/data/R2SDatasets/movielens"},
         data={'ratings':None, 'movies': None, 'tags': None
               , 'links': None, 'genome-tags':None, 'genome-scores': None},
         algo={'PopScore': 'basic'} #key = algo / #value=module
"""

class R2S:
    _VALID_KEYWORDS = {'dataset', 'data', 'algo', 'matrix',  'algodata', 'algoparam'}

    def __init__(self, **kwargs):
        for keyword, value in kwargs.items():
            if keyword in self._VALID_KEYWORDS:
                setattr(self, keyword, value)
            else:
                raise ValueError(
                    "Unknown keyword argument: {!r}".format(keyword))
        
        self.dataset = Namespace(**self.dataset)
        
        #load algorithms available for that dataset
        for k in self.algo:
            print ('Loading the algorithm {} from the module {}'.format(k,self.algo[k]))
            self.algo[k] = getattr(importlib.import_module(self.algo[k],k),k)()
           
        self.algo = Namespace(**self.algo)

        #load all dataset
        for k in self.data:
            fn = str(self.dataset.path) + '/' + k + '.parquet'
            self.data[k] = pq.read_table(source=fn).to_pandas()
            print('Loading data file {} with {} rows and  {} columns'.format(k, self.data[k].shape[0],self.data[k].shape[1]))


        self.matrix = Namespace(**self.matrix)
        #data pre-process
        _row = self.data[self.matrix.source][self.matrix.row].values
        _col = self.data[self.matrix.source][self.matrix.col].values
        _data = self.data[self.matrix.source][self.matrix.data].values.astype(np.single)

        print('Setting a sparse matrix of ratings (rows {} and columns {})  '.format(len(_row),len(_col)))

        self.ui_coo = spa.coo_matrix((_data, (_row, _col)))


        #self.data = Namespace(**self.data)


    def __del__(self):
        print('----------------------------ending the scope of the R2S framework---------------------------')

        #udt = pa.map_(pa.int(), pa.array())
        #schema = pa.schema([pa.field('id',udt), pa.field('rec', pa.array)])
        #test = pd.DataFrame.from_dict(self.algo.Random.rec)
        test = pa.DictionaryArray.from_arrays(self.algo.Random.rec.keys(),self.algo.Random.rec.values())

        
        
        #TODO: SAVING THE RECOMMENDATIONS AND CANDIDATES AS CACHE TO IMPROVE THE ALGORITHMS
        print(type(test))

#    @cached_property
#    def metadata():

