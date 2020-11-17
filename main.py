# Program Name: mapping
# Description: Maps out a path and records it. Uses created date as a unique id.
# Notes: .mpath files should be for containing string versions of mapped paths

#INIT#
#imports#
import mapping
import changes

#MAIN#
if __name__ == '__main__':
    #testing#
    file = open('testing.txt', 'r')
    contents = file.read().split('\n')
    mpath_old = mapping.MappedPath(contents[0])
    mpath_new = mapping.MappedPath(contents[1])
    changes = changes.get_changes(mpath_old, mpath_new)
    for change in changes:
        print('{} {} {}'.format(change.type, change.name, change.ctime))
    file.close()

# Author: Jack Paul Martin
# Start: 11/16/2020, Completion: