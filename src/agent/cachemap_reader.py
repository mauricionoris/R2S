import os
import pickle
import hashlib


cache_path = '/source/R2S/cache/'
cachemap_path = '/source/R2S/cache/cachemap.pickle'



with open(cachemap_path, 'rb') as cachehandle:
    cachemap =  pickle.load(cachehandle)



print(cachemap)
         