# File Name: changes
# Description: can find changes to a mpath using a saved version of the mpath before changes.

#TOD0#
# add clear_trans_action() to changes objects: ADD, DEL, MOV, UPD
# clear_trans_action() at the end of action()
# clear_trans_action() when removed in merge functions

#INIT#
#imports#
import time
import resources

#objects#
class Add():
    """
    addition change in a file path
    parameters: string name, float ctime
    """
    def __init__(self, name, ctime, mtime, dst_name, dst_ctime):
        self.type = 'add'
        self.name = name
        self.ctime = ctime
        self.mtime = mtime
        self.dst_name = dst_name
        self.dst_ctime = dst_ctime
    def action(self, src, mpath):
        loc = mpath.search_attrib(self.dst_ctime, lambda mpath: mpath.ctime)
        path = mpath.get_mpath(loc).path + '\\' + self.name
        src = src + '\\' + str(self.ctime) + str(self.mtime) + self.name
        resources.rename_file(src, path)
        resources.set_time(path, ctime=self.ctime, mtime=self.mtime)
    def trans_action(self, dst, mpath):
        loc = mpath.search_attrib(self.ctime, lambda mpath: mpath.ctime)
        path = mpath.get_mpath(loc).path
        dst = dst + '\\' + str(self.ctime) + str(self.mtime) + self.name
        resources.copy_file(path, dst)
    def display(self):
        print('add {} {} to {} {}'.format(self.name, self.ctime, self.dst_name, self.dst_ctime))
class Delete():
    """
    delete change in a file path
    parameters: string name, float ctime
    """
    def __init__(self, name, ctime):
        self.type = 'del'
        self.name = name
        self.ctime = ctime
    def action(self, mpath):
        loc = mpath.search_attrib(self.ctime, lambda mpath: mpath.ctime)
        path = mpath.get_mpath(loc).path
        resources.delete_file(path)
    def display(self):
        print('delete {} {}'.format(self.name, self.ctime))
class Move():
    """
    move change in a file path
    parameters: string name, float ctime, string new_path
    """
    def __init__(self, name, ctime, mtime, dst_name, dst_ctime):
        self.type = 'mov'
        self.name = name
        self.ctime = ctime
        self.mtime = mtime
        self.dst_name = dst_name
        self.dst_ctime = dst_ctime
    def action(self, mpath):
        loc0 = mpath.search_attrib(self.ctime, lambda mpath: mpath.ctime)
        path0 = mpath.get_mpath(loc0).path
        loc1 = mpath.search_attrib(self.dst_ctime, lambda mpath: mpath.ctime)
        path1 = mpath.get_mpath(loc1).path + '\\' + self.name
        resources.rename_file(path0, path1)
        resources.set_time(path1, ctime=self.ctime, mtime=self.mtime)
    def display(self):
        print('move {} {} to {} {}'.format(self.name, self.ctime, self.dst_name, self.dst_ctime))
class Update():
    """
    update change in a file path
    parameters: string name, float ctime
    """
    def __init__(self, name, ctime, mtime):
        self.type = 'upd'
        self.name = name
        self.ctime = ctime
        self.mtime = mtime
    def action(self, src, mpath):
        loc = mpath.search_attrib(self.ctime, lambda mpath: mpath.ctime)
        path = mpath.get_mpath(loc).path
        src = src + '\\' + str(self.ctime) + str(self.mtime) + self.name
        resources.delete_file(path)
        resources.rename_file(src, path)
        resources.set_time(path, ctime=self.ctime, mtime=self.mtime)
    def trans_action(self, dst, mpath):
        loc = mpath.search_attrib(self.ctime, lambda mpath: mpath.ctime)
        path = mpath.get_mpath(loc).path
        dst = dst + '\\' + str(self.ctime) + str(self.mtime) + self.name
        resources.copy_file(path, dst)
    def display(self):
        print('update {} {} {}'.format(self.name, self.ctime, time.ctime(self.mtime)))

#funcs#
def get_super_path(path):
    '''
    gets the path to the file that contains the file the input path leads to
    parameters: string path | return: string super_path
    '''
    path_list = path.split('\\')
    path_list = path_list[0:-1]
    super_path = ''
    for file in path_list:
        super_path += '\\'
    super_path += '\b'
    return(super_path)
def get_super_mpath(mpath, sub_mpath):
    '''
    gets the mapped path the sub_mpath is contained in from a master mpath
    parameters: MappedPath mpath, MappedPath sub_mpath | return: MappedPath super_mpath
    '''
    pos = mpath.search(sub_mpath)[0:-1]
    super_mpath = mpath.get_mpath(pos)
    return(super_mpath)

def sort_changes(changes):
    '''
    sorts changes to the order they should be made in
    parameters: list changes | return: dict changes
    '''
    sorted_changes = {'add':[], 'mov':[], 'upd':[], 'del':[]}
    for change in changes:
        if change.type == 'add':
            sorted_changes['add'].append(change)
        elif change.type == 'mov':
            sorted_changes['mov'].append(change)
        elif change.type == 'upd':
            sorted_changes['upd'].append(change)
        elif change.type == 'del':
            sorted_changes['del'].append(change)
    return(sorted_changes)
def get_changes(old_mpath, new_mpath):
    """
    gets the changes between two similar mapped paths
    parameters: MappedPath mpath_old, MappedPath mpath_new | return: mixed[] changes
    """
    #init#
    def get_pos_changes(mpath_n, old_mpath, new_mpath):
        #init#
        changes = [] # ADD bc you could mov something to something added but not move something that does not exist yet, MOV UPD DEL bc the order of the rest doesn't matter
        super_mpath_n = get_super_mpath(new_mpath, mpath_n)
        #get changes mpath#
        #add#
        if old_mpath.search(mpath_n) == None:
            name = mpath_n.name
            ctime = mpath_n.ctime
            mtime = mpath_n.mtime
            dst_name = super_mpath_n.name
            dst_ctime = super_mpath_n.ctime
            change = Add(name, ctime, mtime, dst_name, dst_ctime)
            changes.append(change)
        else:
            #move#
            if get_super_mpath(old_mpath, old_mpath.get_mpath(old_mpath.search(mpath_n))).ctime != super_mpath_n.ctime:
                name = mpath_n.name
                ctime = mpath_n.ctime
                mtime = mpath_n.mtime
                dst_name = super_mpath_n.name
                dst_ctime = super_mpath_n.ctime
                change = Move(name, ctime, mtime, dst_name, dst_ctime)
                changes.append(change)
            #update#
            if old_mpath.get_mpath(old_mpath.search(mpath_n)).mtime != mpath_n.mtime:
                if not mpath_n.dir:
                    change = Update(mpath_n.name, mpath_n.ctime, mpath_n.mtime)
                    changes.append(change)
        #get changes sub_mpaths#
        for sub_mpath_n in mpath_n.sub_mpaths:
            changes = changes + get_pos_changes(sub_mpath_n, old_mpath, new_mpath)
        return(changes)
    def get_neg_changes(mpath_o, old_mpath, new_mpath):
        #init#
        changes = []
        #get changes mpath#
        #del#
        if new_mpath.search(mpath_o) == None:
            name = mpath_o.name
            ctime = mpath_o.ctime
            change = Delete(name, ctime)
            changes.append(change)
        #get changes sub_mpaths#
        for sub_mpath_o in mpath_o.sub_mpaths:
            changes = changes + get_neg_changes(sub_mpath_o, old_mpath, new_mpath)
        return(changes)
    changes = get_pos_changes(new_mpath, old_mpath, new_mpath) + get_neg_changes(old_mpath, old_mpath, new_mpath)
    changes = sort_changes(changes)
    return(changes)

