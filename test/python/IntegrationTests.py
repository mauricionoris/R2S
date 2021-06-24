import sys
import json
import logging


logging.basicConfig(filename = './source/R2S/log/R2S.log',
                    encoding='utf-8',
                    format='%(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


if sys.argv[3] != "null":
    logs = sys.argv[3].split(',')
    for item in logs:
        logging.info('%s %s', sys.argv[1], item)



ret = json.loads('{ "r2sPid": 0}')
ret["r2sPid"] = sys.argv[1]
ret["return"] = int(sys.argv[2])

print(json.dumps(ret)) #puts a json on stout
sys.exit(ret["return"]) #exit code of the script