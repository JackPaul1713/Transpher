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
        if new:
            self.path0 = ''
            self.path1 = ''
            self.tpath = path
            self.mpath0 = mapping.MappedPath(mpath_str='a*a*0*0*False<>')
            self.mpath1 = mapping.MappedPath(mpath_str='a*a*0*0*False<>')
            self.changes0 = {'add':[], 'del':[], 'mov':[], 'upd':[]}
            self.changes1 = {'add':[], 'del':[], 'mov':[], 'upd':[]}
    def upload(self):
        #read#
        file = open(self.tfile_path, 'r')
        lines = file.readlines()
        file.close()
        #load#
        self.path0 = lines[0].replace('path0: ', '')[0:-1]
        self.path1 = lines[1].replace('path1: ', '')[0:-1]
        self.tpath = lines[2].replace('tpath: ', '')[0:-1]
        self.mpath0 = mapping.MappedPath(mpath_str=lines[3].replace('mpath0: ', '')[0:-1])
        self.mpath1 = mapping.MappedPath(mpath_str=lines[4].replace('mpath1: ', '')[0:-1])
        self.changes0 = changes.upload_changes(lines[5].replace('changes0: ', '')[0:-1])
        self.changes1 = changes.upload_changes(lines[6].replace('changes1: ', '')[0:-1])
    def download(self):
            #download#
            path0 = 'path0: ' + self.path0 + '\n'
            path1 = 'path1: ' + self.path1 + '\n'
            tpath = 'tpath: ' + self.tpath + '\n'
            mpath0 = 'mpath0: ' + self.mpath0.get_mpath_str() + '\n'
            mpath1 = 'mpath1: ' + self.mpath1.get_mpath_str() + '\n'
            changes0 = 'changes0: ' + changes.download_changes(self.changes0) + '\n'
            changes1 = 'changes1: ' + changes.download_changes(self.changes1) + '\n'
            #write#
            lines = [path0, path1, tpath, mpath0, mpath1, changes0, changes1]
            file = open(self.path, 'w')
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
        tfile.path0 = 'testdir\\original'
        tfile.path1 = 'testdir\\remix'
        tfile.tpath = 'D:\\Transfer'
        tfile.mpath0 = mapping.MappedPath(tfile.path0)
        tfile.mpath1 = mapping.MappedPath(tfile.path1)
        disp_test_output(tfile)

        disp_test_title('download')
        tfile.download()
        disp_test_output('check for \"transfer.tf\"')

        disp_test_title('upload')
        tfile.upload()
        print(tfile.changes0)
        disp_test_output(tfile)

    if cleanup_switch:
        resources.delete_file('transfer.tf')

# Author: Jack Paul Martin
# Start: 1/30/2021, Completion: 1/30/2021