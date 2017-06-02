'''
This module act tie notes.
To use this module, just call tie note.
'''
def tie_note(note, threshold):
    '''
    tie notes which related to same instrument.
    Args: r_harmonic, note, far_th
        r_harmonic - harmonic magnitude list.
        note - note_set of harmonics.
            [ at time 0 [1, 2, 3, 4], [6, 7, 8, 9], ... [211, 212, 213, 214, 215],
              at time 1 [2, 3, 4, 5, 6 ,7, 8], [10, 11, 12] ... [212, 213, 214, 215],
              ...
              at time n [2, 3 , 4, 5], [8, 9, 10, 11], ... [211, 212, 213, 214] ]
        far_th - farnote's threshold.
    Return: link_table, note_list, icoef_table, length_table
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time0-1 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...],
              at time1-2 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...],
              at time2-3 [at note0 [[0,a],[0,b] ...] at note1 [[1,a],[1,b] ...] ...],
              ...
              at time fin-1 - fin [...][...]...								   ...]
        note_list - note list which represent instrumental.
            [ note_list 0 [0, 0, 0, ... 0, 1, 0],
              note_list 1 [1, 1, 1, ... 1, 1, 1],
              note_list 2 [2, 1, 2, ... 1, 1, 2],
              ...
              note_list t [t, t-1, t, ... t, t-1, t] ]
        icoef_table - inversed coefficient of notes. means, value`s number is sharing that
            harmonics magnitude value.
            [ coef 0 [1, 1, 1, ... 1, 3, 1],
              coef 1 [1, 2, 1, ... 2, 3, 1],
              coef 2 [1, 2, 1, ... 2, 3, 1],
              ...
              coef t [1, 1, 1, ... 1, 2, 1] ]
        length_table - plused or minused length of note`s location.
            [ coef 0 [4, -2, -1, ... 1, 3, 3],
              coef 1 [-1, -2, -1, ... 2, 3, 1],
              coef 2 [4, 4, 3, ... 2, -3, 1],
              ...
              coef t [2, 1, 0, ... 1, -2, -1] ]
    Raise:
        nothing.
    '''
    #Initialize 4 table.
    link_table = []
    note_list = []
    icoef_table = []
    length_table = []

    # Initialize link_table with empty list.
    link_table.append([])
    for notes in range(0, len(note[0])):
        link_table[0].append([])

    # add first note to note_list.
    # note[0] mean at time 0, note[time]`s notes.
    for notes in range(0, len(note[0])):
        # so append note_list notes which is list "note"`s index.
        note_list.append([])
        note_list[notes].append(notes)
        # ... and append icoef_table note number which is 1.
        icoef_table.append([])
        icoef_table[notes].append(1)
        # ... and also append length_table note number`s empty list([])
        length_table.append([])
    ########################## Stable Marriagement #############################################
    # Stable_marriagement first at time 0 to 1.
    propose_queue = []
    for t1_number in range(0, len(note[0])):
        # Add empty list at index of t1_number.
        propose_queue.append([])
        for t2_number in range(0, len(note[1])):
            propose_queue[t1_number].append(t2_number)

    prefer_queue = []
    for t2_number in range(0, len(note[1])):
        # Add empty list at index of t1_number.
        prefer_queue.append([])
        for t1_number in range(0, len(note[0])):
            prefer_queue[t2_number].append(t1_number)

    # i is index and value as same time.
    # j is value related to i.
    free, i, j = is_free_note(propose_queue, link_table, 0)
    while free:
        # if there exiest some linkable values...

        linked, linked_i = is_linked(link_table, 0, j=propose_queue[i][j])
        # delete relation with propose_i]queue i and j.
        if linked:
            # if already linked...
            if priority(prefer_queue, propose_queue[i][j], i) > priority(prefer_queue, \
            propose_queue[i][j], linked_i):
                # if priority is highter, then delete that link and link with new i.
                delete_link(link_table, 0, linked_i, propose_queue[i][j])
                make_link(link_table, 0, i, propose_queue[i][j])
        else:
            # if not linked, just link.
            make_link(link_table, 0, i, propose_queue[i][j])
        # renew existance of linkable notes and i, j.
        delete_relation(propose_queue, i, propose_queue[i][j])
        free, i, j = is_free_note(propose_queue, link_table, 0)

    ########################## Stable Marriagement #############################################
	# renew 4 tables.

    append_list(note, link_table, note_list, icoef_table, length_table, 0)


    for time in range(1, len(note)-1):
        print "Doing... : " + str(time) + " / " + str(len(note))
		# Stable marriagement -> link notes 1 : 1
        stable_marriagement(note[time], note[time+1], link_table, note_list, length_table, \
        time, threshold)
		# Converge -> link notes n : 1
        coverage(note[time], note[time+1], link_table, note_list, length_table, time, threshold)
		# Seperate -> link notes 1 : n
        seperate(note[time], note[time+1], link_table, note_list, icoef_table,\
		length_table, time, threshold)
		# renew 4 tables
        append_list(note, link_table, note_list, icoef_table, length_table, time)
    del link_table[-1]
    return link_table, note_list, icoef_table, length_table

