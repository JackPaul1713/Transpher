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

#testdir#
# exclusions

#INIT#
#imports#
import os
import resources

#object#
class MappedAttribute:
    """
    custom attributes for MappedPaths
    parameters: (func declaration, func id_declaration, int position)
    """
    def __init__(self, declaration, id_declaration, call):
        self.declaration = declaration
        self.id_declaration = id_declaration
        self.call = call

#func#
def dec_path(self, path):
    self.path = path
def dec_name(self, path):
    self.name = path.split('\\')[-1]
def dec_ctime(self, path):
    self.ctime = os.path.getctime(path)
def dec_mtime(self, path):
    self.mtime = os.path.getmtime(path)
def dec_dir(self, path):
    self.dir = os.path.isdir(path)

def idec_path(self, path):
    self.path = path
def idec_name(self, name):
    self.name = name
def idec_ctime(self, ctime):
    self.ctime = float(ctime)
def idec_mtime(self, mtime):
    self.mtime = float(mtime)
def idec_dir(self, dir):
    self.dir = bool(dir)

def call_path(self):
    return(self.path)
def call_name(self):
    return(self.name)
def call_ctime(self):
    return(self.ctime)
def call_mtime(self):
    return(self.mtime)
def call_dir(self):
    return(self.dir)

#var#
path_mattrib = MappedAttribute(dec_path, idec_path, call_path)
name_mattrib = MappedAttribute(dec_name, idec_name, call_name)
ctime_mattrib = MappedAttribute(dec_ctime, idec_ctime, call_ctime)
mtime_mattrib = MappedAttribute(dec_mtime, idec_mtime, call_mtime)
dir_mattrib = MappedAttribute(dec_dir, idec_dir, call_dir)

default_mattribs = [path_mattrib, name_mattrib, ctime_mattrib, mtime_mattrib, dir_mattrib]

#object#
class MappedPath:
    """
    makes a map of a directory and all it's sub directories and files using their path, creation time, and modification time or a mpath_str
    parameters: (string path, string[] exclusions) or (string mpath)
    """
    def __init__(self, path=None, mpath_str=None, mattribs=default_mattribs, exclusions=[]):
        if path != None:
            #construct#
            for mattrib in mattribs:
                mattrib.declaration(self, path)
            self.sub_mpaths = []
            if os.path.isdir(path):
                for p in os.scandir(path):
                    if p.path not in exclusions:
                        self.sub_mpaths.append(MappedPath(p.path, mattribs=mattribs, exclusions=exclusions))
        elif path == None and mpath_str != None:
            #cut#
            id_str = mpath_str[0:mpath_str.find('<')]
            sub_mpaths_str = mpath_str[mpath_str.find('<')+1:len(mpath_str)-1]
            #construct#
            i = 0
            for mattrib in mattribs:
                mattrib.id_declaration(self, id_str.split('*')[i])
                i += 1
            self.sub_mpaths = []
            #split mpaths_str, construct#
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
                    self.sub_mpaths.append(MappedPath(mpath_str=sub_mpaths_str[0:end + 1], mattribs=mattribs))
                sub_mpaths_str = sub_mpaths_str[end+1:len(sub_mpaths_str)]

    #search#
    def search(self, mpath_find, func=lambda mpath: mpath.ctime):
        """
        takes in a mapped path object and recursively searches itself for the mapped path and returns its position
        parameters: self, MappedPath mpath_find, lambda func (optional) | return: int[] pos
        """
        #search mpath#
        if func(self) == func(mpath_find):
            return([])
        #search sub_mpath#
        for i in range(len(self.sub_mpaths)):
            pos = self.sub_mpaths[i].search(mpath_find, func)
            if pos != None:
                pos.insert(0, i)
                return(pos)

    def search_dup(self, mpath_find, func=lambda mpath: mpath.ctime):
        """
        takes in a mapped path object and recursively searches itself for duplicate of the mapped path and return its position
        parameters: self, MappedPath mpath_find, lambda func (optional) | return: int[] pos
        """
        #search mpath#
        if func(self) == func(mpath_find) and self != mpath_find:
            return([])
        #search sub_mpath#
        for i in range(len(self.sub_mpaths)):
            ret = self.sub_mpaths[i].search_dup(mpath_find, func)
            if ret != None:
                pos = ret
                pos.insert(0, i)
                return(pos)

    #modify#
    def get_mpath(self, pos):
        """
        takes in position and returns the mapped path object at that position
        parameters: self, int[] pos | return: MappedPath mpath
        """
        mpath = self
        for p in pos:
            mpath = mpath.sub_mpaths[p]
        return(mpath)
    def add_mpath(self, mpath_add, pos):
        """
        takes in a mapped path object and position and adds the mpath at that position
        parameters: self, MappedPath mpath_add, int[] pos | return: none
        """
        if len(pos) > 1:
            self.sub_mpaths[pos[0]] = self.sub_mpaths[pos[0]].add_mpath(mpath_add, pos[1:len(pos)])
        elif len(pos) == 1:
            self.sub_mpaths.insert(pos[0], mpath_add)
    def remove_mpath(self, pos):
        """
        takes in a position and removes the mapped path object at that position
        parameters: int[] pos | return: none
        """
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
        """
        takes in two positions and moves a mapped path object from one position to the other
        parameters: int[] pos_from, int[] pos_to| return: none
        """
        mpath = self.get_mpath(pos_from)
        self.remove_mpath(pos_from)
        self.add_mpath(mpath, pos_to)
    def update_mpath(self, mpath, pos):
        """
        takes in a mapped path and a postion, and set's the mpath at the position to the mpath taken in
        parameters: MappedPath mpath | return: None
        """
        if len(pos) == 0:
            self = mpath
            return
        self.remove_mpath(pos)
        self.add_mpath(mpath, pos)

    def make_ctimes_unique(self):
        """
        checks if there are duplicate creation times within a mapped path and if so increments the ctime by a few nanoseconds
        parameters: none | return: none
        """
        #init#
        def make_ctime_unique(mpath):
            while True:
                if self.search_dup(mpath) != None:
                    #get duplicate#
                    mpath_dup_pos = self.search_dup(mpath)
                    mpath_dup = self.get_mpath(mpath_dup_pos)
                    resources.mod_ctime(mpath_dup.path)
                    self.update_mpath(MappedPath(mpath_dup.path), mpath_dup_pos)
                    make_ctime_unique(mpath_dup)
                else:
                    break
        #make ctime unique for mpath#
        make_ctime_unique(self)
        #make ctime unique for sub_mpaths#
        for sub_mpath in self.sub_mpaths:
            sub_mpath.make_ctimes_unique()
    def refresh(self):
        """
        refreshes a mapped path object using the actual directory
        parameters: none | return: none
        """
        if os.path.isdir(self.path):
            self.sub_mpaths = [MappedPath(p.path) for p in os.scandir(self.path)]

    #output#
    def get_mpath_str(self, mattribs=default_mattribs):
        """
        returns a string version of itself
        parameters: None | return: string mpath_str
        """
        #add mpath#
        id_str = ''
        for mattrib in mattribs:
            id_str += str(mattrib.call(self)) + '*'
        mpath_str = id_str[0:-1] + '<'
        #add sub_mpaths#
        for sub_dir in self.sub_mpaths:
            mpath_str += sub_dir.get_mpath_str(mattribs)
        #close mpath#
        mpath_str = mpath_str + '>'
        #ret#
        return(mpath_str)

# Author: Jack Paul Martin
# Start: idk, Completion: 12/7/2020ish