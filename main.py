# Program Name: Transfer
# File Name: main
# Description: gets changes between two directories and merges, records, and applies them if necessary
# Notes: requires a file

#TOD0#
#check#
# make ctime unique
# using old mpath check for changes in the mpath
# hard_merge to changes0 or 1:, record changes in the loc
# check for changes in the opposite, changes1 or 0:
# if^ soft_merge changes0 and 1:
#apply#
# if^ make changes on the active machine, removing files from server(one drive in this case) that are no longer needed
# *all of this scheduled to run on logon and every so often after

#INIT#
#imports#
import os
import load
import mapping
import changes
import binding

#MAIN#
if __name__ == '__main__':
    #func#
    def transfer(name, path):
        tfile = load.TransFile(name, path)
        tfile.upload()
        local_m = -1
        exterior_m = -1
        if os.environ['COMPUTERNAME'] == tfile.machine[0]:
            local_m = 0
            exterior_m = 1
        elif os.environ['COMPUTERNAME'] == tfile.machine[1]:
            local_m = 1
            exterior_m = 0

        #check#
        print('check')
        mpath = mapping.MappedPath(tfile.path[local_m], exclusions=tfile.path[local_m])
        binding.make_ctimes_unique(mpath)  # make sure any new files have unique ctimes
        new_changes = changes.get_changes(tfile.mpath[local_m], mpath)  # old_mpath, new_mpath
        if not changes.is_empty(tfile.changes[local_m]):
            tfile.changes[local_m] = changes.hard_merge_changes(tfile.changes[local_m], new_changes)  # old_changes, new_changes
            changes.make_trans_changes(tfile.changes[local_m], tfile.tpath, tfile.mpath[local_m])
        elif not changes.is_empty(new_changes):
            tfile.changes[local_m] = new_changes
            changes.make_trans_changes(tfile.changes[local_m], tfile.tpath, tfile.mpath[local_m])

        #apply#
        print('apply')
        if not changes.is_empty(tfile.changes[local_m]):
            tfile.changes[local_m], staged_changes = changes.soft_merge_changes(tfile.changes[local_m], tfile.changes[exterior_m])
            changes.make_changes(staged_changes, tfile.tpath, tfile.mpath[local_m])
            tfile.changes[exterior_m] = {'add':[], 'del':[], 'mov':[], 'upd':[]}

    #title#
    print('TRANSFER')

    #get tfiles#
    path = os.getcwd()
    names = []
    for file in os.scandir(path):
        name = file.name
        if name.split('.')[-1] == 'tf':
            names.append(name)

    #transpher#
    for name in names:
        transfer(name, path)

# Author: Jack Paul Martin
# Start: 1/14/2021, Completion: 1/30/2021