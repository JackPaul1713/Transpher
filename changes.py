# Program Name: changes
# Description: Can find changes to a mpath using a saved version of the mpath before changes.
# Notes: root is the top mpath's path, use default MappedPath MappedAttributes

#TOD0#
#change#
# make get_changes get directory and file changes separately in that order

#add#
# boolean dir to all change objects

#do#
# actions
# funcs

#test#
# get_changes

#INIT#
#objects#
class Add():
    """
    addition change in a file path
    parameters: string name, float ctime
    """
    def __init__(self, name, ctime):
        self.type = 'add'
        self.name = name
        self.ctime = ctime
    def action(self):
        pass
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
        pass
class Move():
    """
    move change in a file path
    parameters: string name, float ctime, string new_path
    """
    def __init__(self, name, ctime, new_path):
        self.type = 'mov'
        self.name = name
        self.ctime = ctime
        self.new_path = new_path
    def action(self):
        pass
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
        pass

#funcs#
def get_changes(mpath_old, mpath_new): # DO
    """
    gets the changes between two similar mapped paths
    parameters: MappedPath mpath_old, MappedPath mpath_new | return: mixed[] changes
    """
    #init#
    def get_plus_recur(mpath_n, mpath_old, mpath_new):
        #init#
        changes = []
        #get changes mpath#
        #add#
        if mpath_old.search(mpath_n) == None:
            changes.append(Add(mpath_n.name, mpath_n.ctime))
            # mpath_old.add_mpath(mpath_n, mpath_new.search(mpath_n))
        else:
            #update#
            if mpath_old.get_mpath(mpath_old.search(mpath_n)).mtime != mpath_n.mtime:
                changes.append(Update(mpath_n.name, mpath_n.ctime))
                temp = mpath_old.get_mpath(mpath_old.search(mpath_n))
                temp.mtime = mpath_n.mtime
                # mpath_old.update_mpath(temp, mpath_old.search(mpath_n))
            #move#
            if mpath_old.get_mpath(mpath_old.search(mpath_n)).path != mpath_n.path:
                changes.append(Move(mpath_n.name, mpath_n.ctime, mpath_n.path))
                # mpath_old.move_mpath(mpath_old.search(mpath_n), mpath_new.search(mpath_n))
        #get changes sub_mpaths#
        for sub_mpath_n in mpath_n.sub_mpaths:
            changes = changes + get_plus_recur(sub_mpath_n, mpath_old, mpath_new)
        return(changes)
    def get_minus_recur(mpath_o, mpath_old, mpath_new):
        #init#
        changes = []
        #get changes mpath#
        #del#
        if mpath_new.search(mpath_o) == None:
            changes.append(Delete(mpath_o.name, mpath_o.ctime))
            # mpath_old.remove_mpath(mpath_old.search(mpath_o))
        #get changes sub_mpaths#
        for sub_mpath_o in mpath_o.sub_mpaths:
            changes = changes + get_minus_recur(sub_mpath_o, mpath_old, mpath_new)
        return(changes)
    changes = get_plus_recur(mpath_new, mpath_old, mpath_new) + get_minus_recur(mpath_old, mpath_old, mpath_new)
    return(changes)
def merge_changes(changes_a, changes_b):  # Look into what causes conflicts more... order and type may matter
    #init#
    merged_changes = []
    #merge#
    for change_a in changes_a:
        for change_b in changes_b():
            if change_a.ctime == change_b.ctime and (change_a.type == 'del' or change_b.type == 'del'):
                print('Conflict:')
                print('1. {} {} {}')
                print('2. {} {} {}')
                override = input('Override: ')
                # More here
    #ret#
    return

def make_changes(src_root, dest_root, changes):
    return
def make_trans_changes_u(src_root, trans_root, changes):
    #adds, updates
    return
def make_trans_changes_d(dest_root, trans_root, changes):
    #adds, updates
    #moves, deletes
    return

#MAIN#
if __name__ == '__main__':
    import mapping
    file = open('testing.txt', 'r')
    contents = file.read().split('\n')
    mpath_old = mapping.MappedPath(contents[0])
    mpath_new = mapping.MappedPath(contents[1])
    changes = get_changes(mpath_old, mpath_new)
    for change in changes:
        print('{} {} {}'.format(change.type, change.name, change.ctime))
    file.close()
    # print('No testing at this point')

# Author: Jack Paul Martin
# Start: 10/20/2020, Completion: