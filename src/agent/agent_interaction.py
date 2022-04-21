import sys

sys.path.append('/source/R2S/src/util')
sys.path.append('/source/R2S/src/environment/recommender')


#from R2Sprofile import profileit
import R2SObject
#import pandas as pd
import numpy as np
import argparse 
from argparse import Namespace


parser=argparse.ArgumentParser()

import time                                                



#@profileit
def callR2S(env, action, parameters):

    #print('Environment:', env)
    #print('Action:', action)
    #print('parameters:', parameters)
    

    #Setting the Environment
    R2SEnv = R2SObject.R2S(env)

    #Executing an action
    ts = time.time()
    ret = R2SEnv.algo[action.algo].recommend(parameters)
    te = time.time()

    for i in parameters.users:
        print('User {} --> Recommendations {}'.format(i,ret[str(i)]))

    print ('Time elapsed {} to run {} algorithm '.format(te-ts, action.algo) )
    
    """"
    print(ret['metadata'])

    #JUST FOR TESTING PURPOSES. It will execute an algorithm setted at the action parameter
    print('available algorithms')

    for available_algorithm in R2SEnv.algo:
        ts = time.time()
        ret = R2SEnv.algo[available_algorithm].recommend(parameters)
        te = time.time()
       for i in parameters.users:
            print('User {} --> Recommendations {}'.format(i,ret[str(i)]))
        print ('Time elapsed {} to run {} algorithm '.format(te-ts, available_algorithm) )
        print(ret['metadata'])cd 
    """
    return ret['metadata']


if __name__ == '__main__':

#                   , algo={'PopScore': 'basic'}
#                   , algo={'Random':'basic'}
#                   , data={'ratings':None, 'movies': None, 'tags': None, 'links': None, 'genome-tags':None, 'genome-scores': None}


    env = argparse.Namespace(dataset={'name':'MovieLens', 'path':'/source/R2S/data/R2SDatasets/movielens'}
                    , data={'ratings':None, 'movies': None} #TODO: specify the columns to load to avoid loading the whole file
                    , matrix={'source':'ratings', 'row':'userId', 'col':'movieId', 'data':'rating'} #format to allow algo computations (on env load ?!?)
                    , algo={ 'Random':'basic'
                           ,'PopScore': 'basic'
                           , 'R2SWrapper_ItemItem':'collaborative_ItemItem'
                           , 'R2SWrapper_UserUser':'collaborative_UserUser'
                           } #list of avalilable algos ---- each env. does not need to have all algos .... 

                    , algodata={'Random':{'items':{'dataset':'movies', 'feature':'movieId'}}  # especific to each algo .... 
                               ,'PopScore':{'scores':{'dataset':'ratings','feature':'movieId'}}
                               ,'R2SWrapper_ItemItem':{'ratings':['userId']}
                               ,'R2SWrapper_UserUser':{'ratings':['userId']}
                               })
                               

    action = argparse.Namespace(algo = 'R2SWrapper_UserUser')
    #param = argparse.Namespace(users = [25,26,27], n = 3, score_method = 'count')
    param = argparse.Namespace(users = [25,26,27], n = 3, nnbrs = 5, save_nbrs=5)
    
    #print(args)
    print(callR2S(env, action, param))
    sys.exit(0) #exit code of the script

