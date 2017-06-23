

def pileup_acgt(pileup, quality, depth, reference,
                qlimit=53, noend=False, nostart=False):
    '''
    Parse the mpileup format and return the occurrence of each nucleotides
    in the given positions.
    Intended to replace the parse_pileup_seq. Apparently while loops are slower
    then for loops, so this function performs slightly less then
    the old implementation.
    '''
    nucleot_dict = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    strand_dict = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    commas = ('.', ',')
    index = len(pileup)
    n = 0
    q = 0

    accepted_bases = '.ACGT,acgt'
    while n < index:
        forward = False
        char = pileup[n]
        if char in accepted_bases:
            passed = ord(quality[q]) >= qlimit
            if char in commas:
                if char == '.':
                    forward = True
                char = reference
            else:
                if char.isupper():
                    forward = True
                char = char.upper()
            try:
                if pileup[n + 1] == '$':
                    if not noend and passed:
                        nucleot_dict[char] += 1
                        if forward:
                            strand_dict[char] += 1
                    n += 2
                else:
                    if passed:
                        nucleot_dict[char] += 1
                        if forward:
                            strand_dict[char] += 1
                    n += 1
            except IndexError:
                if passed:
                    nucleot_dict[char] += 1
                    if forward:
                        strand_dict[char] += 1
                n += 1
            q += 1
        elif char == '*':
            n += 1
            q += 1
        elif char == '^':
            passed = ord(quality[q]) >= qlimit
            char = pileup[n + 2]
            if char in commas:
                if char == '.':
                    forward = True
                char = reference
            else:
                if char.isupper():
                    forward = True
                char = char.upper()
            if not nostart and passed:
                nucleot_dict[char] += 1
                if forward:
                    strand_dict[char] += 1
            q += 1
            n += 3
        elif char == '-' or char == '+':
            # if char == '-':
            #   comment = 'del'
            # else:
            #   comment = 'ins'
            offset = n + 1
            while True:
                if pileup[offset].isdigit():
                    offset += 1
                else:
                    break
            step = int(pileup[n + 1:offset])
            n += step + len(str(step)) + 1
    nucleot_dict['Z'] = [strand_dict['A'], strand_dict[
        'C'], strand_dict['G'], strand_dict['T']]
    return nucleot_dict


def pileup_split(pileup, index, reference):
    '''
    This generator separate each block of the pileup string. The index
    must be <= the length of the pileup string, otherwise will cause an
    infinite loop. The returning objects are tuples in the format:
       (call, forward, comment)
    where call is the character found in the pileup stripped by the
    annotation denoting start/end of reads or indels. forward is a boolean
    denoting if forward or reverse. The comment field have possible values
    None, "start", "end", "del", "ins". This turned out to be slow compared
    to older implementation...
    '''
    n = 0
    accepted_bases = ['.', ',', 'A', 'C', 'G', 'T', 'a', 'c', 'g', 't']
    while n < index:
        forward = False
        comment = None
        increment = 1
        try:
            char = pileup[n]
            if char in accepted_bases:
                char, forward = check_base(char, reference)
                if pileup[n + 1] == '$':
                    comment = 'end'
                    increment = 2
            elif char == '^':
                char = pileup[n + 2]
                comment = 'start'
                char, forward = check_base(char, reference)
                increment = 3
            elif char == '-' or char == '+':
                if char == '-':
                    comment = 'del'
                else:
                    comment = 'ins'
                offset = n + 1
                while True:
                    if pileup[offset].isdigit():
                        offset += 1
                    else:
                        break
                step = int(pileup[n + 1:offset])
                start = n + len(str(step)) + 1
                stop = start + step
                char = pileup[start:stop]
                increment = step + len(str(step)) + 1
            yield(char, forward, comment)
            n += increment
        except IndexError:
            char, forward = check_base(char, reference)
            yield(char, forward, comment)
            n += 1


def check_base(char, reference):
    forward = False
    if char in '.,':
        if char == '.':
            forward = True
        char = reference
    else:
        if char.isupper():
            forward = True
        char = char.upper()
    return(char, forward)