def stable_marriagement(note_t1, note_t2, link_table, note_list, length_table, time, threshold):
    '''
	link note1 and note2 with smallest value and length_table with threshold.
	Args: note, link_table, note_list, icoef_table, length_table, time, threshold
		note_t1 - time1`s note. [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]]
		note_t2 - time2`s note. [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]]
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        length_table - plused or minused length of note`s location.
            [ coef 0 [4, -2, -1, ... 1, 3, 3],
              coef 1 [-1, -2, -1, ... 2, 3, 1],
              coef 2 [4, 4, 3, ... 2, -3, 1],
              ...
              coef t [2, 1, 0, ... 1, -2, -1] ]
		time - now processing time.
		threshold - threshold to acceptance of distance.
	Return:
	    Add to link_table
	Raise:
	    nothing
	'''
    difference1 = distance(note_t1, note_t2)
    difference2 = distance(note_t2, note_t1)
    propose_queue = make_queue(note_t1, note_t2, length_table, note_list, difference1, threshold, \
    time)
    prefer_queue = make_queue(note_t2, note_t1, length_table, note_list, difference2, threshold, \
    time)

    # i is index and value as same time.
    # j is value related to i.
    free, i, j = is_free_note(propose_queue, link_table, time)

    while free:
        # if there exiest some linkable values...

        linked, linked_i = is_linked(link_table, time, j=propose_queue[i][j])
        # delete relation with propose_queue i and j.
        if linked:
            # if already linked...
            if priority(prefer_queue, propose_queue[i][j], i) > priority(prefer_queue, \
            propose_queue[i][j], linked_i):
                # if priority is highter, then delete that link and link with new i.
                delete_link(link_table, time, linked_i, propose_queue[i][j])
                make_link(link_table, time, i, propose_queue[i][j])
        else:
            # if not linked, just link.
            make_link(link_table, time, i, propose_queue[i][j])
        # renew existance of linkable notes and i, j.
        delete_relation(propose_queue, i, propose_queue[i][j])
        free, i, j = is_free_note(propose_queue, link_table, time)

def make_queue(note_t1, note_t2, length_table, note_list, difference, threshold, time):
    '''
    make propose queue ( prefer list ) for note_t1 to note_t2.
    if note_t1 and note_t2`s length is smaller then before_length + threshold, append it.
    Args: note_t1, note_t2, length_table, difference, threshold
        note_t1, note_t2 - note_t1 is standard note and note_t2 is compared note.
        length_table - length information is saved here.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        difference - length between note_t1 and note_t2.
        threshold - threshold value which calculated at make decision.
        time - t1`s time. t2 mean "time+1".
    Return: prefer_list
        prefer_list - propose queue of note_t1 to note_t2.
        [ 0 th value`s priority is [0, 1, 2],
          1 th value`s priority is [1, 2, 3],
          2 th value`s priority is [2, 3, 4, 5],
          ...
          n th value`s priority is [n-2, n-1, n] ]
    Raise:
        nothing.
    '''
    # Initialize prefer_list with empty list.
    prefer_list = []
    for t1_number in range(0, len(note_t1)):
        # Add empty list at index of t1_number.
        prefer_list.append([])
        for t2_number in range(0, len(note_t2)):
            if get_length(length_table, note_list, time, t1_number) + threshold > \
            difference[t1_number][t2_number]:
                # Add prefer_list to index "t2_number".
                prefer_list[t1_number].append(t2_number)
    return prefer_list

def get_length(length_table, note_list, time, i):
    '''
    get length from length table which is linked with i th note at time "time-1" to "time".
    Args: length_table, time, i
        length_table - length information is saved here.
            [ note 0 [4, -2, -1, ... 1, 3, 3],
              note 1 [-1, -2, -1, ... 2, 3, 1],
              note 2 [4, 4, 3, ... 2, -3, 1],
              ...
              note t [2, 1, 0, ... 1, -2, -1] ]
        time - time which will be used in when`s length.
        i - note`s index which note want to calculate.
    Return: length
        length - length_table
    Raise:
        nothing.
    '''
    # take all value in length_table`s time-1`s i th note`s length.
    for note_number in range(0, len(note_list)):
        if note_list[note_number][time] == i:
            return length_table[note_number][time-2]
    return -1

def is_free_note(propose_queue, link_table, time):
    '''
    Calculate is ther free note in link_table which is at propose_queue.
    Args: propose_queue, link_table
        propose_queue - propose queue of note_t1 to note_t2.
        [ 0 th value`s priority is [0, 1, 2],
          1 th value`s priority is [1, 2, 3],
          2 th value`s priority is [2, 3, 4, 5],
          ...
          n th value`s priority is [n-2, n-1, n] ]
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
    Return: Bool, i, j
        Bool - does linkable notes are exist.
        i - if linkable, t1`s notes index.
        j - if linkable, t2`s notes index.
    Raise:
        nothing.
    '''
    for link_number in range(0, len(link_table[time])):
        # for all link_table[time]`s note index...
        if len(link_table[time][link_number]) == 0:
            # if link_table[time][link_number] is not linked... with len == 0...
            if len(propose_queue[link_number]) != 0:
                # if propose_queue is note empty.
                return True, link_number, 0
    return False, -1, -1

def is_linked(link_table, time, i=-1, j=-1):
    '''
    Check if given i or j is linked in link_table, and return which is linked.
    Args: i, j, link_table
    link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
    Return: linked, linked_i
        linked - if given i or j are linked with some notes, return True, else return False.
        linked_i - if linked == True, return linked note`s list "note"`s index.( value )
            else, return -1
    Raise:
        nothing.
    '''
    if i != -1:
        if len(link_table[time][i]) != 0:
            return True, link_table[time][i][0]
        else:
            return False, -1
    elif j != -1:
        for t1_number in range(0, len(link_table[time])):
            if len(link_table[time][t1_number]) != 0:
                if link_table[time][t1_number][0] == j:
                    return True, t1_number
        return False, -1

def delete_relation(propose_queue, i, j):
    '''
    delete relation at propose_queue[i] which is linked with value "j"
    Args: propose_queue, i, j
    Return:
        nothing.
    Raise:
        nothing.
    '''
    # For all range in propose_queue[i]...
    for delete_number in range(0, len(propose_queue[i])):
        if propose_queue[i][delete_number] == j:
            del propose_queue[i][delete_number]
            break

def priority(prefer_queue, i, j):
    '''
    return j th priority at prefer_queue[i].
    Args: prefer_queue, i, j
    Return: priority
        priority - value which is MAX - index.
            if prioirity is large, index is small.
    Raise:
        nothing.
    '''
    # For all range in prefer_queue[i]...
    for prior in range(0, len(prefer_queue[i])):
        if prefer_queue[i][prior] == j:
            # length - prior is priority.
            return len(prefer_queue[i]) - prior