def hard_merge_changes(old_changes, new_changes):
    """
    merges old changes with newer ones within the same file system
    parameters: dict old_changes, dict new_changes | return: dict merged_changes
    """
    #init#
    def compare(old_type, new_type, old_changes, new_changes, old_func=lambda c: c.ctime, new_func=lambda c: c.ctime):
        for nc in range(len(new_changes[new_type])):
            new_change = new_changes[new_type][nc]
            for oc in range(len(old_changes[old_type])):
                old_change = old_changes[old_type][oc]
                if new_func(new_change) == old_func(old_change):
                    old_changes[old_type].pop(oc)
        return(old_changes)

    #add conflicts#
    # possible conflicts: add(new) vs del(old)
    old_changes = compare('add', 'del', old_changes, new_changes)
    old_changes = compare('add', 'del', old_changes, new_changes, old_func=lambda c: c.dst_ctime)

    #mov conflicts#
    # possible conflicts: mov(new) vs mov(old), del(old)
    old_changes = compare('mov', 'mov', old_changes, new_changes)
    old_changes = compare('mov', 'del', old_changes, new_changes)
    old_changes = compare('mov', 'del', old_changes, new_changes, old_func=lambda c: c.dst_ctime)

    #upd conflicts#
    # possible conflicts: upd(new) vs upd, del(old)
    old_changes = compare('upd', 'upd', old_changes, new_changes)
    old_changes = compare('upd', 'del', old_changes, new_changes)

    #del conflicts#
    # possible conflicts: del(new) vs everything(old)
    old_changes = compare('del', 'add', old_changes, new_changes)
    old_changes = compare('del', 'add', old_changes, new_changes, new_func=lambda c: c.dst_ctime)
    old_changes = compare('del', 'mov', old_changes, new_changes)
    old_changes = compare('del', 'mov', old_changes, new_changes, new_func=lambda c: c.dst_ctime)
    old_changes = compare('del', 'upd', old_changes, new_changes)
    old_changes = compare('del', 'del', old_changes, new_changes)

    #merge#
    merged_changes = {}
    merged_changes['add'] = new_changes['add'] + old_changes['add']
    merged_changes['mov'] = new_changes['mov'] + old_changes['mov']
    merged_changes['upd'] = new_changes['upd'] + old_changes['upd']
    merged_changes['del'] = new_changes['del'] + old_changes['del']
    #ret#
    return(merged_changes)
def soft_merge_changes(local_changes, exterior_changes):  # Look into what causes conflicts more... order and type may matter
    """
    merges changes between two similar(identical before changes) file systems, and prompts the user to resolve conflicts
    parameters: dict local_changes, dict new_changes | return: dict local_changes, staged_changes
    """
    #init#
    def resolve_conflict(local_change, exterior_change):
        print('CONFLICT: {} vs {}'.format(local_change.type, exterior_change.type))
        print('select the change to be applied')
        print('1(local). ', end='')
        local_change.display()
        print('2(exterior). ', end='')
        exterior_change.display()
        while True:
            selection = input('input: ')
            if selection == '1':
                return('local')
            elif selection == '2':
                return('exterior')
            else:
                print('invalid input, try again')
    def compare(local_type, exterior_type, local_changes, exterior_changes, local_func=lambda c: c.ctime, exterior_func=lambda c: c.ctime):
        for lc in range(len(local_changes[local_type])):
            local_change = local_changes[local_type][lc]
            for ec in range(len(exterior_changes[exterior_type])):
                exterior_change = exterior_changes[exterior_type][ec]
                #conflicts#
                if local_func(local_change) == exterior_func(exterior_change):
                    resolution = resolve_conflict(local_change, exterior_change)
                    if resolution == 'local':
                        exterior_changes[exterior_type].pop(ec)
                    elif resolution == 'exterior':
                        local_changes[local_type].pop(lc)
        #ret#
        return(local_changes, exterior_changes)

    #add conflicts#
    # possible conflicts: add vs add, del
    local_changes, exterior_changes = compare('add', 'add', local_changes, exterior_changes)
    local_changes, exterior_changes = compare('add', 'del', local_changes, exterior_changes)
    local_changes, exterior_changes = compare('add', 'del', local_changes, exterior_changes, local_func=lambda c: c.dst_ctime)

    #move conflicts#
    # possible conflicts: mov vs mov, del # also special case: mov and mov_dst vs mov and mov_dst
    for l in range(len(local_changes['mov'])):
        local_change = local_changes['mov'][l]
        for e in range(len(exterior_changes['mov'])):
            exterior_change = exterior_changes['mov'][e]
            if local_change.ctime == exterior_change.ctime and local_change.dst_ctime == exterior_change.dst_ctime:
                local_changes['mov'].pop(l)
                exterior_changes['mov'].pop(e)
    local_changes, exterior_changes = compare('mov', 'mov', local_changes, exterior_changes)
    local_changes, exterior_changes = compare('mov', 'del', local_changes, exterior_changes)
    local_changes, exterior_changes = compare('mov', 'del', local_changes, exterior_changes, local_func=lambda c: c.dst_ctime)

    #update conflicts#
    # possible conflicts: upd vs upd, del
    local_changes, exterior_changes = compare('upd', 'upd', local_changes, exterior_changes)
    local_changes, exterior_changes = compare('upd', 'del', local_changes, exterior_changes)

    #delete conflicts#
    # possible conflicts: del vs add, add_dst, mov, mov_dst, upd # also special case: del vs del
    for l in range(len(local_changes['del'])):
        local_change = local_changes['del'][l]
        for e in range(len(exterior_changes['del'])):
            exterior_change = exterior_changes['del'][e]
            if local_change.ctime == exterior_change.ctime:
                local_changes['del'].pop(l)
                exterior_changes['del'].pop(e)
    local_changes, exterior_changes = compare('del', 'add', local_changes, exterior_changes)
    local_changes, exterior_changes = compare('del', 'add', local_changes, exterior_changes, exterior_func=lambda c: c.dst_ctime)
    local_changes, exterior_changes = compare('del', 'mov', local_changes, exterior_changes)
    local_changes, exterior_changes = compare('del', 'mov', local_changes, exterior_changes, exterior_func=lambda c: c.dst_ctime)
    local_changes, exterior_changes = compare('del', 'upd', local_changes, exterior_changes)

    #ret#
    staged_changes = exterior_changes
    return(local_changes, staged_changes)

