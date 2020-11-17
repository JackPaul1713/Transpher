# Program Name: mapping
# Description: Maps out a path and records it. Uses created date as a unique id.
# Notes: .mpath files should be for containing string versions of mapped paths

#TOD0#
#add#
# none
#do#
# none
#test#
# none

#INIT#
#imports#
import os
from ctypes import windll, wintypes, byref

#func#
def mod_ctime(path, mod_size):
    '''description: changes the creation time of a file | parameters: string path, int mod_size | return: None '''
    timestamp = int((os.path.getctime(path) * 10000000) + 116444736000000000 + (10 * mod_size))
    ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
    handle = windll.kernel32.CreateFileW(path, 256, 0, None, 3, 128, None)
    windll.kernel32.SetFileTime(handle, byref(ctime), None, None)
    windll.kernel32.CloseHandle(handle)
def set_ctime(path, ctime):
    '''description: changes the creation time of a file to a certain time | parameters: string path, int ctime | return: None '''
    timestamp = int((ctime * 10000000) + 116444736000000000)
    ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
    handle = windll.kernel32.CreateFileW(path, 256, 0, None, 3, 128, None)
    windll.kernel32.SetFileTime(handle, byref(ctime), None, None)
    windll.kernel32.CloseHandle(handle)

#MAIN#
if __name__ == '__main__':
    #testing#
    print('no testing at this point')

# Author: Jack Paul Martin
# Start: 11/16/2020, Completion: