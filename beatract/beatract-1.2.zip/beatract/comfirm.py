'''
debugging console.
'''

import beat_cqt as bt
import beat_tie as bt2

'''
make_empty_list test code
'''

'''
test_list = bt.make_empty_list([3, 3, 3], [])
print (test_list)
'''

''' 
stage_note test code
'''
'''
test_notes = \
[\
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],\
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],\
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],\
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],\
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],\
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],\
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],\
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
note = bt.stage_note(test_notes)

print "============================note================================="
print("length of time : " + str(len(note)))
for i in range(0, len(note)):
    print(note[i])
print "============================note===========================----======"

link_table, note_list, icoef_table, length_table = bt2.tie_note(note, 2)
print "============================link====================================="
print("length of link_table : " + str(len(link_table)))
for i in range(0, len(link_table)):
    print(link_table[i])
print "============================link====================================="
print "==========================note_list=================================="
print("length of note_list : " + str(len(note_list)))
for i in range(0, len(note_list)):
    print(note_list[i])
print "==========================note_list=================================="
print "=========================icoef_table================================="
print("length of icoef_table : " + str(len(icoef_table)))
for i in range(0, len(icoef_table)):
    print(icoef_table[i])
print "=========================icoef_table================================="
print "========================length_table================================="
print("length of length_table : " + str(len(length_table)))
for i in range(0, len(length_table)):
    print(length_table[i])
print "========================length_table================================="
print("Note Number = " + str(len(note_list)))
'''
dir_name = "/home/sshrik/Workspace/python/Regacy of void/WAV_CUT"

#save_dir = "/home/sshrik/Workspace/python/Music/WAV"
bt.beatract(dir_name=dir_name,file_name=-1, show_graph=-1)
