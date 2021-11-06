import time
import zmq
import json 
import sys
from importlib import util
from argparse import Namespace



#def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
#def json2obj(data): return json.loads(data, object_hook=_json_object_hook)



def create_arg_dict(args):
    arg_dict = {}

    for idx in range(1,len(args)):
       arg = args[idx].split('=') 
       arg_dict[arg[0][2:]] = arg[1] 

    return Namespace(**arg_dict)
    #return R2SNamespace(**arg_dict)

def load_file_as_module(name, location):
    spec = util.spec_from_file_location(name, location)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://10.0.0.11:5555") 

while True:

    try:
        #  Wait for next request from client
        msg = socket.recv().decode('utf-8').split(',')
        print(msg)
        
        R2S = load_file_as_module('R2Szmq', msg[0])

        R2Sreturn = R2S.R2SProxyModule(create_arg_dict(msg))
        socket.send(json.dumps(R2Sreturn).encode('utf8'))

    except Exception as e:
        print(e)
        pass
    