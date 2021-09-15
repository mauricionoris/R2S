import sys

sys.path.append('/source/R2S/src/util')
sys.path.append('/source/R2S/src/environment/recommender')


#from R2Sprofile import profileit
import R2SObject
import pandas as pd
import numpy as np
import argparse 


parser=argparse.ArgumentParser()

import time                                                



#@profileit
def callR2S(env_setup, parameters, action=0):

    print(env.__dict__)
    print(param.__dict__)
    #Setting the Environment
    MyEnvironment = R2SObject.R2S(env_setup)

    #Executing an action

    print('available algorithms')
        

    #ret = R2S.algo.Random.recommend(users=param.users, n= param.n)
    for available_algorithm in MyEnvironment.algo:
        
        ts = time.time()
        ret = MyEnvironment.algo[available_algorithm].recommend(parameters)
        te = time.time()

        for i in parameters.users:
            print('User {} --> Recommendations {}'.format(i,ret[str(i)]))

        print ('Time elapsed {} to run ({}) with the folling parameters {}'.format(te-ts, available_algorithm, parameters) )
        print(ret['metadata'])


    return 0

if __name__ == '__main__':

    env = argparse.Namespace(dataset={'name':'MovieLens', 'path':'/source/R2S/data/R2SDatasets/movielens'}
#                   , data={'ratings':None, 'movies': None, 'tags': None, 'links': None, 'genome-tags':None, 'genome-scores': None}
                    , data={'ratings':None, 'movies': None} #TODO: specify the columns to load to avoid loading the whole file
                    , matrix={'source':'ratings', 'row':'userId', 'col':'movieId', 'data':'rating'}
                    , algo={ 'Random':'basic','PopScore': 'basic'}
#                   , algo={'PopScore': 'basic'}
#                   , algo={'Random':'basic'}
                    , algodata={'Random':{'items':{'dataset':'movies', 'feature':'movieId'}}
                               ,'PopScore':{'scores':{'dataset':'ratings','feature':'movieId'}}})

    param = argparse.Namespace(users = [25,26,27,28,29,30], n = 10, score_method = 'count')


    action = argparse.Namespace(t0 = {'algo':'Random'})

    #print(args)
    print(callR2S(env, param, action))
    sys.exit(0) #exit code of the script

