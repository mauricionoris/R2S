import os, secrets, pickle

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
        return file_info.st_size # convert_bytes(file_info.st_size)}

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
    
    return  files


def read_pickle(file_path):
    with open(file_path, 'rb') as cachehandle:
        return pickle.load(cachehandle)


def write_pickle(file_path): #TODO
    files = []
    for FILE in os.listdir(folder_path):
        if FILE.endswith("." + extension):
            files.append(FILE)
    
    return  files


