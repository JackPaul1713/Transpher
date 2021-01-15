# File Name: changes
# Description: can find changes to a mpath using a saved version of the mpath before changes.

#TOD0#
# do actions for change objects, ADD, DEL, UPD, MOV
# do sort function
# do merge functions
# do modify functions

#INIT#
#objects#
class Add():
    """
    addition change in a file path
    parameters: string name, float ctime
    """
    def __init__(self, name, ctime, dst_name, dst_ctime):
        self.type = 'add'
        self.name = name
        self.ctime = ctime
        self.dst_name = dst_name
        self.dst_ctime = dst_ctime
    def action(self):
        print('Add {} to {}'.format(self.name, self.dst_name))
class Delete():
    """
    delete change in a file path
    parameters: string name, float ctime
    """
    def __init__(self, name, ctime):
        self.type = 'del'
        self.name = name
        self.ctime = ctime
    def action(self):
        print('Delete {}'.format(self.name))
class Move():
    """
    move change in a file path
    parameters: string name, float ctime, string new_path
    """
    def __init__(self, name, ctime, dst_name, dst_ctime):
        self.type = 'mov'
        self.name = name
        self.ctime = ctime
        self.dst_name = dst_name
        self.dst_ctime = dst_ctime
    def action(self):
        print('Move {} to {}'.format(self.name, self.dst_name))
class Update():
    """
    update change in a file path
    parameters: string name, float ctime
    """
    def __init__(self, name, ctime):
        self.type = 'upd'
        self.name = name
        self.ctime = ctime
    def action(self):
        print('Update {}'.format(self.name))

#funcs#
def get_super_path(path):
    '''
    gets the path to the file that contains the file the input path leads to
    parameters: string path | return: string super_path
    '''
    path_list = path.split('\\')
    path_list[0:-1]
    super_path = ''
    for file in path_list:
        super_path += '\\'
    super_path += '\b'
    return(super_path)
def get_super_mpath(mpath, sub_mpath):
    '''
    gets the mapped path the sub_mpath is contained in from a master mpath
    parameters: MappedPath mpath, MappedPath sub_mpath | return: MappedPath super_mpath
    '''
    pos = mpath.search(sub_mpath)[0:-1]
    super_mpath = mpath.get_mpath(pos)
    return(super_mpath)

def get_changes(mpath_old, mpath_new): # DO
    """
    gets the changes between two similar mapped paths
    parameters: MappedPath mpath_old, MappedPath mpath_new | return: mixed[] changes
    """
    #init#
    def get_pos_changes(mpath_n, mpath_old, mpath_new):
        #init#
        changes = [] # ADD bc you could mov something to something added but not move something that does not exist yet, MOV UPD DEL bc the order of the rest doesn't matter
        super_mpath_n = get_super_mpath(mpath_new, mpath_n)
        #get changes mpath#
        #add#
        if mpath_old.search(mpath_n) == None:
            name = mpath_n.name
            ctime = mpath_n.ctime
            dst_name = super_mpath_n.name
            dst_ctime = super_mpath_n.ctime
            change = Add(name, ctime, dst_name, dst_ctime)
            changes.append(change)
        else:
            # move#
            if get_super_mpath(mpath_old, mpath_old.get_mpath(mpath_old.search(mpath_n))).ctime != super_mpath_n.ctime:
                name = mpath_n.name
                ctime = mpath_n.ctime
                dst_name = super_mpath_n.name
                dst_ctime = super_mpath_n.ctime
                change = Move(name, ctime, dst_name, dst_ctime)
                changes.append(change)
            #update#
            if mpath_old.get_mpath(mpath_old.search(mpath_n)).mtime != mpath_n.mtime:
                if not mpath_n.dir:
                    change = Update(mpath_n.name, mpath_n.ctime)
                    changes.append(change)
        #get changes sub_mpaths#
        for sub_mpath_n in mpath_n.sub_mpaths:
            changes = changes + get_pos_changes(sub_mpath_n, mpath_old, mpath_new)
        return(changes)
    def get_neg_changes(mpath_o, mpath_old, mpath_new):
        #init#
        changes = []
        #get changes mpath#
        #del#
        if mpath_new.search(mpath_o) == None:
            name = mpath_o.name
            ctime = mpath_o.ctime
            change = Delete(name, ctime)
            changes.append(change)
        #get changes sub_mpaths#
        for sub_mpath_o in mpath_o.sub_mpaths:
            changes = changes + get_neg_changes(sub_mpath_o, mpath_old, mpath_new)
        return(changes)
    changes = get_pos_changes(mpath_new, mpath_old, mpath_new) + get_neg_changes(mpath_old, mpath_old, mpath_new)
    return(changes)
def sort_changes(changes):
    '''
    sorts changes to the order they should be made in
    parameters: list changes | return: dict changes
    '''
    sorted_changes = {'add':[], 'mov':[], 'upd':[], 'del':[]}
    pass

def soft_merge_changes(changes0, changes1):  # Look into what causes conflicts more... order and type may matter
    pass
def hard_merge_changes(change0, change1):
    pass

def upload_changes():
    #adds, updates
    return
def make_changes():
    return

# Author: Jack Paul Martin
# Start: 10/20/2020, Completion: