# Program Name: changes
# Description: Can find changes to a mpath using a saved version of the mpath before changes.
# Notes: root is the top mpath's path

#do#
# DO actions
# DO funcs

#init#
class Add():
    def __init__(self, path):
        self.type = 'add'
        self.path = path
    def action(self):
        return
class Delete():
    def __init__(self, path):
        self.type = 'del'
        self.path = path
    def action(self):
        return
class Move():
    def __init__(self, src_path, dest_path):
        self.type = 'mov'
        self.src = src_path
        self.dest = dest_path
    def action(self):
        return
class Update():
    def __init__(self, path):
        self.type = 'upd'
        self.path = path
    def action(self):
        return

def get_changes(old, new):
    #init#
    changes = []
    #find changes#
    # get updates
    # get moves
    # get deletes
    # get adds
    #ret#
    return(changes)
def get_conflicts(changes_a, changes_b):
    #init#
    #find conflicts#
    # get update conflicts (w del)
    # get move conflicts (w del)
    # order move and updates to prevent move update conflicts?
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

# Author: Jack Paul Martin
# Start: 10/20/2020, Completion: