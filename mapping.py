# Program Name: mapping
# Description: Maps out a path and records it. Uses created date as a unique id.
# Notes: .mpath files should be for containing string versions of mapped paths

#TOD0#
#add#
# boolean dir to MappedPath class
# boolean dir to both __init__ branches
# boolean dir to mpath_str

#do#
# none

#test#
# exclusions

#INIT#
#imports#
import os
import resources

#objects#
class MappedPath():
    '''
    description: makes a map of a directory and all it's sub directories and files using their path , creation time, and modification time or a mpath_str
    parameters: string path, string[] exclusions or string mpath.
    '''
    def __init__(self, init, exclusions=[]):
        if 'C:\\' in init and '<' not in init: # if init is a directory # ADD exclusions here
            #init#
            path = init
            #construct#
            self.path = path
            self.name = path.split('\\')[-1]
            self.ctime = os.path.getctime(path)
            self.mtime = os.path.getmtime(path)
            self.sub_mpaths = []
            if os.path.isdir(path):
                for p in os.scandir(self.path):
                    if p.path not in exclusions:
                        self.sub_mpaths.append(MappedPath(p.path, exclusions))
        elif '<' in init: # if init is a mapped string
            #init#
            mpath_str = init
            def init_id_str(mpath, id_str):
                mpath.path = id_str.split('*')[0]
                mpath.name = mpath.path.split('\\')[-1]
                mpath.ctime = float(id_str.split('*')[1])
                mpath.mtime = float(id_str.split('*')[2])
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
                    self.sub_mpaths.append(MappedPath(sub_mpaths_str[0:end + 1]))
                sub_mpaths_str = sub_mpaths_str[end+1:len(sub_mpaths_str)]

    #search#
    def search(self, mpath_find, func=lambda mpath: mpath.ctime):
        '''description: takes in a mapped path object and recursively searches itself for the mapped path and returns its position | parameters: self, MappedPath mpath_find, lambda func (optional) | return: int[] pos'''
        def search_recur(mpath, mpath_find, func):
            #init#
            pos = []
            #search mpath#
            if func(mpath) == func(mpath_find):
                return([])
            #search sub_mpath#
            for i in range(len(mpath.sub_mpaths)):
                ret = search_recur(mpath.sub_mpaths[i], mpath_find, func)
                if ret != None:
                    pos = ret
                    pos.insert(0, i)
                    return(pos)
        return(search_recur(self, mpath_find, func))
    def search_dup(self, mpath_find, func=lambda mpath: mpath.ctime):
        '''description: takes in a mapped path object and recursively searches itself for duplicate of the mapped path and return its position | parameters: self, MappedPath mpath_find, lambda func (optional) | return: int[] pos'''
        def search_recur(mpath, mpath_find, func):
            #init#
            pos = []
            #search mpath#
            if func(mpath) == func(mpath_find) and mpath != mpath_find:
                return([])
            #search sub_mpath#
            for i in range(len(mpath.sub_mpaths)):
                ret = search_recur(mpath.sub_mpaths[i], mpath_find, func)
                if ret != None:
                    pos = ret
                    pos.insert(0, i)
                    return(pos)
        return(search_recur(self, mpath_find, func))

    #modify#
    def get_mpath(self, pos):
        '''description: takes in position and returns the mapped path object at that position| parameters: self, int[] pos | return: MappedPath mpath'''
        mpath = self
        for p in pos:
            mpath = mpath.sub_mpaths[p]
        return(mpath)
    def add_mpath(self, mpath_add, pos):
        '''description: takes in a mapped path object and position and adds the mpath at that position | parameters: self, MappedPath mpath_add, int[] pos | return: None'''
        def sub(mpath, mpath_add, pos):
            if len(pos) > 1:
                mpath.sub_mpaths[pos[0]] = sub(mpath.sub_mpaths[pos[0]], mpath_add, pos[1:len(pos)])
                return(mpath)
            elif len(pos) == 1:
                mpath.sub_mpaths.insert(pos[0], mpath_add)
                return(mpath)
        self.sub_mpaths = sub(self, mpath_add, pos).sub_mpaths
    def remove_mpath(self, pos):
        '''description: takes in a position and removes the mapped path object at that position | parameters: int[] pos | return: None'''
        if len(pos) < 1:
            raise Exception('ValueError:', 'len(pos) must be >= 1')
        def sub(mpath, pos):
            if len(pos) > 1:
                mpath.sub_mpaths[pos[0]] = sub(mpath.sub_mpaths[pos[0]], pos[1:len(pos)])
                return(mpath)
            elif len(pos) == 1:
                mpath.sub_mpaths.pop(pos[0])
                return(mpath)
        self.sub_mpaths = sub(self, pos).sub_mpaths
    def move_mpath(self, pos_from, pos_to):
        '''description: takes in two positions and moves a mapped path object from one position to the other | parameters: int[] pos_from, int[] pos_to| return: None'''
        mpath = self.get_mpath(pos_from)
        self.remove_mpath(pos_from)
        self.add_mpath(mpath, pos_to)
    def update_mpath(self, mpath, pos):
        '''description: takes in a mapped path and a postion, and set's the mpath at the position to the mpath taken in | parameters: MappedPath mpath | return: None'''
        if len(pos) == 0:
            self = mpath
            return
        self.remove_mpath(pos)
        self.add_mpath(mpath, pos)

    def make_ctimes_unique(self):
        '''description: checks if there are duplicate creation times within a mapped path and if so increments the ctime by a few nanoseconds | parameters: None | return: None'''
        def make_ctime_unique(mpath):
            while True:
                if self.search_dup(mpath) != None:
                    mpath_dup_pos = self.search_dup(mpath)
                    mpath_dup = self.get_mpath(mpath_dup_pos)
                    resources.mod_ctime(mpath_dup.path)
                    self.update_mpath(MappedPath(mpath_dup.path), mpath_dup_pos)
                    make_ctime_unique(mpath_dup)
                else:
                    break
        def make_ctime_unique_recur(mpath):
            #make ctime unique for mpath#
            make_ctime_unique(mpath)
            #make ctime unique for sub_mpaths#
            for sub_mpath in mpath.sub_mpaths:
                make_ctime_unique_recur(sub_mpath)
        make_ctime_unique_recur(self)
    def refresh(self):
        '''description: refreshes a mapped path object using the actual directory | parameters: None | return: None '''
        if os.path.isdir(self.path):
            self.sub_mpaths = [MappedPath(p.path) for p in os.scandir(self.path)]

    #output#
    def get_mpath_str(self):
        '''description: returns a string version of itself | parameters: None | return: string mpath_str'''
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

#MAIN#
if __name__ == '__main__':
    #testing#
    mpath = MappedPath('a*0*0*0<b*1*0*0<d*0*0*0<5*0*0*0<>>2*0*0*0<>>c*0*0*0<3*0*0*0<>4*0*0*0<>>>')
    print(mpath.get_mpath_str())
    # print('no testing at this point')

# Author: Jack Paul Martin
# Start: idk, Completion: 10/20/2020ish