def print_markdown(table, colum_size):

    print('|', end='')
    column = 0
    for subelem in table[0]:
        subelem_str = subelem + (' ' * (colum_size[column] - len(str(subelem))))
        print(' {} |'.format(subelem_str), end='')
        column += 1
    print('')

    print('|', end='')
    column = 0
    for subelem in table[0]:
        print(' ', end='')
        print('-' * (colum_size[column]), end='')
        print(' |', end='')
        column += 1
    print('')

    for elem in table[1:]:
        print('|', end='')
        column = 0

        for subelem in elem[0]:
            print(' {} |'.format(subelem), end='')
            column += 1
        print('')
