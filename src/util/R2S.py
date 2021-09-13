import argparse, sys, os
import json
import logging

     
sys.path.append('/source/R2S/src/environment/setup')
sys.path.append('/source/R2S/src/environment/recommender')

parser=argparse.ArgumentParser()

parser.add_argument('--folder_path'  , '-dp'  , help="Folder path")
parser.add_argument('--file_path'    , '-fp'  , help="Path to a specific file")
parser.add_argument('--r2sPid'       , '-id'  , help="The executing Id of R2S")
parser.add_argument('--extension'    , '-ext' , help="A file extension")
parser.add_argument('--ret'          ,  '-r'  , help="The determined script return (for tests only)")
parser.add_argument('--function'     ,  '-f'  , help="The function which should be called from here")
parser.add_argument('--log'          ,  '-l'  , help="Register the interaction to the log")
parser.add_argument('--logfile'      , '-lf'  , help="Path to the log file")

ret = json.loads('{"r2sPid": 0, "return": 1000, "exitCode": 100}')

def ParseParameters():
    return parser.parse_args()


def R2Sselector(func, args):
    if func == 'ArrowTesting':
        from arrowTest import arrowTest
        return arrowTest(args)

    if func == 'read_folder':
        from fileHandler import read_folder
        return {'files': read_folder(args.folder_path, args.extension)}

    if func == 'read_pickle':
        from pickletojson import transform
        return {'data': transform(args.file_path)} #{'data':[1,2,3,4]}
        #print(str(r)[-1])

    if func == 'create_folder':
        from fileHandler import create_folder
        return create_folder(args.folder_path)

    if func == 'file_size':
        from fileHandler import file_size
        return {'file_size' : file_size(args.file_path)}
    
    if func == 'import_dataset':
        from preparation import import_dataset
        return {'imported_files': import_dataset(args)}
    
    if func == 'recommend':
        from agent import callR2S
        return {'metadata': callR2S(args)}


def R2SProxyModule(args):
    return json.dumps(ProxyModule(args))


def ProxyModule(args):

    if args.function != "":
        ret.update(R2Sselector(args.function, args))
  

    if args.r2sPid != None:
        ret["r2sPid"] = args.r2sPid

    if args.ret != "":
        ret["return"] = int(args.ret)

    if args.log != "" :
        logging.basicConfig(filename = args.logfile,
                        encoding='utf-8',
                        format='%(asctime)s - %(message)s', 
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO)

        logging.info('%s %s', ret["r2sPid"], args.log)
    

    ret["exitCode"]=ret["return"]

    return ret #puts a json on stout


if __name__ == '__main__':
    args = parser.parse_args()
    #print(args)
    print(R2SProxyModule(args))
    sys.exit(ret["return"]) #exit code of the script