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
        #get host computer#
        if os.environ['COMPUTERNAME'] == tfile.machine[0]:
            local_m = 0
            exterior_m = 1
        elif os.environ['COMPUTERNAME'] == tfile.machine[1]:
            local_m = 1
            exterior_m = 0

        #CHECK# - get any changes on the local machine
        #var#
        old_mpath = tfile.mpath[local_m]
        new_mpath = mapping.MappedPath(tfile.path[local_m], exclusions=tfile.path[local_m])  # get new new_mpath to compare to the old one
        old_changes = tfile.changes(local_m)
        new_changes = changes.empty_changes
        merged_changes = changes.empty_changes

        #check#
        binding.make_ctimes_unique(new_mpath)  # make sure any new files have unique ctimes
        new_changes = changes.get_changes(tfile.mpath[local_m], new_mpath)  # compare old_mpath to new_mpath
        tfile.mpath[local_m] = new_mpath

        if not changes.is_empty(old_changes): # if there are old changes
            merged_changes = changes.hard_merge_changes(tfile.changes[local_m], new_changes)  # merge old_changes with new_changes
            tfile.changes[local_m] = merged_changes  # add merged changes
            changes.make_trans_changes(tfile.changes[local_m], tfile.tpath, tfile.mpath[local_m])  # make transitional changes so changes can be made
        elif not changes.is_empty(new_changes): # if there are no old changes but there are new ones
            tfile.changes[local_m] = new_changes # add changes
            changes.make_trans_changes(tfile.changes[local_m], tfile.tpath, tfile.mpath[local_m])  # make transitional changes so changes can be made

        #display#
        print('CHECK')
        print('old new_mpath: ' + new_mpath.get_mpath_str())
        print('new new_mpath: ' + old_mpath.get_mpath_str())
        print('')
        print('old changes(local):')
        for change in old_changes:
            change.display()
        print('')
        print('new changes(local):')
        for change in new_changes:
            change.display()
        print('')
        if not changes.is_empty(old_changes):  # if there are old changes
            print('merged changes(local):')
            for change in new_changes:
                change.display()
            print('')

        #APPLY# - merge any changes on the local machine with changes on the exterior machine and apply merged exterior changes(staged changes)
        #var#
        local_changes = tfile.changes(local_m)
        exterior_changes = tfile.changes(exterior_m)
        merged_local_changes = changes.empty_changes
        staged_changes = changes.empty_changes

        #apply#
        if (not changes.is_empty(local_changes)) and (not changes.is_empty(exterior_changes)):  # if there are changes on the local and exterior machine
            merged_local_changes, staged_changes = changes.soft_merge_changes(local_changes, exterior_changes)  # merge local and exterior changes
            tfile.changes[local_m] = merged_local_changes
            changes.make_changes(staged_changes, tfile.tpath, tfile.mpath[local_m])  # apply staged changes
            tfile.changes[exterior_m] = changes.empty_changes  # clear exterior changes (applied)

        #display#
        print('APPLY')
        print('local changes:')
        for change in local_changes:
            change.display()
        print('')
        print('exterior changes:')
        for change in exterior_changes:
            change.display()
        print('')
        if (not changes.is_empty(local_changes)) and (
        not changes.is_empty(exterior_changes)):  # if there are changes on the local and exterior machine
            print('merged local changes:')
            for change in merged_local_changes:
                change.display()
            print('')
            print('staged changes:')
            for change in staged_changes:
                change.display()
            print('')
            print('staged changes applied')
        else:
            print('no staged changes')

        #DOWNLOAD#
        tfile.download()

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