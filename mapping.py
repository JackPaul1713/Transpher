# Program Name: mapping
# Description: Maps out a path and records it. Uses created date as a unique id.
# Notes: .mpath files should be for containing string versions of mapped paths

#do#
# ADD exclusions

#init#
import os
from ctypes import windll, wintypes, byref

class MappedPath():
    def __init__(self, init):
        if 'C:\\' in init and '<' not in init: # if init is a directory # ADD exclusions here
            #init#
            path = init
            #construct#
            self.path = path
            self.name = path.split('\\')[-1]
            self.ctime = os.path.getctime(path)
            self.mtime = os.path.getmtime(path)
            if os.path.isdir(path):
                self.sub_mpaths = [MappedPath(p.path) for p in os.scandir(self.path)]
            else:
                self.sub_mpaths = []
        elif '<' in init: # if init is a mapped string
            #init#
            mpath_str = init
            def init_id_str(mpath, id_str):
                mpath.path = id_str.split('*')[0]
                mpath.name = mpath.path.split('\\')[-1]
                mpath.mtime = str(id_str.split('*')[2])
                mpath.ctime = str(id_str.split('*')[1])
                mpath.sub_mpaths = []
            #cut#
            id_str = mpath_str[0:mpath_str.find('<')]
            sub_mpaths_str = mpath_str[mpath_str.find('<')+1:len(mpath_str)-1]
            #init_id_str, construct#
            init_id_str(self, id_str)
            #split_mpaths_str, construct#
            while len(sub_mpaths_str) != 0:
                start = sub_mpaths_str.find('<')
                end = 0
                i = 0
                for c in range(start, len(sub_mpaths_str)):
                    if sub_mpaths_str[c] == '<':
                        i += 1
                    elif sub_mpaths_str[c] == '>':
                        i -= 1
                    if i == 0:
                        end = c
                        break
                if end >= start:
                    self.sub_mpaths.append(MappedPath(sub_mpaths_str[0:end+1]))
                sub_mpaths_str = sub_mpaths_str[end+1:len(sub_mpaths_str)]

    #search#
    def search(self, mpath_find): # CHANGE THIS, return a position list, pos[]
        def search_recur(mpath, mpath_find):
            #init#
            pos = []
            #search mpath#
            if mpath.ctime == mpath_find.ctime:
                return([])
            #search sub_mpath#
            for i in range(len(mpath.sub_mpaths)):
                ret = search_recur(mpath.sub_mpaths[i], mpath_find)
                if ret != None:
                    pos = ret
                    pos.insert(0, i)
                    return(pos)
        return(search_recur(self, mpath_find))
    def search_dup(self, mpath_find): # CHANGE THIS, return a position list, pos[]
        def search_recur(mpath, mpath_find):
            #init#
            pos = []
            #search mpath#
            if mpath.ctime == mpath_find.ctime and mpath != mpath_find:
                return([])
            #search sub_mpath#
            for i in range(len(mpath.sub_mpaths)):
                ret = search_recur(mpath.sub_mpaths[i], mpath_find)
                if ret != None:
                    pos = ret
                    pos.insert(0, i)
                    return(pos)
        return(search_recur(self, mpath_find))

    #modify#
    def get_mpath_at_pos(self, pos):
        mpath = self
        for p in pos:
            mpath = mpath.sub_mpaths[p]
        return(mpath)
    def add_mpath_at_pos(self, mpath_add, pos):
        def sub(mpath, mpath_add, pos):
            if len(pos) > 0:
                mpath.sub_mpaths[pos[0]] = sub(mpath.sub_mpaths[pos[0]], mpath_add, pos[1:len(pos)])
                return(mpath)
            elif len(pos) == 0:
                mpath.sub_mpaths.append(mpath_add)
                return(mpath)
        self.sub_mpaths = sub(self, mpath_add, pos).sub_mpaths
    def rem_mpath_at_pos(self, pos):
        def sub(mpath, pos):
            print('new_pos:', pos)
            if len(pos) > 1:
                mpath.sub_mpaths[pos[0]] = sub(mpath.sub_mpaths[pos[0]], pos[1:len(pos)])
                return(mpath)
            elif len(pos) == 1:
                mpath.sub_mpaths.pop(pos[0])
                return(mpath)
        self.sub_mpaths = sub(self, pos).sub_mpaths
    def move_mpath_at_pos(self, pos_from, pos_to):
        mpath = self.get_mpath_at_pos(pos_from)
        self.rem_mpath_at_pos(pos_from)
        self.add_mpath_at_pos(mpath, pos_to)
    def update_mpath_at_pos(self, mpath, pos):
        self.rem_mpath_at_pos(pos)
        self.add_mpath_at_pos(mpath, pos)

    def make_ctime_unique(self): # CHANGE THIS to work with updated search functions, remove refresh
        def mod_ctime(path, mod_size):
            timestamp = int((os.path.getctime(path) * 10000000) + 116444736000000000 + (10 * mod_size))
            ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
            handle = windll.kernel32.CreateFileW(path, 256, 0, None, 3, 128, None)
            windll.kernel32.SetFileTime(handle, byref(ctime), None, None)
            windll.kernel32.CloseHandle(handle)
        def make_ctime_unique_recur(mpath):
            counter = 1
            #make ctime unique for mpath#
            while True:
                if self.search_dup(mpath) != None:
                    mpath_dup_pos = self.search_dup(mpath)
                    mpath_dup = self.get_mpath_at_pos(mpath_dup_pos)
                    mod_ctime(mpath_dup.path, counter)
                    self.update_mpath_at_pos(MappedPath(mpath_dup.path), mpath_dup_pos)
                    counter += 1
                else:
                    break
            #make ctime unique for sub_mpaths#
            for sub_mpath in mpath.sub_mpaths:
                make_ctime_unique_recur(sub_mpath)
        make_ctime_unique_recur(self)
    def refresh(self):
        if os.path.isdir(self.path):
            self.sub_mpaths = [MappedPath(p.path) for p in os.scandir(self.path)]

    #output#
    def get_mpath_str(self):
        def make_id_str(mpath):
            return(mpath.path + '*' + str(mpath.ctime) + '*' + str(mpath.mtime))
        def get_mpath_str_recur(mpath):
            #add mpath#
            mpath_str = make_id_str(mpath) + '<'
            #add sub_mpaths#
            for sub_dir in mpath.sub_mpaths:
                mpath_str = mpath_str + get_mpath_str_recur(sub_dir)
            #close mpath#
            mpath_str = mpath_str + '>'
            return(mpath_str)
        return(get_mpath_str_recur(self))

#testing#
if __name__ == '__main__':
    test_mpath = MappedPath('a*0*0<b*0*0<c*0*0<d*0*0<>d1*0*0<e*0*0<>>>>b1*0*0<>>')
    print(test_mpath.get_mpath_str())
    test_mpath.make_ctime_unique()
    print(test_mpath.get_mpath_str())

# Author: Jack Paul Martin
# Start: idk, Completion: 10/20/2020ish