def delete_link(link_table, time, i, j):
    '''
    delete link at link_table[i]`s linked value "j"
    Args: link_table, i, j
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        i - time "time"`s index.
        j - time "time+"`s note index value.
    Return:
        nothing.
    Raise:
        nothing.
    '''
    # for all value in link_table.
    for delete_number in range(0, len(link_table[time][i])):
        if link_table[time][i][delete_number] == j:
            # delete which value is j in i th note`s link.
            del link_table[time][i][delete_number]

def make_link(link_table, time, i, j):
    '''
    make link at link_table[i]`s link value "j"
    Args: link_table, i, j
    Return:
        nothing.
    Raise:
        nothing.
    '''
    # Make link with at time "time", i`th notes to j.
    link_table[time][i].append(j)

def coverage(note_t1, note_t2, link_table, note_list, length_table, time, threshold):
    '''
    converge which is not linked and have acceptable link notes.
    Args: note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold
    Return:
        nothing.
    Raise:
        nothing.
    '''
    difference = distance(note_t1, note_t2)
    for note_number1 in range(0, len(note_t1)):
        linked, _ = is_linked(link_table, time, i=note_number1)
        if not linked:
            # if not linked note_number1
            note_number2 = get_smallest_index(note_number1, difference)
            if note_number2 != -1:
                if difference[note_number1][note_number2] < get_length(length_table, \
                note_list, time, note_number1) + threshold:
                    make_link(link_table, time, note_number1, note_number2)

def get_smallest_index(note_number1, difference):
    '''
    get smallest index of difference[note_number1]`s list.
    '''
    smallest_index = -1
    for note_number2 in range(0, len(difference[note_number1])):
        if difference[note_number1][note_number2] < difference[note_number1][smallest_index]:
            smallest_index = note_number2
    return smallest_index

def acceptable_note(length_table, note_list, difference, i, j, time, threshold):
    '''
    Check acceptablility with difference[i][j] is in length acceptable at time.
    Args: difference, i, j, time, threshold
    Return: bool
        bool - if acceptable, return True, else return False.
    Raise:
        nothing.
    '''
    if get_length(length_table, note_list, time, i) + threshold > difference[i][j]:
        return True
    else:
        return False

def seperate(note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold):
    '''
    Seperate if coef is lareger then 2 and have acceptable_note in range of length.
    Args: note_t1, note_t2, link_table, note_list, icoef_table, length_table, time, threshold
    Return:
        nothing.
    Raise:
        nothing.
    '''
    difference = distance(note_t1, note_t2)
    for t1_number in range(0, len(note_t1)):
        icoef = calc_icoef(icoef_table, note_list, time, t1_number)
        for t2_number in range(0, len(note_t2)):
            if icoef > 1:
                if acceptable_note(length_table, note_list, difference, \
                t1_number, t2_number, time, threshold):
                    make_link(link_table, time, t1_number, t2_number)
            else:
                break

def calc_icoef(icoef_table, note_list, time, note_list_number):
    '''
    calculate icoef with time0 to time1`s note_list`s value is note_list_number.
    stage location of note_list`s value, then return that location`s icoef_table
    Args: icoef_table, note_list, note_list_number.
        icoef_table - inversed coefficient of notes. means, value`s number is sharing that
            harmonics magnitude value.
            [ coef 0 [1, 1, 1, ... 1, 3, 1],
              coef 1 [1, 2, 1, ... 2, 3, 1],
              coef 2 [1, 2, 1, ... 2, 3, 1],
              ...
              coef t [1, 1, 1, ... 1, 2, 1] ]
        note_list - note list which represent instrumental.
            [ note_list 0 [0, 0, 0, ... 0, 1, 0],
              note_list 1 [1, 1, 1, ... 1, 1, 1],
              note_list 2 [2, 1, 2, ... 1, 1, 2],
              ...
              note_list t [t, t-1, t, ... t, t-1, t] ]
        note_list_number - index of which want to know.
    Return: int
        int - calculation note_list`s nl icoef value.
    Raise:
        nothing
    '''
    # Return icoef value of table which note number is "note_list_number" and at time.
    for note_number in range(0, len(note_list)):
        if note_list[note_number][time] == note_list_number:
            return icoef_table[note_number][time-1]

