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
import os
import requests

#MAIN#
if __name__ == '__main__':
    #func#
    def download_files(path):
        files = ['main.py', 'load.py', 'mapping.py', 'changes.py', 'binding.py', 'resources.py']
        for file in files:
            content = requests.get('https://raw.github.com/JackPaul1713/Transpher/main/' + file).content
            file = open(path + '\\' + file, 'wb')
            file.write(content)
            file.close()
    def schedule_task():
        # os.system('SCHTASKS /CREATE...') # fuck this
        pass

    #title#
    print('TRANSFER SETUP')

    #input#
    print("1. machine0")
    print("2. machine1")
    selection = input('Input: ')
    print('')
    if selection == '1':
        #title#
        print('SETUP PART 1')

        #input#
        print("enter the location on the server for transfering files")
        tpath = input('Input: ')
        print("enter the first path")
        path0 = input('Input: ')
        print("enter the second path")
        path1 = input('Input: ')
        print("enter exclusions, 's' to stop")
        exclusions = []
        while True:
            exclusion = input('Input: ')
            if exclusion != 's':
                exclusions.append(exclusion)
            else:
                break
        exclusions0 = []
        exclusions1 = []
        for exclusion in exclusions:
            exclusions0.append(path0 + exclusion)
            exclusions1.append(path1 + exclusion)

        #setup tfile#
        tfile = load.Transfile(tpath, new=True)
        tfile.machine[0] = os.environ['COMPUTERNAME']
        tfile.path[0] = path0
        tfile.path[1] = path1
        tfile.exclusions[0] = exclusions0
        tfile.exclusions[1] = exclusions1
        tfile.mpath[0] = mapping.MappedPath(tfile.path[0], exclusions=tfile.exclusions[0])

        #setup machine0#
        binding.make_ctimes_unique(tfile.mpath[0])
        tfile.mpath[0].refresh()

        #download#
        tfile.download()
        download_files(tpath)

        #task#
        print('schedule a task to run main.py')

    if selection == '2':
        #title#
        print('SETUP PART 2')

        #input#
        print("enter the location on the server for transfering files (same location as part 1)")
        tpath = input('Input: ')

        #setup tfile#
        tfile = load.Transfile(tpath).upload()
        tfile.local_m[1] = os.environ['COMPUTERNAME']

        #setup machine1#
        binding.bind_paths(tfile.mpath[0], tfile.path[0], tfile.path[1])
        tfile.mpath[1] = mapping.MappedPath(tfile.path[1], exclusions=tfile.exclusions[1])

        #download#
        tfile.download()
        download_files(tpath)

        #task#
        print('schedule a task to run main.py')

# Author: Jack Paul Martin
# Start: 1/14/2021, Completion: 1/30/2021