def print_lol(the_list, flag=0,num=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item, flag, num+1)
        else:
            if flag:
                for n in range(num):
                    print ('\t',end='')
            print (each_item)
#            else:
#                print (each_item)


movies=['wohucanglong',2000,'zhangmanyu',91,[['zhangziyi','yangziqiong'],['liangchaowei','zhangzhen']]]

print_lol(movies,1,0)

list1=[1,2,3,4,[1,2]]

print_lol(list1)