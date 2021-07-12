import os
import uuid

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
        return convert_bytes(file_info.st_size)


def create_folder(folder_path):

    # define the access rights
    access_rights = 0o755

    try:
        if os.path.exists(folder_path):
            os.rename(folder_path, folder_path + join(str(uuid.uuid4()).split('-')))
        os.mkdir(path, access_rights)
    except OSError:
        print ("Creation of the directory %s failed" % folder_path)
    else:
        print ("Successfully created the directory %s" % folder_path)
    return 0


def read_folder(folder_path, extension):
    files = []
    for FILE in os.listdir(folder_path):
        if FILE.endswith("." + extension):
            files.push(FILE)
    
    return files