def append_list(note, link_table, note_list, icoef_table, length_table, time):
    '''
	append list from note and link_table, to note_list... etc.
	Args: note, link_table, note_list, icoef_table, length_table, time
	    note - note values of which frequency ( or real note ) are included.
			[ at time 0 [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]],
              at time 1 [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]],
              at time 2 [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]],
			  ...
              at time t [[1, 2, 3, 4], [10, 11, 12, 13, 14, ...] ... [210, 211, 212, 213]] ]
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        note_list - note list which represent instrumental.
            [ note_list 0 [0, 0, 0, ... 0, 1, 0],
              note_list 1 [1, 1, 1, ... 1, 1, 1],
              note_list 2 [2, 1, 2, ... 1, 1, 2],
              ...
              note_list n [t, t-1, t, ... t, t-1, t] ]
        icoef_table - inversed coefficient of notes. means, value`s number is sharing that
            harmonics magnitude value.
            [ note 0 [1, 1, 1, ... 1, 3, 1],
              note 1 [1, 2, 1, ... 2, 3, 1],
              note 2 [1, 2, 1, ... 2, 3, 1],
              ...
              note n [1, 1, 1, ... 1, 2, 1] ]
        length_table - plused or minused length of note`s location.
            [ note 0 [4, -2, -1, ... 1, 3, 3],
              note 1 [-1, -2, -1, ... 2, 3, 1],
              note 2 [4, 4, 3, ... 2, -3, 1],
              ...
              note n [2, 1, 0, ... 1, -2, -1] ]
	Return:
	    nothing
	Raise:
	    nothing
	'''
    # Append note_list with link_table and append icoef & length too.
    append_note(link_table, note_list, icoef_table, length_table, time)
    # Append iceof_table with note_list.
    append_icoef(note_list, icoef_table)
    # Append length_table at note.
    append_length(note, note_list, length_table, time)
    #print "length : " + str(length_table)
    #print "note : " + str(note_list)
    # Append link_table empty...
    # This mean Initailize which is not linked.
    link_table.append([])
    for _ in range(0, len(note[time+1])):
        link_table[time+1].append([])

def copy_to(dest_list, dest, src_list):
    '''
    copy src_list to dest_list[dest] with insert method.
    Args: dest_list, dest, src_list
    Return:
        nothing.
    Raises:
        nothing.
    '''
    # Add empty list at dest_list[dest].
    dest_list.insert(dest, src_list)

def make_list(list_contents, times, trail=-2):
    '''
    make list with [list_contents, list_contents, ... ] for times`s time.
    if trail is not -2, then add trail to list and return it.
    Args: list_contets, times, trail
        list_contents - repeat value.
        times - length of default size of list.
        trial - if not -2, append it to return_list.
    Return: made_list
        made_list - [list_contents, list_contents, ... ] or
                  - [list_contents, list_contents, ... , trail]
    Raises:
        nothing.
    '''
    made_list = []
    for _ in range(0, times):
        made_list.append(list_contents)
    if trail != -2:
        made_list.append(trail)
    return made_list

def copy_list(_list, trail=-2):
    '''
    copy one dimension list "one_D_list" and return it.
    and if trail is not -1, then append it to end of list.
    Args: one_D_list, trail
        one_D_list - will be copied list.
        trail - if not -2, then append it at the end.
    Return: copy_list
        copy_list - copied list with input.
    Raise:
        nothing.
    '''
    # Initialize copy_list.
    copied_list = []
    # For all value in range of one_D_list...
    for list_number in range(0, len(_list)):
        # Copy it.
        copied_list.append(_list[list_number])
    if trail != -2:
        copied_list.append(trail)
    return copy_list

def append_icoef(note_list, icoef_list):
    '''
    append icoef_list with note_list and link_table.
    Args: link_table, note_list, icoef_list
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        note_list - note list which represent instrumental.
            [ note_list 0 [0, 0, 0, ... 0, 1, 0],
              note_list 1 [1, 1, 1, ... 1, 1, 1],
              note_list 2 [2, 1, 2, ... 1, 1, 2],
              ...
              note_list t [t, t-1, t, ... t, t-1, t] ]
        icoef_table - inversed coefficient of notes. means, value`s number is sharing that
            harmonics magnitude value.
            [ coef 0 [1, 1, 1, ... 1, 3, 1],
              coef 1 [1, 2, 1, ... 2, 3, 1],
              coef 2 [1, 2, 1, ... 2, 3, 1],
              ...
              coef t [1, 1, 1, ... 1, 2, 1] ]
    Return:
        nothing.
    Raises:
        nothing.
    '''
    # Coef number is started from 1.
    same_number = 1
    coef_number = 0
    recorded_number = 0

    while coef_number < len(note_list)-1:
        if note_list[coef_number][-1] == -1:
            for _ in range(0, same_number):
                icoef_list[recorded_number].append(0)
                recorded_number += 1
                same_number = 1
        elif note_list[coef_number] == note_list[coef_number+1]:
            same_number += 1
        else:
            for _ in range(0, same_number):
                icoef_list[recorded_number].append(same_number)
                recorded_number += 1
                same_number = 1
        coef_number += 1
    for _ in range(recorded_number, len(note_list)):
        icoef_list[recorded_number].append(same_number)

def append_length(note, note_list, length_table, time):
    '''
    append length_table with note_list and link_table.
    Args: link_table, note_list, length_table
    Return:
        nothing.
    Raises:
        nothing.
    '''
    # for all range of note_list...
    for note_number in range(0, len(note_list)):
        # if note[time][i] and note[time+1][j] are linked, length is difference between two notes.
        if len(note_list[note_number]) == time + 1:
            note_list[note_number].append(note_list[note_number][-1])
            # For Error Correction... This case must not occur but occured sometimes...
            # Specific Debugging is needed.
        if note_list[note_number][time + 1] == -1:
            length_table[note_number].append(0)
        else:
            length = mid(note[time][note_list[note_number][time]]) \
            - mid(note[time+1][note_list[note_number][time+1]])
            length_table[note_number].append(length)

def append_note(link_table, note_list, icoef_table, length_table, time):
    '''
    append note_list with link_table.
    if add some instrumental, then copy it.
    Args: link_table, note_list, icoef_table, length_table, time
        link_table - tied notes which is related to some other note.
            bundle of notes are other represent of instrument.
            [ at time 0[[0], [0], [0], ... , [0], [1], [0]],
              at time 1[[1], [1, 2], [1], ... , [1], [1, 2], [2]],
              at time 2[[2], [1, 2], [2], ... , [2], [1, 2], [2]],
              ...
              at time t[[t], [t], [t], ... , [t], [t-1, t], [t]] ]
        note_list - note list which represent instrumental.
            [ note_list 0 [0, 0, 0, ... 0, 1, 0],
              note_list 1 [1, 1, 1, ... 1, 1, 1],
              note_list 2 [2, 1, 2, ... 1, 1, 2],
              ...
              note_list t [t, t-1, t, ... t, t-1, t] ]
        icoef_table - inversed coefficient of notes. means, value`s number is sharing that
            harmonics magnitude value.
            [ coef 0 [1, 1, 1, ... 1, 3, 1],
              coef 1 [1, 2, 1, ... 2, 3, 1],
              coef 2 [1, 2, 1, ... 2, 3, 1],
              ...
              coef t [1, 1, 1, ... 1, 2, 1] ]
        length_table - plused or minused length of note`s location.
            [ coef 0 [4, -2, -1, ... 1, 3, 3],
              coef 1 [-1, -2, -1, ... 2, 3, 1],
              coef 2 [4, 4, 3, ... 2, -3, 1],
              ...
              coef t [2, 1, 0, ... 1, -2, -1] ]
        time - at timing "time".
    Return:
        nothing.
    Raise:
        nothing.
    '''
    before_index = 0
    for index in range(0, len(link_table[time])):
        absent, start_note, finish_note = absent_note(link_table, index, before_index, time)
        if absent:
            before_index = index
            for insert_number in range(start_note, finish_note):
                copy_to(note_list, insert_number, make_list(-1, time + 1, insert_number + 1))
                copy_to(icoef_table, insert_number, make_list(0, time + 1))
                copy_to(length_table, insert_number, make_list(0, time - 1))
        if len(link_table[time][index]) == 0:
            add_notelist(note_list, time, index, -1)
        elif len(link_table[time][index]) == 1:
            before_index = index
            add_notelist(note_list, time, index, link_table[time][index][0])
        else:
            before_index = index
            for copy_number in range(0, len(note_list)):
                if capiable(note_list, time, index, copy_number):
                    basic = copy_list(note_list[copy_number])
                    # Delete basic lists.
                    del note_list[copy_number]

                    for note_num in range(0, len(link_table[time][index])):
                        copy_to(note_list, copy_number, copy_list(basic, \
                        trail=link_table[time][index][note_num]))
                        copy_to(icoef_table, copy_number, copy_list(icoef_table[copy_number]))
                        copy_to(length_table, copy_number, copy_list(length_table[copy_number]))
                    # Delete basic lists.
                    del icoef_table[copy_number]
                    del length_table[copy_number]
        for finished_note in range(0, len(note_list)):
            if len(note_list[finished_note]) == time + 1 and note_list[finished_note][-1] == -1:
                note_list[finished_note].append(-1)

