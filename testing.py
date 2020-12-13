# Program Name: testing
# Description: Tests potential code

#INIT#
#imports#
import mapping
import changes
import resources

#funcs#
def disp_test_title(name):
    print('test:', name)
def disp_test_output(output):
    print('output:', output, end='\n\n')

#MAIN#
if __name__ == '__main__':
    print('TRANSFER TESTING\n\n')
    #switches#
    mapping_switch = True
    changes_switch = False
    resources_switch = True
    #tests#
    if mapping_switch:
        print('mapping\n')
        #switches#
        mattributes_switch = False
        mpath_switch = True
        #tests#
        if mattributes_switch:
            pass
        if mpath_switch:
            #switches#
            init_switch = True
            search_switch = True
            modify_switch = True
            output_switch = True
            #tests#
            if init_switch:
                disp_test_title('init path')
                mpath = mapping.MappedPath('testdir')
                mpath_str = mpath.get_mpath_str()
                disp_test_output(mpath_str)
                disp_test_title('init path with exclusions')
                mpath_ex = mapping.MappedPath('testdir', exclusions=[mpath.get_mpath(mpath.search('symb', lambda mapth: mpath.name))])
                mpath_ex_str = mpath_ex.get_mpath_str()
                disp_test_output(mpath_ex_str)
                disp_test_title('init path with different mapped attributes')
                mpath_ma = mapping.MappedPath('testdir', mattribs=[mapping.name_mattrib])
                mpath_ma_str = mpath_ma.get_mpath_str(mattribs=[mapping.name_mattrib])
                disp_test_output(mpath_ma_str)
                disp_test_title('init mpath_str')
                mpath_s = mapping.MappedPath(mpath_str=mpath_str)
                mpath_s_str = mpath_s.get_mpath_str()
                disp_test_output(mpath_s_str)
            if search_switch:
                mpath = mapping.MappedPath('testdir')
                disp_test_title('search for directory')
                mpath_search_dir = mapping.MappedPath(mpath_str='testdir\\symb*symb*0*0*True<>')
                disp_test_output(mpath.search(mpath_search_dir, lambda mpath: mpath.name))
                disp_test_title('search for file')
                mpath_search_file = mapping.MappedPath(mpath_str='testdir\\alpha\\a.txt*a.txt*0*0*False<>')
                disp_test_output(mpath.search(mpath_search_file, lambda mpath: mpath.name))
                disp_test_title('search for nonexistent')
                disp_test_output(mpath.search(mpath_search_dir)) # ctime is 0
                disp_test_title('search_dup for duplicate')
                disp_test_output(mpath.search_dup(mpath_search_dir, lambda mpath: mpath.name))
                disp_test_title('search_dup for nonexistent')
                disp_test_output(mpath.search_dup(mpath_search_dir)) # ctime is 0
            if modify_switch:
                disp_test_title('get')
                disp_test_title('add')
                disp_test_title('remove')
                disp_test_title('move')
                disp_test_title('update')
            if output_switch:
                disp_test_title('get mapped path string') # uhh used for most of the previous tests
                mpath = mapping.MappedPath('testdir')
                mpath_str = mpath.get_mpath_str()
                disp_test_output(mpath_str)
        print('')
    if changes_switch:
        print('changes\n')
        print('')
    if resources_switch:
        print('resources\n')
        print('')

# Author: Jack Paul Martin
# Start: 11/20/2020, Completion: