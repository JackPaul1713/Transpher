# File Name: resources
# Description: some resources




#### INIT ####
#### imports ####
import os
import datetime
import shutil
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_WRITE, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, FILE_SHARE_WRITE
# from ctypes import windll, wintypes, byref


#### func ####
    #### time ####
def mod_ctime(path):
    """
    increments file creation time by a nanosecond
    parameters: string path, int mod_size | return: none
    """
    ctime = os.path.getctime(path) + 0.001  # increment ctime by 0.001
    fh = CreateFile(path, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, 0)
    SetFileTime(fh, datetime.datetime.fromtimestamp(ctime), None, None)  # update file ctime
    CloseHandle(fh)

def set_time(path, ctime=None, atime=None, mtime=None):
    """
    changes file times to input times
    parameters: string path, int ctime | return: none
    """
    # get datetime value of time if time has a value
    if ctime != None:
        ctime = datetime.datetime.fromtimestamp(ctime)
    if atime != None:
        atime = datetime.datetime.fromtimestamp(atime)
    if mtime != None:
        mtime = datetime.datetime.fromtimestamp(mtime)
    fh = CreateFile(path, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, 0)
    SetFileTime(fh, ctime, atime, mtime)  # update file times (None value keeps previous value)
    CloseHandle(fh)
    # alternate method(more precise but does not work on directories):
    # timestamp = int((ctime * 10000000) + 116444736000000000)
    # ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
    # handle = windll.kernel32.CreateFileW(path, 256, 0, None, 3, 128, None)
    # windll.kernel32.SetFileTime(handle, byref(ctime), None, None)
    # windll.kernel32.CloseHandle(handle)


    #### file_opts ####
def make_file(path):
    """
    makes a new file at the path
    """
    file = open(path, 'w')
    file.close()

def make_dir(path):
    """
    makes a new directory at the path
    """
    os.mkdir(path)

def delete_file(path):
    """
    deletes the file at the path
    """
    if not os.path.isdir(path):  # not directory
        os.remove(path)
    elif os.path.isdir(path):  # directory
        shutil.rmtree(path)

def write_file(path, mod):
    """
    writes to the file at path
    """
    file = open(path, 'w')
    file.write(mod)
    file.close()

def rename_file(old_path, new_path):
    """
    renames the file at path0 to path1
    """
    os.rename(old_path, new_path)

def copy_file(src_path, dst_path):
    """
    copies a file from path0 to path1
    """
    if not os.path.isdir(src_path):  # not directory
        shutil.copyfile(src_path, dst_path)
    elif os.path.isdir(src_path):  # directory
        shutil.copytree(src_path, dst_path)




# Author: Jack Paul Martin
# Start: 11/16/2020, Completion: 1/27/2021