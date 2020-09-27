# Program Name: mapping
# Description:
# Notes: Keep .mdir file containing versions of file maps inside main dir

#init#
import os
from ctypes import windll, wintypes, byref

class MappedFile():
    def __init__(self, path):
        self.path = path
        self.name = self.path.split('\\')[-1]
        self.ctime = os.path.getctime(path)
        self.mtime = os.path.getmtime(path)

class MappedDir():
    def __init__(self, init):
        if os.path.exists(os.path.dirname(init)): # if init is a directory
            path = init
            self.path = path
            self.name = path.split('\\')[-1]
            self.ctime = os.path.getctime(path)
            self.sub_dir = [MappedDir(d.path) for d in os.scandir(self.path) if d.is_dir()]
            self.files = [MappedFile(f.path) for f in os.scandir(self.path) if f.is_file()]
            self.make_ctime_unique()
        else:  # if init is a mapped string
            mapped_dir_str = init
            # take id and fill out stf
            # separate sub_dir and files into two lists
            # find files from the front, cutting at '|' until '<'
            # while w != 0, where w = 1, if '<': w++, if '>' w--
            # split at the end position of while loop
            # make files out of id and fill files
            # call this function for each sub_dir

    #search#
    def search(self, mdir_find):
        def search_recur(mdir, mdir_find):
            if mdir.ctime == mdir_find.ctime: # search mdir
                return(mdir)
            for mfile in mdir.get_files(): # search mfiles
                if mfile.ctime == mdir_find.ctime:
                    return(mfile)
            for msub_dir in mdir.get_sub_dirs(): # search msub_dir
                ret = search_recur(msub_dir, mdir_find.ctime)
                if ret != None:
                    return(ret)
        return(search_recur(self, mdir_find))
    def search_dup(self, mdir_find):
        def search_recur(mdir, mdir_find):
            if mdir.ctime == mdir_find.ctime and mdir != mdir_find: # search mdir
                return (mdir)
            for mfile in mdir.get_files(): # search mfiles
                if mfile.ctime == mdir_find.ctime and mfile != mdir_find:
                    return (mfile)
            for msub_dir in mdir.get_sub_dirs(): # search msub_dir
                ret = search_recur(msub_dir, mdir_find.ctime)
                if ret != None:
                    return (ret)
        return(search_recur(self, mdir_find))

    #modify#
    def make_ctime_unique(self):
        def mod_ctime(path):
            timestamp = int((os.path.getctime(path) * 10000000) + 116444736000000000 + 10)
            ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
            handle = windll.kernel32.CreateFileW(path, 256, 0, None, 3, 128, None)
            windll.kernel32.SetFileTime(handle, byref(ctime), None, None)
            windll.kernel32.CloseHandle(handle)
        def make_ctime_unique_recur(mdir):
            if self.search_dup(mdir) != None:
                mod_ctime(mdir.path)
            for mfile in self.files:
                if self.search_dup(mfile) != None:
                    mod_ctime(mfile.path)
            for msub_dir in self.sub_dir:
                make_ctime_unique_recur(msub_dir)
        self.refresh()
    def refresh(self):
        self.ctime = os.path.getctime(self.path)
        self.sub_dir = [MappedDir(d.path) for d in os.scandir(self.path) if d.is_dir()]
        self.files = [MappedFile(f.path) for f in os.scandir(self.path) if f.is_file()]

    #output#
    def get_mdir_str(self):
        def make_id_str(dir):
            return (self.path + '*' + str(self.ctime))
        def get_mdir_str_recur(mdir):
            mdir_str = make_id_str(mdir) + '<' # add dir
            for file in mdir.get_files(): # add files
                mdir_str = mdir_str + make_id_str(file) + '|'
            for sub_dir in mdir.get_sub_dirs(): # add sub_dir
                mdir_str = mdir_str + get_mdir_str_recur(sub_dir) + '|'
            mdir_str = mdir_str + '\b' + '>'
            return(mdir_str)
        return(get_mdir_str_recur(self))
    def get_changes_of(self, mapped_dir): # moves, renames -then- adds, deletes
        # start at top dir
        # record changes
        # fix mapped_dir object
        # move downward
        # record changes
        # fix mapped_dir object
        return()

#testing#
if __name__ == '__main__':
    print("no testing at this point")
    # test ids next (file handles)
    # test compare_dir() next

# Author: Jack Paul Martin
#