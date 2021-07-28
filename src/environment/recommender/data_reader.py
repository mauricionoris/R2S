
"""
 extracted and adapted from Lenskit dataset.py
    
    1) changed to read Parquet files instead of CSV - done
    2) simplification for R2S purposes  --done
    3) Allowing to split the users among agents 
    4) TODO: multi-databases --done
 
"""
"""
Code to import commonly-used RecSys data sets into LensKit-compatible data frames.
"""

import os.path
from pathlib import Path
import logging

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from functools import cached_property
from argparse import Namespace

log = logging.getLogger(__name__)


"""
Example of use:
ml = R2S(dataset={'name':"MovieLens", 'path':"/source/R2S/data/R2SDatasets/movielens"},
         data={'ratings':None, 'movies': None, 'tags': None
               , 'links': None, 'genome-tags':None, 'genome-scores': None})

"""

class R2S:
    _VALID_KEYWORDS = {'dataset', 'data'}

    def __init__(self, **kwargs):
        for keyword, value in kwargs.items():
            if keyword in self._VALID_KEYWORDS:
                setattr(self, keyword, value)
            else:
                raise ValueError(
                    "Unknown keyword argument: {!r}".format(keyword))
        
        self.dataset = Namespace(**self.dataset)
        
        
        for k in self.data:
            print(k)
    
            fn = str(self.dataset.path) + '/' + k + '.parquet'
            self.data[k] = pq.read_table(source=fn).to_pandas()

        self.data = Namespace(**self.data)


    #TODO: Data preparation
    #def transform(self, args):
    #    self.dataset[args.name].rename(columns=args.columns, inplace=True)

