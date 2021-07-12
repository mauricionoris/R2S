import argparse, sys, os
import json
import logging

parser=argparse.ArgumentParser()


parser.add_argument('--log'     ,  '-l', help="Register the interaction to the log")
parser.add_argument('--logfile' , '-lf', help="Path to the log file")
parser.add_argument('--r2sPid'  , '-id', help="The executing Id of R2S")
parser.add_argument('--ret'     ,  '-r', help="The determined script return (for tests only)")
parser.add_argument('--function',  '-f', help="The function which should be called from here")


ret = json.loads('{"r2sPid": 0, "return": 1000, "exitCode": 100}')



def R2Sselector(func, args):
    if func == 'ArrowTesting':
        from arrowTest import arrowTest
        return arrowTest(args)
    if func == 'b':
        return 2

def R2STestingModule(args):

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
    return json.dumps(ret) #puts a json on stout
    

if __name__ == '__main__':
    args = parser.parse_args()
    #print(args)
    print(R2STestingModule(args))
    sys.exit(ret["return"]) #exit code of the script
