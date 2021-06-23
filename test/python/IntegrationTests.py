import sys
import json

ret = json.loads('{ "r2sPid": 0}')
ret["r2sPid"] = sys.argv[1]
ret["return"] = int(sys.argv[2])

print(json.dumps(ret))

sys.exit(ret["return"])