def make_trans_changes(changes, dst, mpath):
    """
    moves necessary files to a accessible location so that the changes can be made
    parameters: dict changes, str dst, MappedPath mpath | return: None
    """
    #adds#
    for change in changes['add']:
        change.trans_action(dst, mpath)
    #upd#
    for change in changes['upd']:
        change.trans_action(dst, mpath)
def make_changes(changes, src, mpath):
    """
    makes changes to a file system
    parameters: dict changes, str src, MappedPath mpath | return: None
    """
    for change in changes['add']:
        change.action(src, mpath)
    for change in changes['mov']:
        change.action(mpath)
    for change in changes['upd']:
        change.action(src, mpath)
    for change in changes['del']:
        change.action(mpath)

def upload_changes(changes_str):
    """
    expands changes from a string
    parameters: str changes_str | return: dict changes
    """
    changes = {'add':[], 'mov':[], 'upd':[], 'del':[]}
    types = changes_str.split('|')
    adds = types[0].split(':')
    moves = types[1].split(':')
    updates = types[2].split(':')
    deletes = types[3].split(':')
    if adds == ['']:
        adds = []
    if moves == ['']:
        moves = []
    if updates == ['']:
        updates = []
    if deletes == ['']:
        deletes = []
    for add in adds:
        elements = add.split('*')
        change = Add(elements[0], float(elements[1]), float(elements[2]), elements[3], float(elements[4]))
        changes['add'].append(change)
    for move in moves:
        elements = move.split('*')
        change = Move(elements[0], float(elements[1]), float(elements[2]), elements[3], float(elements[4]))
        changes['mov'].append(change)
    for update in updates:
        elements = update.split('*')
        change = Update(elements[0], float(elements[1]), float(elements[2]))
        changes['upd'].append(change)
    for delete in deletes:
        elements = delete.split('*')
        change = Delete(elements[0], float(elements[1]))
        changes['del'].append(change)
    return(changes)
def download_changes(changes):
    """
    records changes to a string
    parameters: dict changes | return: str changes_str
    """
    #init#
    changes_str = '' # ':' divides elements, '/' divides changes, '|' divides types
    add = False
    move = False
    update = False
    delete = False
    #add#
    for change in changes['add']:
        change_str = '{}*{}*{}*{}*{}'.format(change.name, change.ctime, change.mtime, change.dst_name, change.dst_ctime)
        if add:
            changes_str = changes_str + ':' + change_str
        else:
            changes_str = changes_str + change_str
            add = True
    #mov#
    changes_str += '|'
    for change in changes['mov']:
        change_str = '{}*{}*{}*{}*{}'.format(change.name, change.ctime, change.mtime, change.dst_name, change.dst_ctime)
        if move:
            changes_str = changes_str + ':' + change_str
        else:
            changes_str = changes_str + change_str
            move = True
    #upd#
    changes_str += '|'
    for change in changes['upd']:
        change_str = '{}*{}*{}'.format(change.name, change.ctime, change.mtime)
        if update:
            changes_str = changes_str + ':' + change_str
        else:
            changes_str = changes_str + change_str
            update = True
    #del#
    changes_str += '|'
    for change in changes['del']:
        change_str = '{}*{}'.format(change.name, change.ctime)
        if delete:
            changes_str = changes_str + ':' + change_str
        else:
            changes_str = changes_str + change_str
            delete = True
    #ret#
    return(changes_str)

