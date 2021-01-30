# Program Name: Transfer
# File Name: settup
# Description: sets up two directories to be used for Transfer
# Notes: requires a file

#TOD0#
# needs file with two identical(sub_names) paths
# two parts pick 0, 1 (each on different machines)
# settup file with mpath0 and 1:, changes0 and 1:, merged_changes0 and 1:
# 0: make ctimes unique for path0, map out path, record mpath in file   (?) download python files and schedule tasks 0
# 1: bind ctimes for path1, map out path, record mpath in file   (?) download python files and schedule tasks 1

#INIT#
#imports#
import load
import mapping
import binding

#MAIN#
if __name__ == '__main__':
    print('TRANSFER SETUP')
    print("1. machine0")
    print("2. machine1")
    selection = input('Input: ')
    print('')
    if selection == '1':
        #input#
        print('SETUP PART 1')
        print("enter the location on the server for transfering files")
        tpath = input('Input: ')
        print("enter the first path")
        path0 = input('Input: ')
        print("enter the second path")
        path1 = input('Input: ')
        #setup tfile#
        tfile = load.Transfile(tpath, new=True)
        tfile.path0 = path0
        tfile.path1 = path1
        tfile.mpath0 = mapping.MappedPath(path0)
        binding.make_ctimes_unique(tfile.mpath0)
        tfile.mpath0.refresh()
        tfile.download()
    if selection == '2':
        #input#
        print('SETUP PART 2')
        print("enter the location on the server for transfering files (same location as part 1)")
        tpath = input('Input: ')
        #setup tfile#
        tfile = load.Transfile(tpath).upload()
        binding.bind_paths(tfile.mpath0, tfile.path0, tfile.path1)
        tfile.mpath1 = mapping.MappedPath(tfile.path1)
        tfile.download()

# Author: Jack Paul Martin
# Start: 1/14/2021, Completion: