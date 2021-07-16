import sys, json

sys.path.append('/source/R2S/src/util')

import R2S


def R2SProxyModule(args):
    return json.dumps(R2S.ProxyModule(args))


if __name__ == '__main__':
    args = R2S.ParseParameters()
    #print(args)
    ret = R2S.ProxyModule(args)
    print(json.dumps(ret))
    sys.exit(ret["return"]) #exit code of the script
