import sys
import json

ret = json.loads('{ "r2sPid": 0}')

ret["r2sPid"] = sys.argv[1]

print(json.dumps(ret))
sys.exit(0)