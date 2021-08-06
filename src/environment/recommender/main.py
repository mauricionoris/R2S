import R2SObject
import pandas as pd
import numpy as np
from argparse import Namespace


args = "dataset={'name':'MovieLens', 'path':'/source/R2S/data/R2SDatasets/movielens'}, data={'ratings':None, 'movies': None, 'tags': None, 'links': None, 'genome-tags':None, 'genome-scores': None}, algo={'PopScore': './algoritms/PopScore.py'}"


#print(args)
R2S = R2SObject.R2S(dataset={'name':'MovieLens', 'path':'/source/R2S/data/R2SDatasets/movielens'}
#                     , data={'ratings':None, 'movies': None, 'tags': None, 'links': None, 'genome-tags':None, 'genome-scores': None}
                     , data={'ratings':None, 'movies': None}
                     , algo={'PopScore': 'basic', 'Random':'basic'}
                     , matrix={'source':'ratings', 'row':'userId', 'col':'movieId', 'data':'rating'})

#print(R2S.__dict__)

#print(R2S.__dict__)

R2S.algo.PopScore.scores = R2S.data['ratings']['movieId'].value_counts()
R2S.algo.PopScore.score_method = 'quantile'
"""

#print(len(R2S.algo.Random.items))
R2S.algo.Random.fit()
print(R2S.algo.Random.users)

"""

#print(R2S.algo.Random.items)


print(R2S.algo.PopScore.fit())
R2S.algo.Random.ui_coo = R2S.ui_coo
R2S.algo.Random.items = R2S.data['movies']['movieId'].to_numpy()

arr = np.arange(100)
print(arr)
R2S.algo.Random.recommend(arr.tolist())
#R2S.algo.Random.recommend()

print(R2S.algo.Random.rec)
