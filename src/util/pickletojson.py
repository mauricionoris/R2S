import pickle, json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
   

def transform(pickle_file):
    with open(pickle_file, 'rb') as cachehandle:
        new_dict =  pickle.load(cachehandle)
    return json.loads(json.dumps(new_dict, cls=NumpyEncoder))
 


if __name__ == '__main__':
    args = '/source/R2S/cache/d028d53bbde0d3cc5e2886e03ea2a6212e67a011.pickle'
    #args = '/source/R2S/cache/fe34f3ef0f1d85fd59fc4cade5cc5bf25160edbb.pickle'
    ret = transform(args)
    print(ret)
    
