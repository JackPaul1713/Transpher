# Program Name: Transfer
# File Name: load
# Description: stores info for Transpher in a file
# Notes: requires a file

#INIT#
#imports#
import mapping
import changes

#objects#
class Transfile:
    def __init__(self, path, new=False, name='transfer.tf'):
        self.tfile_path = path + name
        self.tpath = 0
        self.machine = [0, 0]
        self.path = [0, 0]
        self.exclusions = [0, 0]
        self.mpath = [0, 0]
        self.changes = [0, 0]
        if new:
            self.tpath = path
            self.machine[0] = ''
            self.machine[1] = ''
            self.path[0] = ''
            self.path[1] = ''
            self.exclusions[0] = []
            self.exclusions[1] = []
            self.mpath[0] = mapping.MappedPath(mpath_str='a*a*0*0*False<>')
            self.mpath[1] = mapping.MappedPath(mpath_str='a*a*0*0*False<>')
            self.changes[0] = {'add':[], 'del':[], 'mov':[], 'upd':[]}
            self.changes[1] = {'add':[], 'del':[], 'mov':[], 'upd':[]}
    def upload(self):
        #read#
        file = open(self.tfile_path, 'r')
        lines = file.readlines()
        file.close()
        #load#
        self.tpath = lines[0].replace('tpath: ', '')[0:-1]
        self.machine[0] = lines[1].replace('machine0: ', '')[0:-1]
        self.machine[1] = lines[2].replace('machine1: ', '')[0:-1]
        self.path[0] = lines[3].replace('path0: ', '')[0:-1]
        self.path[1] = lines[4].replace('path1: ', '')[0:-1]
        self.exclusions[0] = lines[5].replace('exclusions0: ', '')[0:-1]
        self.exclusions[1] = lines[6].replace('exclusions1: ', '')[0:-1]
        if self.exclusions[0] != '':
            self.exclusions[0] = self.exclusions[0].split('|')
            self.exclusions[1] = self.exclusions[1].split('|')
        else:
            self.exclusions[0] = []
            self.exclusions[1] = []
        self.mpath[0] = mapping.MappedPath(mpath_str=lines[7].replace('mpath0: ', '')[0:-1])
        self.mpath[1] = mapping.MappedPath(mpath_str=lines[8].replace('mpath1: ', '')[0:-1])
        self.changes[0] = changes.upload_changes(lines[9].replace('changes0: ', '')[0:-1])
        self.changes[1] = changes.upload_changes(lines[10].replace('changes1: ', '')[0:-1])
    def download(self):
            #download#
            tpath = 'tpath: ' + self.tpath + '\n'
            machine0 = 'machine0: ' + self.machine[0] + '\n'
            machine1 = 'machine1: ' + self.machine[1] + '\n'
            path0 = 'path0: ' + self.path[0] + '\n'
            path1 = 'path1: ' + self.path[1] + '\n'
            exclusions0 = 'exclusions0: '
            exclusions1 = 'exclusions1: '
            for e in range(len(self.exclusions[0])):
                exclusions0 = exclusions0 + self.exclusions[0][e] + '|'
                exclusions1 = exclusions1 + self.exclusions[1][e] + '|'
            exclusions0 = exclusions0[0:-1] + '\n'
            exclusions1 = exclusions1[0:-1] + '\n'
            mpath0 = 'mpath0: ' + self.mpath[0].get_mpath_str() + '\n'
            mpath1 = 'mpath1: ' + self.mpath[1].get_mpath_str() + '\n'
            changes0 = 'changes0: ' + changes.download_changes(self.changes[0]) + '\n'
            changes1 = 'changes1: ' + changes.download_changes(self.changes[1]) + '\n'
            #write#
            lines = [tpath, machine0, machine1, path0, path1, exclusions0, exclusions1, mpath0, mpath1, changes0, changes1]
            file = open(self.tfile_path, 'w')
            file.writelines(lines)
            file.close()

#MAIN#
#testing#
if __name__ == '__main__':
    #init#
    import resources
    def disp_test_title(name):
        print('test:', name)
    def disp_test_output(output):
        print('output: {}'.format(output), end='\n\n')

    #title#
    print('transfile testing\n')

    #switches#
    transfile_switch = True
    cleanup_switch = True

    #tests#
    if transfile_switch:
        disp_test_title('make new')
        tfile = Transfile('', new=True)
        tfile.tpath = 'D:\\Transfer'
        tfile.path[0] = 'testdir\\original'
        tfile.path[1] = 'testdir\\remix'
        tfile.exclusions[0].append('testdir\\original\\symb')
        tfile.exclusions[1].append('testdir\\remix\\symb')
        tfile.mpath[0] = mapping.MappedPath(tfile.path[0], exclusions=tfile.exclusions[0])
        tfile.mpath[1] = mapping.MappedPath(tfile.path[1], exclusions=tfile.exclusions[1])
        print('tpath: {}'.format(tfile.tpath))
        print('path0: {}'.format(tfile.path[0]))
        print('path1: {}'.format(tfile.path[1]))
        print('exclusions0: {}'.format(tfile.exclusions[0]))
        print('exclusions1: {}'.format(tfile.exclusions[1]))
        print('mpath0: {}'.format(tfile.mpath[0].get_mpath_str()))
        print('mpath1: {}'.format(tfile.mpath[1].get_mpath_str()))
        print('changes0: {}'.format(tfile.changes[0]))
        print('changes1: {}'.format(tfile.changes[1]))
        disp_test_output(tfile)

        disp_test_title('download')
        tfile.download()
        disp_test_output('check for \"transfer.tf\"')

        disp_test_title('upload')
        tfile.upload()
        print(tfile.changes[0])
        disp_test_output(tfile)

    if cleanup_switch:
        resources.delete_file('transfer.tf')

# Author: Jack Paul Martin
# Start: 1/30/2021, Completion: 1/30/2021