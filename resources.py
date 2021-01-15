# File Name: resources
# Description: some resources

#TOD0#

#INIT#
#imports#
import os
import datetime
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_WRITE, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, FILE_SHARE_WRITE
# from ctypes import windll, wintypes, byref

#func#
def mod_ctime(path):
    """
    changes the creation time of a file
    parameters: string path, int mod_size | return: none
    """
    ctime = os.path.getctime(path) + 0.001
    fh = CreateFile(path, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, 0)
    SetFileTime(fh, datetime.datetime.fromtimestamp(ctime), None, None)
    CloseHandle(fh)
def set_time(path, ctime=None, atime=None, mtime=None):
    """
    changes the creation time of a file to a certain time
    parameters: string path, int ctime | return: none
    """
    if ctime != None:
        ctime = datetime.datetime.fromtimestamp(ctime)
    if atime != None:
        atime = datetime.datetime.fromtimestamp(atime)
    if mtime != None:
        mtime = datetime.datetime.fromtimestamp(mtime)
    fh = CreateFile(path, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, 0)
    SetFileTime(fh, ctime, atime, mtime)
    CloseHandle(fh)
    # timestamp = int((ctime * 10000000) + 116444736000000000)
    # ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
    # handle = windll.kernel32.CreateFileW(path, 256, 0, None, 3, 128, None)
    # windll.kernel32.SetFileTime(handle, byref(ctime), None, None)
    # windll.kernel32.CloseHandle(handle)

#MAIN#
if __name__ == '__main__':
    #testing#
    print('no testing at this point')

# Author: Jack Paul Martin
# Start: 11/16/2020, Completion: >1/14/2021