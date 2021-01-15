# File Name: binding.py
# Description: Binds identical paths together using creation time

#TOD0#

#INIT#
#imports#
import mapping
import resources

#func#
def make_ctimes_unique(mpath):
    """
    checks if there are duplicate creation times within a mapped path and if so increments the ctime by a few nanoseconds
    parameters: none | return: none
    """
    #init#
    def make_ctime_unique(mpath_check):
        while True:
            if mpath.search_dup(mpath_check) != None:
                #get duplicate#
                mpath_dup_pos = mpath.search_dup(mpath_check)
                mpath_dup = mpath.get_mpath(mpath_dup_pos)
                #mod duplicate#
                resources.mod_ctime(mpath_dup.path)
                mpath.update_mpath(mapping.MappedPath(mpath_dup.path), mpath_dup_pos)
                make_ctime_unique(mpath_dup)
            else:
                break
    #make ctime unique for mpath#
    make_ctime_unique(mpath)
    #make ctime unique for sub_mpaths#
    for sub_mpath in mpath.sub_mpaths:
        make_ctimes_unique(sub_mpath)
def bind_paths(path0, path1):
    '''
    binds two identically named paths together using creation time
    parameters: string path0, string path1 | return: none
    '''
    mpath = mapping.MappedPath(path0)
    def bind_recur(mpath, path0, path1):
        #bind mpath#
        path = mpath.path.replace(path0, path1)
        ctime = mpath.ctime
        mtime = mpath.mtime
        resources.set_time(path, ctime, None, mtime)
        #bind sub_mpath#
        for sub_mpath in mpath.sub_mpaths:
            bind_recur(sub_mpath, path0, path1)
    bind_recur(mpath, path0, path1)


# Author: Jack Paul Martin
# Start: 1/1/2021, Completion: 1/14/2021