def pileup_acgt2(pileup, quality, depth, reference,
                 qlimit=53, noend=False, nostart=False):
    '''
    Yet another version of the pileup parser. Used as a template
    for the C implementation
    '''
    characters = 'ACGTacgt$*-+'
    nucleot_list = [0, 0, 0, 0]
    strand_list = [0, 0, 0, 0]
    last_base = None
    index = len(pileup)
    n = 0
    q = 0
    while n < index:
        base = pileup[n]
        if base == '^':
            if not nostart:
                n += 2
                base = pileup[n]
            else:
                n += 3
                q += 1
                continue
        if base == '.':
            base = reference
        elif base == ',':
            base = reference.lower()
        base_index = characters.index(base)
        if base_index < 4:
            if ord(quality[q]) >= qlimit:
                last_base = base_index
                nucleot_list[base_index] += 1
                strand_list[base_index] += 1
            else:
                last_base = None
            n += 1
            q += 1
        elif base_index < 8:
            if ord(quality[q]) >= qlimit:
                last_base = base_index
                nucleot_list[base_index - 4] += 1
            else:
                last_base = None
            n += 1
            q += 1
        elif base_index == 8:
            if not noend:
                pass
            else:
                if last_base:
                    if last_base < 4:
                        nucleot_list[last_base] -= 1
                        strand_list[last_base] -= 1
                    else:
                        nucleot_list[last_base - 4] -= 1
            last_base = None
            n += 1
        elif base_index == 9:
            last_base = None
            n += 1
            q += 1
        elif base_index > 9:
            offset = n + 1
            while True:
                if pileup[offset].isdigit():
                    offset += 1
                else:
                    break
            step = int(pileup[n + 1:offset])
            n = step + offset

    nucleot_dict = {'A': nucleot_list[0], 'C': nucleot_list[
        1], 'G': nucleot_list[2], 'T': nucleot_list[3]}
    nucleot_dict['Z'] = [strand_list[0], strand_list[
        1], strand_list[2], strand_list[3]]
    return nucleot_dict
    # return (nucleot_list, strand_list)


def acgt(pileup, quality, depth, reference, qlimit=53,
         noend=False, nostart=False):
    '''
    Parse the mpileup format and return the occurrence of
    each nucleotides in the given positions.
    '''
    nucleot_dict = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    strand_dict = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    n = 0
    block = {'seq': '', 'length': 0}
    start = False
    del_ins = False
    l_del_ins = ''
    last_base = None
    ins_del_length = 0
    for base in pileup:
        if block['length'] == 0:
            if base == '$':
                if noend:
                    if last_base:
                        nucleot_dict[last_base.upper()] -= 1
                        if last_base.isupper():
                            strand_dict[last_base.upper()] -= 1
                    last_base = None
            elif base == '^':
                start = True
                block['length'] += 1
                block['seq'] = base
            elif base == '+' or base == '-':
                del_ins = True
                block['length'] += 1
                block['seq'] = base
            elif base == '.' or base == ',':
                if ord(quality[n]) >= qlimit:
                    nucleot_dict[reference] += 1
                    if base == '.':
                        strand_dict[reference] += 1
                        last_base = reference
                    else:
                        last_base = reference.lower()
                else:
                    last_base = None
                n += 1
            elif base.upper() in nucleot_dict:
                if ord(quality[n]) >= qlimit:
                    nucleot_dict[base.upper()] += 1
                    if base.isupper():
                        strand_dict[base.upper()] += 1
                    last_base = base
                else:
                    last_base = None
                n += 1
            else:
                n += 1
        else:
            if start:
                block['length'] += 1
                block['seq'] += base
                if block['length'] == 3:
                    if not nostart:
                        if base == '.' or base == ',':
                            if ord(quality[n]) >= qlimit:
                                nucleot_dict[reference] += 1
                                if base == '.':
                                    strand_dict[reference] += 1
                        elif base.upper() in nucleot_dict:
                            if ord(quality[n]) >= qlimit:
                                nucleot_dict[base.upper()] += 1
                                if base.isupper():
                                    strand_dict[base.upper()] += 1
                    block['length'] = 0
                    block['seq'] = ''
                    start = False
                    last_base = None
                    n += 1
            elif del_ins:
                if base.isdigit():
                    l_del_ins += base
                    block['seq'] += base
                    block['length'] += 1
                else:
                    ins_del_length = int(l_del_ins) + 1 + len(l_del_ins)
                    block['seq'] += base
                    block['length'] += 1
                    if block['length'] == ins_del_length:
                        block['length'] = 0
                        block['seq'] = ''
                        l_del_ins = ''
                        # ins_del = False
                        ins_del_length = 0

    nucleot_dict['Z'] = [strand_dict['A'], strand_dict[
        'C'], strand_dict['G'], strand_dict['T']]
    return nucleot_dict
