# File Name: mapping
# Description: maps a file system at a path
# Notes: custom mapped attributes can be used for MappedPath

#TOD0#
# test mattributes
# test mpath modifiers

#INIT#
#imports#
import os
import resources

#object#
class MappedAttribute:
    """
    custom attributes for MappedPaths
    parameters: func declaration, func id_declaration, func call
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
    self.ctime = round(os.path.getctime(path), 3)
def dec_mtime(self, path):
    self.mtime = round(os.path.getmtime(path), 3)
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
    def search_attrib(self, attrib_find, func):
        """
        takes in a mapped path object and recursively searches itself for the mapped path and returns its position
        parameters: self, MappedPath mpath_find, lambda func (optional) | return: int[] pos
        """
        #search mpath#
        if func(self) == attrib_find:
            return([])
        #search sub_mpath#
        for i in range(len(self.sub_mpaths)):
            pos = self.sub_mpaths[i].search_attrib(attrib_find, func)
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
            self.sub_mpaths[pos[0]].add_mpath(mpath_add, pos[1:len(pos)])
        elif len(pos) == 1:
            self.sub_mpaths.insert(pos[0], mpath_add)
    def remove_mpath(self, pos):
        """
        takes in a position and removes the mapped path object at that position
        parameters: int[] pos | return: none
        """
        if len(pos) < 1:
            raise Exception('ValueError:', 'len(pos) must be >= 1')
        if len(pos) > 1:
            self.sub_mpaths[pos[0]].remove_mpath(pos[1:len(pos)])
        elif len(pos) == 1:
            self.sub_mpaths.pop(pos[0])
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

#MAIN#
#testing#
if __name__ == '__main__':
    #init#
    def disp_test_title(name):
        print('test:', name)
    def disp_test_output(output):
        print('output:', output, end='\n\n')
    test_dir = 'testdir\\original'

    #title#
    print('mapping testing\n')

    #switches#
    mattributes_switch = False
    mpath_switch = True

    #tests#
    if mattributes_switch:
        # TEST THIS
        pass
    if mpath_switch:
        #switches#
        init_switch = True
        search_switch = True
        modify_switch = True
        output_switch = True
        #tests#
        if init_switch:
            disp_test_title('init path')
            mpath = MappedPath(test_dir)
            mpath_str = mpath.get_mpath_str()
            disp_test_output(mpath_str)

            disp_test_title('init path with exclusions')
            mpath_ex = MappedPath(test_dir, exclusions=[test_dir + '\\symb'])
            mpath_ex_str = mpath_ex.get_mpath_str()
            disp_test_output(mpath_ex_str)

            disp_test_title('init path with different mapped attributes')
            mpath_ma = MappedPath(test_dir, mattribs=[name_mattrib])
            mpath_ma_str = mpath_ma.get_mpath_str(mattribs=[name_mattrib])
            disp_test_output(mpath_ma_str)

            disp_test_title('init mpath_str')
            mpath_s = MappedPath(mpath_str=mpath_str)
            mpath_s_str = mpath_s.get_mpath_str()
            disp_test_output(mpath_s_str)
        if search_switch:
            mpath = MappedPath(test_dir)
            disp_test_title('search for directory')
            mpath_search_dir = MappedPath(mpath_str=test_dir + '\\symb*symb*0*0*True<>')
            disp_test_output(mpath.search(mpath_search_dir, lambda mpath: mpath.name))

            disp_test_title('search for file')
            mpath_search_file = MappedPath(mpath_str=test_dir + '\\alpha\\a.txt*a.txt*0*0*False<>')
            disp_test_output(mpath.search(mpath_search_file, lambda mpath: mpath.name))

            disp_test_title('search for nonexistent')
            disp_test_output(mpath.search(mpath_search_dir))  # ctime is 0

            disp_test_title('search_dup for duplicate')
            disp_test_output(mpath.search_dup(mpath_search_dir, lambda mpath: mpath.name))

            disp_test_title('search_dup for nonexistent')
            disp_test_output(mpath.search_dup(mpath_search_dir))  # ctime is 0
        if modify_switch:
            disp_test_title('get')
            mpath = MappedPath(test_dir, mattribs=[name_mattrib])
            mpath_get = mpath.get_mpath([0])
            mpath_get_str = mpath_get.get_mpath_str(mattribs=[name_mattrib])
            disp_test_output('[0]: ' + mpath_get_str)

            disp_test_title('add')
            mpath_add = mpath_get
            mpath_add.add_mpath(mpath_get.get_mpath([0]), [1, 0])
            mpath_add_str = mpath_add.get_mpath_str(mattribs=[name_mattrib])
            disp_test_output('[0, 0]: ' + mpath_add_str)

            disp_test_title('remove')
            # TEST THIS

            disp_test_title('move')
            # TEST THIS

            disp_test_title('update')
            # TEST THIS
        if output_switch:
            disp_test_title('get mapped path string')  # uhh used for most of the previous tests lol
            mpath = MappedPath(test_dir)
            mpath_str = mpath.get_mpath_str()
            disp_test_output(mpath_str)

# Author: Jack Paul Martin
# Start: idk, Completion: 1/29/2021