import sys

sys.path.append('/source/R2S/src/util')
from R2Sprofile import profileit
import R2SObject
import pandas as pd
import numpy as np
from argparse import Namespace


import time                                                



@profileit
def callR2S():

    #print(args)
    R2S = R2SObject.R2S(
                        dataset={'name':'MovieLens', 'path':'/source/R2S/data/R2SDatasets/movielens'}
    #                    , data={'ratings':None, 'movies': None, 'tags': None, 'links': None, 'genome-tags':None, 'genome-scores': None}
                        , data={'ratings':None, 'movies': None}
    #                     , algo={'PopScore': 'basic', 'Random':'basic'}
    #                     , algo={'PopScore': 'basic'}
                        , algo={'Random':'basic'}
                        , matrix={'source':'ratings', 'row':'userId', 'col':'movieId', 'data':'rating'})

    #print(R2S.__dict__)

    # setting PopScore
    #R2S.algo.PopScore.scores = R2S.data['ratings']['movieId'].value_counts()
    #R2S.algo.PopScore.score_method = 'quantile'

    #print(R2S.algo.Random.items)
    #print(R2S.algo.PopScore.fit())

    # setting Random algo
    R2S.algo.Random.items = R2S.data['movies']['movieId'].to_numpy()

    arr = np.arange(170)

    n = 100
    use_cache = True

    #@timeit
    #def evaluateTime(arr, n, cache):
    #    R2S.algo.Random.recommend(user = arr, n=n, clean_cache=cache)


    #evaluateTime(arr,n,True)
    ts = time.time()
    R2S.algo.Random.recommend(user=arr, n= n, use_cache = use_cache)
    #cProfile.runctx('R2S.algo.Random.recommend(user, n, use_cache)', {'user' : arr, 'n': n, 'use_cache': use_cache},{})
   
    te = time.time()

    #for i in arr:
    #    print('User {} --> Recommendations {}'.format(i,R2S.algo.Random.rec[i][0:n]))

    print ('Time elapsed {} to run ({}) with the folling parameters {}'.format(te-ts,'Random',{'arr':len(arr), 'n': n, 'use cache':use_cache}) )

    from pympler import asizeof
    print ('R2S Object with {} kbytes'.format(asizeof.asizeof(R2S)/1024))
    return True



callR2S()