def is_empty(changes):
    is_empty = 1
    if len(changes['add']) > 0:
        is_empty = 0
    if len(changes['mov']) > 0:
        is_empty = 0
    if len(changes['upd']) > 0:
        is_empty = 0
    if len(changes['del']) > 0:
        is_empty = 0
    return(is_empty)

#var#
empty_changes = {'add':[], 'del':[], 'mov':[], 'upd':[]}

#MAIN#
#testing#
if __name__ == '__main__':
    #init#
    import mapping
    import binding
    def disp_test_title(name):
        print('test:', name)
    def disp_test_output(output):
        print('output: {}'.format(output), end='\n\n')
    test_dir0 = 'C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\original'
    test_dir1 = 'C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix'

    #title#
    print('changes testing\n')

    #switches#
    get_changes_switch = False
    merge_changes_switch = False
    make_changes_switch = False
    output_switch = True

    #tests#
    if get_changes_switch:
        #init#
        mpath0 = mapping.MappedPath(test_dir0)
        binding.make_ctimes_unique(mpath0)
        resources.delete_file(test_dir1)
        resources.copy_file(test_dir0, test_dir1)
        binding.bind_paths(test_dir0, test_dir1)
        resources.make_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\symb\\$.txt') # add
        resources.rename_file('/testdir/remix/numb/positive/a.txt',
                  'C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\numb\\positive\\a.txt') # move
        resources.write_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\symb\\!.txt', 'no') # update
        resources.delete_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\alpha\\d.txt') # del
        mpath1 = mapping.MappedPath(test_dir1)

        #tests#
        disp_test_title('get changes')
        changes = get_changes(mpath0, mpath1)
        print('output: ')
        for type in changes.values():
            for change in type:
                change.display()
        print()
    if merge_changes_switch:
        #init#
        def test_hard_merge(title, change0, change1):
            print(title)
            changes0 = sort_changes([change0])
            changes1 = sort_changes([change1])
            output = hard_merge_changes(changes1, changes0)
            print('output: {}'.format(output))
        def test_soft_merge(title, change0, change1):
            print(title)
            changes0 = sort_changes([change0])
            changes1 = sort_changes([change1])
            output = soft_merge_changes(changes0, changes1)
            print('output: {}'.format(output))

        ctime0 = 0.0
        ctime1 = 1.1

        name = 'file'
        dst_name = 'dst_file'
        mtime = 2.2

        add = Add(name, ctime0, mtime, dst_name, ctime1)
        add_dst = Add(name, ctime1, mtime, dst_name, ctime0)
        move0 = Move(name, ctime0, mtime, dst_name, ctime1)
        move1 = Move(name, ctime0, mtime, dst_name, ctime0)
        move_dst = Move(name, ctime1, mtime, dst_name, ctime0)
        update = Update(name, ctime0, mtime)
        delete = Delete(name, ctime0)

        #tests#
        disp_test_title('hard merge')
        test_hard_merge('add vs delete', add, delete)
        test_hard_merge('add_dst vs delete', add_dst, delete)
        test_hard_merge('move vs move', move0, move0)
        test_hard_merge('move vs delete', move0, delete)
        test_hard_merge('move_dst vs delete', move_dst, delete)
        test_hard_merge('update vs update', update, update)
        test_hard_merge('update vs delete', update, delete)
        test_hard_merge('delete vs add', delete, add)
        test_hard_merge('delete vs add_dst', delete, add_dst)
        test_hard_merge('delete vs move', delete, move0)
        test_hard_merge('delete vs move_dst', delete, move_dst)
        test_hard_merge('delete vs update', delete, update)
        test_hard_merge('delete vs delete', delete, delete)
        print('')

        disp_test_title('hard merge')
        test_soft_merge('add vs add', add, add)
        test_soft_merge('add vs delete', add, delete)
        test_soft_merge('add_dst vs delete', add_dst, delete)
        test_soft_merge('move vs move (special case)', move0, move0)
        test_soft_merge('move vs move', move0, move1)
        test_soft_merge('move vs delete', move0, delete)
        test_soft_merge('move_dst vs delete', move_dst, delete)
        test_soft_merge('update vs update', update, update)
        test_soft_merge('update vs delete', update, delete)
        test_soft_merge('delete vs add', delete, add)
        test_soft_merge('delete vs add_dst', delete, add_dst)
        test_soft_merge('delete vs move', delete, move0)
        test_soft_merge('delete vs move_dst', delete, move_dst)
        test_soft_merge('delete vs update', delete, update)
        test_soft_merge('delete vs delete (special case)', delete, delete)

        disp_test_title('soft_merge')
    if make_changes_switch:
        #init#
        resources.make_dir('temp')

        mpath0 = mapping.MappedPath(test_dir0)
        binding.make_ctimes_unique(mpath0)
        resources.delete_file(test_dir1)
        resources.copy_file(test_dir0, test_dir1)
        binding.bind_paths(test_dir0, test_dir1)

        #test#
        disp_test_title('make changes, add')
        resources.delete_file(test_dir1 + '\\alpha\\d.txt')
        mpath1 = mapping.MappedPath(test_dir1)
        changes = get_changes(mpath1, mpath0)  # old, new
        print(changes)
        make_trans_changes(changes, 'temp', mpath0)
        make_changes(changes, 'temp', mpath1)
        disp_test_output('check for \"testdir\\remix\\d.txt\"')

        disp_test_title('make changes, move')
        resources.rename_file('/testdir/remix/numb/positive/a.txt',
                              'C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\numb\\positive\\a.txt')
        mpath1 = mapping.MappedPath(test_dir1)
        changes = get_changes(mpath1, mpath0)  # old, new
        print(changes)
        make_trans_changes(changes, 'temp', mpath0)
        make_changes(changes, 'temp', mpath1)
        disp_test_output('check for \"testdir\\remix\\alpha\\a.txt\"')

        disp_test_title('make changes, update')
        resources.write_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\symb\\!.txt', 'no')
        mpath1 = mapping.MappedPath(test_dir1)
        changes = get_changes(mpath1, mpath0)  # old, new
        print(changes)
        make_trans_changes(changes, 'temp', mpath0)
        make_changes(changes, 'temp', mpath1)
        disp_test_output('check \"testdir\\remix\\symb\\!.txt\" for text')

        disp_test_title('make changes, delete')
        resources.make_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\symb\\$.txt')
        mpath1 = mapping.MappedPath(test_dir1)
        changes = get_changes(mpath1, mpath0)  # old, new
        print(changes)
        make_trans_changes(changes, 'temp', mpath0)
        make_changes(changes, 'temp', mpath1)
        disp_test_output('check \"testdir\\remix\\symb\" for \"$.txt\"')

        #reset#
        resources.delete_file('temp')
    if output_switch:
        #init#
        mpath0 = mapping.MappedPath(test_dir0)
        binding.make_ctimes_unique(mpath0)
        resources.delete_file(test_dir1)
        resources.copy_file(test_dir0, test_dir1)
        binding.bind_paths(mpath0, test_dir0, test_dir1)
        resources.make_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\symb\\$.txt')  # add
        resources.rename_file('/testdir/remix/numb/positive/a.txt',
                              'C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\numb\\positive\\a.txt')  # move
        resources.write_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\symb\\!.txt',
                             'no')  # update
        resources.delete_file('C:\\Users\\JackPaul\\PycharmProjects\\Transpher\\testdir\\remix\\alpha\\d.txt')  # del
        mpath1 = mapping.MappedPath(test_dir1)

        #tests#
        disp_test_title('download changes')
        changes = get_changes(mpath0, mpath1)
        changes_str = download_changes(changes)
        disp_test_output(changes_str)

        disp_test_title('upload changes')
        print(changes)
        changes = upload_changes(changes_str)
        disp_test_output(changes)

# Author: Jack Paul Martin
# Start: 10/20/2020, Completion: 1/30/2021