def absent_note(link_table, index, before_index, time):
    '''
    Check if there exist absetn notes.
    Args: link_table, inde, before_index, time
    Return: bool, start_note, finish_note
        bool - if there absent_note, True. Else False.
        start_note, finish_note - start and finish note number. if bool is False, -1, -1
    Raise:
        nothing
    '''
    if len(link_table[time][index]) != 0 and index != before_index:
        if len(link_table[time][before_index]) != 0:
            # if input link_table[time][index] is not null...
            if link_table[time][index][0] - link_table[time][before_index][-1] > 1:
                # if difference of link_table`s are larger then 2...
                return True, link_table[time][before_index][-1], link_table[time][index][0]-1
    return False, -1, -1

def add_notelist(note_list, time, index, contents):
    '''
    add to note_list[i][time] contents if before value is index.
    Args: note_list, time, index, contents
        note_list - note list which represent instrumental.
            [ note_list 0 [0, 0, 0, ... 0, 1, 0],
              note_list 1 [1, 1, 1, ... 1, 1, 1],
              note_list 2 [2, 1, 2, ... 1, 1, 2],
              ...
              note_list t [t, t-1, t, ... t, t-1, t] ]
        time - at time "time".
        index - before index values.
        contents - which value to append.
    Return:
        nothing.
    Raise:
        nothing.
    '''
    for note_number in range(0, len(note_list)):
        if note_list[note_number][time] == index:
            # if at time value is index, append contents.
            note_list[note_number].append(contents)

def capiable(note_list, time, index, copy_number):
    '''
    Does note_list[copy_number][time] is copiable?
    Which mean same as index and length is time - 1.
    Args: note_list, time, index, copy_number
    Return: bool
        bool - if capiable, return True, else retur False.
    Raise:
        nothing.
    '''
    if note_list[copy_number][time] == index:
        # if value is index.
        if len(note_list[copy_number]) == time:
            # if length is time...
            return True
    return False

def mid(note):
    '''
    Input note set and return average of some vector or return a remarkable values.
    Args : note
        note - list of vector which represent some note.
    Returns : average
    average - average of vector or remarkable values.
    Raises :
        nothing
    '''
    average = 0
    for i in range(0, len(note)):
        average += note[i]
    # just return average of note`s contents.
    return average / len(note)

