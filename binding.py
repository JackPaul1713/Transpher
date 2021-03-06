# File Name: binding.py
# Description: Binds identical paths together using creation time




#### INIT ####
#### imports ####
import mapping
import resources


#### func ####
def make_ctimes_unique(mpath, mpath_check=None):
    """
    checks if there are duplicate creation times within a mapped path and if so increments the ctime by a few nanoseconds
    parameters: none | return: none
    """
    if mpath_check == None:
        mpath_check = mpath
    #### init ####
    def make_ctime_unique(mpath, mpath_check):
        while True:
            if mpath.search_dup(mpath_check) != None:  # while duplicate exists
                #### get duplicate ####
                mpath_dup_pos = mpath.search_dup(mpath_check)
                mpath_dup = mpath.get_mpath_at(mpath_dup_pos)
                #### mod duplicate ####
                resources.mod_ctime(mpath_dup.path)  # iterate duplicate ctime by a nanosecond
                mpath.update_mpath_at(mapping.MappedPath(mpath_dup.path), mpath_dup_pos)  # update mpath duplicate
                make_ctime_unique(mpath, mpath_dup)  # check duplicate for duplicates
            else:
                break
    #### make ctime unique ####
    # for mpath
    make_ctime_unique(mpath, mpath_check)
    # for sub_mpaths
    for sub_mpath in mpath_check.sub_mpaths:
        make_ctimes_unique(mpath, sub_mpath)

def bind_paths(mpath, path0, path1):
    '''
    binds the files of two identically named paths together using creation time
    parameters: string path0, string path1 | return: none
    '''
    #### bind ####
    # mpath
    path = mpath.path.replace(path0, path1)  # replaces the path to the files mapped on mpath(path0) with the path to the other files(path1)
    ctime = mpath.ctime
    mtime = mpath.mtime
    resources.set_time(path, ctime, None, mtime)  # sets the times of the other files to the times of files mapped on mpath
    # sub_mpath
    for sub_mpath in mpath.sub_mpaths:
        bind_paths(sub_mpath, path0, path1)




#### MAIN ####
#### testing ####
if __name__ == '__main__':
    #### init ####
    def disp_test_title(name):
        print('test:', name)
    def disp_test_output(output):
        print('output:', output, end='\n\n')
    test_dir0 = 'C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\original'
    test_dir1 = 'C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix'

    #### title ####
    print('binding testing\n')

    #### switches ####
    binding_switch = True

    #### tests ####
    if binding_switch:
        #### init ####
        mpath0 = mapping.MappedPath(test_dir0)
        def make_ctimes_identical(mpath, ctime=None):
            if ctime == None:
                ctime = mpath.ctime
            #### make ctime identical ####
            # mpath
            resources.set_time(mpath.path, ctime)
            # sub_mpath
            for sub_mpath in mpath.sub_mpaths:
                make_ctimes_identical(sub_mpath, ctime)
        mpath0.make_ctimes_identical(mpath0)
        mpath0.refresh()

        disp_test_title('make ctimes unque')
        make_ctimes_unique(mpath0)
        disp_test_output('manually check ctimes at \"testdir\\original\"')

        disp_test_title('bind paths')
        resources.delete_file(test_dir1)
        resources.copy_file(test_dir0, test_dir1)
        bind_paths(mpath0, test_dir0, test_dir1)
        disp_test_output('manually compare ctimes between \"testdir\\original\" and \"testdir\\remix\"')




# Author: Jack Paul Martin
# Start: 1/1/2021, Completion: 1/30/2021