import argparse, sys, os
import secrets
import json

parser=argparse.ArgumentParser()

ret = json.loads('{"r2sPid": 0, "return": 1000, "exitCode": 100}')

parser.add_argument('--folder_path'  , '-dp'  , help="Folder path")
parser.add_argument('--file_path'    , '-fp'  , help="Path to a specific file")
parser.add_argument('--r2sPid'       , '-id'  , help="The executing Id of R2S")
parser.add_argument('--extension'    , '-ext' , help="A file extension")
parser.add_argument('--ret'          ,  '-r'  , help="The determined script return (for tests only)")
parser.add_argument('--function'     ,  '-f'  , help="The function which should be called from here")
parser.add_argument('--log'          ,  '-l'  , help="Register the interaction to the log")
parser.add_argument('--logfile'      , '-lf'  , help="Path to the log file")



def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return {'file_size' : file_info.st_size} # convert_bytes(file_info.st_size)}

def create_folder(folder_path):

    # define the access rights
    access_rights = 0o755
    if os.path.exists(folder_path):
        os.rename(folder_path, folder_path + '_' + secrets.token_hex(8))
    os.mkdir(folder_path, access_rights)
    return {}

#    try:
#    except OSError:
#        print ("Creation of the directory %s failed" % folder_path)
#    else:
#        print ("Successfully created the directory %s" % folder_path)


def read_folder(folder_path, extension):
    files = []
    for FILE in os.listdir(folder_path):
        if FILE.endswith("." + extension):
            files.append(FILE)
    
    return {'files': files}



def R2Sselector(func, args):
    if func == 'read_folder':
        return read_folder(args.folder_path, args.extension)
    if func == 'create_folder':
        return create_folder(args.folder_path)
    if func == 'file_size':
        return file_size(args.file_path)


def R2SProxyModule(args):

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
    print(R2SProxyModule(args))
    sys.exit(ret["return"]) #exit code of the script