def distance(note_t1, note_t2):
    '''
    compare note1 and note2 then return some distance of 2 notes.
    Args : time1, time2
        time1, time2 - notes list of at time1 and time2
    Return : difference
        difference - list of all distance of mid(time1[i]) and mid(time2[j])
    Raises :
        nothing
    '''
    difference = []
    # initialize return value "difference" with empty list
    for note_number1 in range(0, len(note_t1)):
        difference.append([])
        # add empty list to difference to show i`th time1 notes and all time2 notes.
        for note_number2 in range(0, len(note_t2)):
            # add difference of time1[i] and time2[j]
            # just uclidean distance of two note`s average.
            difference[note_number1].append(abs(mid(note_t1[note_number1]) - \
            mid(note_t2[note_number2])))
    return difference

def weightract(r_harmonics, note, note_list, icoef_table):
    '''
    Extract beat with some weights.
    Periodic instrument( note link ) will have low weights.
    Large sound will have high weights.
    Args: r_harmonics, note, link_table, note_list, icoef_table
    Return: beat_weights
    Raise:
         nothing
    '''
    # Calculate periodicalilty and add it to periodic list.
    # if have small portion of music, and periodically wave, periodic will be decrease.
    periodic = []
    for note_number in range(0, len(note_list)):
        periodic.append(get_periodic(note_list[note_number]))

    weights = []
    for note_number in range(0, len(note_list)):
        weights.append([])
        for time in range(0, len(note_list[note_number])):
            # Weights are weights value / coef * periodicality.
            weights[note_number].append(\
            get_weights(r_harmonics, note, note_list[note_number][time], \
            icoef_table[note_number][time], time))
            #get_weights(r_harmonics, note, note_list[note_number][sequence],\
            #icoef_table[note_number][sequence], sequence) * periodic[note_number])
    real_beat = []
    # Add all beat weights.
    for note_number2 in range(0, len(weights[0])):
        _sum = 0
        for note_number1 in range(0, len(weights)):
            _sum += weights[note_number1][note_number2]
        real_beat.append(_sum)

    return real_beat

def get_periodic(note_t1):
    '''
    get note_t1`s periodic score.
    if note_t1 have many notes, score up.
    if note_t1 have periodical wave, score down.
    Args: note_t1
    Return: periodic_score
        periodic_score - score if note_t1 have many periodical wave or decompose many.
    Raise:
        nothing.
    '''
    # Calculate Portions.
    empty_number = 0
    for note_number in range(0, len(note_t1)):
        if note_t1[note_number] == -1:
            empty_number += 1
    # empty_number / len(note_t1) is portion score.

    return empty_number / len(note_t1)

def get_weights(r_harmonics, note, note_value, icoef_value, time):
    '''
    get weights of note`s with note_value and icoef_value.
    if icoef_value is large, weights are small.
    if value`s magnitude is large, weights are bigger.
    Args: note, note_list, note_value, icoef_value
    Return: weights
        weights - value which magnitude is big and which is sharing magnitude.
    Raise:
        nothing.
    '''
    magnitude_sum = 0
    # Add all magnitudes for at all value in note[time][note_value]
    if len(note[time]) != 0:
        for note_index in range(0, len(note[time][note_value])):
            magnitude_sum += abs(r_harmonics[note[time][note_value][note_index]][time])
            # abs(r_harmonics) are magnitudes.
            # weights = magnitude_sum / (icoef_value+1)
    return magnitude_sum

def average_note_list(weight_t1):
    '''
    calculate weight_t1`s average magnitude.
    '''

def note_length(note_t1):
    '''
    '''

def length_normalize(link_table, note_list, icoef_table, length_table, time):
    '''
    Normalize 4 list with time domain.
    For all notes number, we check if len(list) is correct time and if larger or smaller, append or delete
        apropriate notes / icoef / length
    Args: link_table, note_list, icoef_table, length_table
        link_table -
        note_list -
        icoef_table -
        length_table -
    Return:
        nothing.
    Raises:
        nohting.
    '''

def icoef_recalculation(note_list, icoef_table):
    '''
    Recalculation icoef_table with calculated note_list.
    Confirm icoef can mean note_list`s sharing note`s information.
    Args: note_list, icoef_table
        note_list -
        icoef_table -
    Return:
        nothing.
    Raises:
        nohting.
    '''
