# -*- coding: utf_8 -*-

import sys, argparse, bisect

class Converter:
    def __init__(self, habrahabr_html = False):
        self.to_html_called_inside_to_html_outer_pos_list = []
        self.newline_chars = []
        self.habrahabr_html = habrahabr_html

    def instr_pos_to_line_column(self, pos):
        pos += sum(self.to_html_called_inside_to_html_outer_pos_list)
        line = bisect.bisect(self.newline_chars, pos)
        return line + 1, pos - (self.newline_chars[line-1] if line > 0 else -1)

    def to_html(self, instr, outfile = None, ohd = 0, *, outer_pos = 0):
        self.to_html_called_inside_to_html_outer_pos_list.append(outer_pos)
        class FileToStringProxy:
            def __init__(self):
                self.result = [] # this should be faster than using regular string
            def write(self, s):
                self.result.append(s)
        if outfile == None:
            outfile = FileToStringProxy()

        # Формируем массив позиций всех символов новой строки для определения номера строки по номеру символа
        if len(self.to_html_called_inside_to_html_outer_pos_list) == 1:
            self.newline_chars = []
            i = 0
            while i < len(instr):
                if instr[i] == "\r" or (instr[i] == "\n" and instr[i-1:i] != "\r"):
                    self.newline_chars.append(i)
                i += 1

        def exit_with_error(msg, pos):
            print(msg + ' at line {} column {}'.format(*self.instr_pos_to_line_column(pos)))
            sys.exit(-1)

        i = 0
        def next_char(offset = 1):
            return instr[i + offset] if i + offset < len(instr) else "\0"

        def i_next_str(str): # i_ — if_/is_
            #return i + len(str) <= len(instr) and instr[i:i+len(str)] == str
            return instr[i+1:i+1+len(str)] == str # first check is not necessarily in Python

        def prev_char(offset = 1):
            return instr[i - offset] if i - offset >= 0 else "\0"

        def html_escape(str):
            return str.replace('&', '&amp;').replace('<', '&lt;')
        def html_escapeq(str):
            return str.replace('&', '&amp;').replace('"', '&quot;')

        writepos = 0
        def write_to_pos(pos, npos):
            nonlocal writepos
            outfile.write(html_escape(instr[writepos:pos]))
            writepos = npos

        def write_to_i(add_str, skip_chars = 1):
            write_to_pos(i, i+skip_chars)
            outfile.write(add_str)

        def find_ending_pair_quote(i): # ищет окончание ‘строки’
            assert(instr[i] == "‘") # ’
            nesting_level = 0
            while True:
                if i == len(instr):
                    exit_with_error('Unpaired left single quotation mark', startqpos)
                ch = instr[i]
                if ch == "‘":
                    nesting_level += 1
                elif ch == "’":
                    nesting_level -= 1
                    if nesting_level == 0:
                        return i
                i += 1

        unique_links = {}
        nonunique_links = {}
        link = ''

        def write_http_link(startpos, endpos, q_offset = 1, text = None):
            nonlocal i, link
            # Ищем окончание ссылки
            nesting_level = 0
            i += 2
            while True:
                if i == len(instr):
                    exit_with_error('Unended link', endpos+1)
                ch = instr[i]
                if ch == "[":
                    nesting_level += 1
                elif ch == "]":
                    if nesting_level == 0:
                        break
                    nesting_level -= 1
                elif ch == " ":
                    break
                i += 1

            link = html_escapeq(instr[endpos+1+q_offset:i])
            tag = '<a href="' + link + '"'

            # Ищем альтернативный текст при такой записи: ссылка[http://... ‘альтернативный текст’]
            if instr[i] == " ":
                tag += ' title="'
                if next_char() == "‘": # ’[[
                    endqpos2 = find_ending_pair_quote(i+1)
                    assert(instr[endqpos2+1] == ']')
                    tag += html_escapeq(instr[i+2:endqpos2])
                    i = endqpos2 + 1
                else:
                    endb = instr.find(']', i)
                    tag += instr[i+1:endb]
                    i = endb
                tag += '"'
            if next_char() == '[' and (next_char(2).isdigit() or next_char(2) == '-'):
                j = i + 3
                while j < len(instr):
                    if instr[j] == ']':
                        if next_char(2) == '-':
                            nonunique_links[int(instr[i+3:j])] = link
                        else:
                            assert(int(instr[i+2:j]) not in unique_links)
                            unique_links[int(instr[i+2:j])] = link
                        i = j
                        break
                    if not instr[j].isdigit():
                        break
                    j += 1
            if text == None:
                write_to_pos(startpos, i+1)
                text = html_escape(instr[startpos+q_offset:endpos])
            outfile.write(tag + '>' + (text if text != '' else link) + '</a>')

        def find_ending_sq_bracket(str, i):
            assert(str[i] == "[") # ]
            nesting_level = 0
            while True:
                ch = str[i]
                if ch == "[":
                    nesting_level += 1
                elif ch == "]":
                    nesting_level -= 1
                    if nesting_level == 0:
                        return i
                i += 1
                if i == len(str):
                    raise 'Unpaired `[`' # ]

        def remove_comments(s):
            while True:
                j = s.find("[[[") # ]]]
                if j == -1: break
                s = s[0:j] + s[find_ending_sq_bracket(s, j)+1:]
            return s

        def write_note(startpos, endpos, q_offset = 1):
            nonlocal i
            i += q_offset
            endqpos2 = find_ending_pair_quote(i+1) # [[‘
            if instr[endqpos2+1] != ']':
                exit_with_error("Bracket ] should follow ’", endqpos2+1)
            write_to_pos(startpos, endqpos2+2)
            outfile.write('<abbr title="'
                + html_escapeq(remove_comments(instr[i+2:endqpos2])) + '">'
                + html_escape(remove_comments(instr[startpos+q_offset:endpos])) + '</abbr>')
            i = endqpos2 + 1

        endi = 0
        def numbered_link(offset = 1):
            if next_char(offset).isdigit() or (next_char(offset) == '-' and next_char(offset+1).isdigit()):
                j = i + offset + 1
                while j < len(instr): # [
                    if instr[j] == ']':
                        nonlocal link
                        try:
                            if next_char(offset) == '-':
                                link = nonunique_links[int(instr[i+offset+1:j])]
                            else:
                                link = unique_links[int(instr[i+offset:j])]
                        except ValueError as ve:
                            exit_with_error("ValueError", j-1)
                        nonlocal endi
                        endi = j
                        return True
                    if not instr[j].isdigit():
                        break
                    j += 1
            return False

        ordered_list_current_number = None
        def close_ordered_list():
            nonlocal ordered_list_current_number, i
            if ordered_list_current_number != None:
                write_to_i("</li>\n</ol>\n", 0)
                ordered_list_current_number = None

        in_unordered_list = False
        def close_unordered_list():
            nonlocal in_unordered_list, i
            if in_unordered_list:
                write_to_i("</li>\n</ul>\n", 0)
                in_unordered_list = False

        ending_tags = []
        new_line_tag = None

        while i < len(instr):
            ch = instr[i]
            if i == 0 or prev_char() == "\n": # if beginning of line
                if ch == '.' and (next_char() in ' ‘'): # ’ this is unordered list
                    close_ordered_list()
                    s = ''
                    if not in_unordered_list:
                        s = "<ul>\n<li>"
                        in_unordered_list = True
                    else:
                        s = "</li>\n<li>"
                    write_to_i(s)
                    new_line_tag = '' # используем тот факт, что разрыва строк в списках вида `. элемент списка` быть не может, и следующий символ \n будет либо закрывать список, либо обозначать начало следующего элемента списка
                    if next_char() == ' ':
                        i += 1
                    else:
                        endqpos = find_ending_pair_quote(i + 1)
                        outfile.write(self.to_html(instr[i+2:endqpos], outer_pos = i+2))
                        i = endqpos
                    writepos = i + 1
                elif in_unordered_list != None:
                    close_unordered_list()
                if ch.isdigit():
                    j = i + 1
                    while j < len(instr):
                        if not instr[j].isdigit():
                            break
                        j += 1
                    if instr[j:j+1] == '.' and instr[j+1:j+2] in (' ', '‘'): # ’ this is ordered list
                        close_unordered_list()
                        value = int(instr[i:j])
                        s = ''
                        if ordered_list_current_number == None:
                            s = ('<ol>' if value == 1 else '<ol start="' + str(value) + '">') + "\n<li>"
                            ordered_list_current_number = value
                        else:
                            s = "</li>\n" + ("<li>" if value == ordered_list_current_number + 1 else '<li value="' + str(value) + '">')
                            ordered_list_current_number = value
                        write_to_i(s)
                        new_line_tag = '' # используем тот факт, что разрыва строк в списках вида `1. элемент списка` быть не может
                        if instr[j+1] == ' ':
                            i = j + 1
                        else:
                            endqpos = find_ending_pair_quote(j + 1)
                            outfile.write(self.to_html(instr[j+2:endqpos], outer_pos = j+2))
                            i = endqpos
                        writepos = i + 1
                    elif ordered_list_current_number != None:
                        close_ordered_list()
                elif ordered_list_current_number != None:
                    close_ordered_list()

                if ch == ' ':
                    write_to_i('&emsp;')
                elif ch == '-': # horizontal rule
                    if i_next_str('--'):
                        j = i + 3
                        while True:
                            if j == len(instr) or instr[j] == "\n":
                                write_to_i("<hr />\n")
                                i = j
                                writepos = j + 1
                                break
                            if instr[j] != '-':
                                break
                            j += 1
                elif ch == '>' and (next_char() in ' ‘'): # ’ this is blockquote
                    write_to_pos(i, i + 2)
                    outfile.write('<blockquote>')
                    if next_char() == ' ':
                        new_line_tag = '</blockquote>'
                    else:
                        ending_tags.append('</blockquote>')
                    i += 1

            if ch == "‘":
                prevci = i - 1
                prevc = instr[prevci] if prevci >= 0 else "\0"
                #assert(prevc == prev_char())
                startqpos = i
                endqpos = i = find_ending_pair_quote(i)
                str_in_b = '' # (
                if prevc == ')':
                    openb = instr.rfind('(', 0, prevci - 1) # )
                    if openb != -1 and openb > 0:
                        str_in_b = instr[openb+1:startqpos-1]
                        prevci = openb - 1
                        prevc = instr[prevci]
                if prevc in 'PР': # Рисунок обрабатывается по-особенному
                    write_to_pos(prevci, endqpos + 1)
                    title = ''
                    if i_next_str('[‘'): # альтернативный текст’
                        endqpos2 = find_ending_pair_quote(i+2)
                        assert(instr[endqpos2+1] == ']')
                        title = ' title="'+html_escapeq(instr[i+3:endqpos2])+'"'
                    imgtag = '<img'
                    if str_in_b != '':
                        wh = str_in_b.replace(',', ' ').split()
                        assert(len(wh) in range(1, 3))
                        imgtag += ' width="' + wh[0] + '" height="' + wh[-1] + '"'
                    imgtag += ' src="'+instr[startqpos+1:endqpos]+'"'+title+' />'
                    if i_next_str('[http'): # ]
                        write_http_link(startqpos, endqpos, 1, imgtag)
                        writepos = i + 1
                    elif i_next_str('[‘'): # ’]
                        outfile.write(imgtag)
                        writepos = endqpos2 + 2
                        i = endqpos2 + 1
                    else:
                        outfile.write(imgtag)
                        i = endqpos
                elif i_next_str('[http'): # ]
                    write_http_link(startqpos, endqpos)
                elif next_char() == '[' and numbered_link(2): # ]
                    i = endi
                    write_to_pos(startqpos, i+1)
                    outfile.write('<a href="' + link + '">' + html_escape(instr[startqpos+1:endqpos]) + '</a>')
                elif i_next_str('[‘'): # ’] сноска/альтернативный текст/текст всплывающей подсказки
                    write_note(startqpos, endqpos)
                elif next_char() == '{' and self.habrahabr_html:
                    # Ищем окончание спойлера }
                    nesting_level = 0
                    i += 2
                    while True:
                        if i == len(instr):
                            exit_with_error('Unended spoiler', endqpos+1)
                        ch = instr[i]
                        if ch == "{":
                            nesting_level += 1
                        elif ch == "}":
                            if nesting_level == 0:
                                break
                            nesting_level -= 1
                        i += 1
                    write_to_pos(prevci, i + 1)
                    outer_p = endqpos+(3 if instr[endqpos+2] == "\n" else 2) # проверка на == "\n" нужна, чтобы переход на новую строку/перевод строки после `{` игнорировался
                    outfile.write('<spoiler title="' + instr[startqpos+1:endqpos].replace('"', "''") + '">' + self.to_html(instr[outer_p:i], outer_pos = outer_p) + '</spoiler>')
                    if next_char() == "\n": # чтобы переход на новую строку/перевод строки после `}` игнорировался
                        i += 1
                        writepos = i + 1
                elif prevc == "'": # raw [html] output
                    t = startqpos - 1
                    while t >= 0:
                        if instr[t] != "'":
                            break
                        t -= 1
                    eat_left = startqpos - 1 - t # количество кавычек, которые нужно съесть слева
                    t = endqpos + 1
                    while t < len(instr):
                        if instr[t] != "'":
                            break
                        t += 1
                    eat_right = t - (endqpos + 1) # количество кавычек, которые нужно съесть справа
                    write_to_pos(startqpos - eat_left, t)
                    outfile.write(instr[startqpos + eat_left:endqpos - eat_right + 1])
                elif prevc == "!":
                    write_to_pos(prevci, endqpos+1)
                    outfile.write(html_escape(instr[startqpos+1:endqpos]).replace("\n", "<br />\n"))
                elif prevc == "#":
                    if self.habrahabr_html:
                        write_to_pos(prevci, endqpos+1)
                        outfile.write(('<source lang="' + str_in_b + '">' if str_in_b else '<code>') + instr[startqpos+1:endqpos] + ("</source>" if str_in_b else "</code>")) # так как <source> в habrahabr — блочный элемент, а не встроенный\inline
                    # elif ohd: # [-TODO syntax highlighting-]
                    else:
                        write_to_pos(prevci, endqpos+1)
                        outfile.write('<pre style="display: inline">' + html_escape(instr[startqpos+1:endqpos]) + '</pre>')
                elif prevc in 'TТ':
                    write_to_pos(prevci, endqpos+1)
                    outfile.write("<table>\n")
                    header_row = False
                    hor_row_align = None
                    ver_row_align = None
                    j = prevci + 2
                    while j < endqpos:
                        ch = instr[j]
                        if ch == "‘": # ’
                            endrow = find_ending_pair_quote(j)
                            hor_col_align = None
                            ver_col_align = None
                            colspan = 1
                            outfile.write("<tr>")

                            # Read table row
                            j += 1
                            while j < endrow:
                                ch = instr[j]
                                if ch == "‘": # ’
                                    end_of_column = find_ending_pair_quote(j)
                                    tag = "th" if header_row else "td"
                                    style = ""
                                    if hor_row_align or hor_col_align:
                                        style += "text-align:" + (hor_col_align if hor_col_align else hor_row_align) + ";"
                                    if ver_row_align or ver_col_align:
                                        style += "vertical-align:" + (ver_col_align if ver_col_align else ver_row_align) + ";"
                                    hor_col_align = None
                                    ver_col_align = None
                                    outfile.write('<' + tag + (' style="'+style+'"' if style else "") + (' colspan="'+str(colspan)+'"' if colspan > 1 else "") + '>' + self.to_html(instr[j+1:end_of_column], outer_pos = j+1) + '</'+tag+'>')
                                    j = end_of_column
                                elif ch in '<>' and instr[j+1:j+2] in ('<', '>'):
                                    hor_col_align = {'<<':'left', '>>':'right', '><':'center', '<>':'justify'}[instr[j:j+2]]
                                    j += 1
                                elif instr[j:j+2] in ("/\\", "\\/"):
                                    ver_col_align = "top" if instr[j:j+2] == "/\\" else "bottom"
                                    j += 1
                                elif ch == "-":
                                    colspan += 1
                                elif ch not in " \t\n":
                                    exit_with_error('Unknown formatting character inside table row', j)
                                j += 1

                            outfile.write("</tr>\n")
                            header_row = False
                            hor_row_align = None
                            ver_row_align = None
                        elif ch in 'HН':
                            header_row = True
                        elif ch in '<>' and instr[j+1:j+2] in ('<', '>'):
                            hor_row_align = {'<<':'left', '>>':'right', '><':'center', '<>':'justify'}[instr[j:j+2]]
                            j += 1
                        elif instr[j:j+2] in ("/\\", "\\/"):
                            ver_row_align = "top" if instr[j:j+2] == "/\\" else "bottom"
                            j += 1
                        elif ch not in " \t\n":
                            exit_with_error('Unknown formatting character inside table', j)

                        j += 1
                    outfile.write("</table>\n")
                    new_line_tag = ''
                else:
                    i = startqpos # откатываем позицию обратно
                    if prev_char() in '*_-~':
                        write_to_pos(i - 1, i + 1)
                        tag = {'*':'b', '_':'u', '-':'s', '~':'i'}[prev_char()]
                        outfile.write('<' + tag + '>')
                        ending_tags.append('</' + tag + '>')
                    elif prevc in 'HН':
                        write_to_pos(prevci, i + 1)
                        tag = 'h' + str(min(max(3 - (0 if str_in_b == '' else int(str_in_b)), 1), 6))
                        outfile.write('<' + tag + '>')
                        ending_tags.append('</' + tag + '>')
                    elif prevc in 'CС':
                        write_to_pos(prevci, i + 1)
                        outfile.write('<span style="color:' + str_in_b + ';">')
                        ending_tags.append('</span>')
                    elif prevc in '<>' and instr[prevci-1] in '<>': # выравнивание текста \ text alignment
                        write_to_pos(prevci-1, i + 1)
                        outfile.write('<div align="' + {'<<':'left', '>>':'right', '><':'center', '<>':'justify'}[instr[prevci-1]+prevc] + '">')
                        ending_tags.append('</div>')
                    elif (instr[prevci-1]+prevc) in ("/\\", "\\/"):
                        write_to_pos(prevci-1, i + 1)
                        tag = 'sup' if (instr[prevci-1]+prevc) == "/\\" else "sub"
                        outfile.write('<' + tag + '>')
                        ending_tags.append('</' + tag + '>')
                    else: # ‘
                        ending_tags.append('’')
            elif ch == "’":
                write_to_pos(i, i + 1)
                if len(ending_tags) == 0:
                    exit_with_error('Unpaired right single quotation mark', i)
                last = ending_tags.pop()
                outfile.write(last)
                if next_char() == "\n" and (last.startswith('</h') # так как <h.> - блоковый элемент, то он автоматически завершает строку, поэтому лишний тег <br> в этом случае добавлять не нужно (иначе получится лишняя пустая строка после заголовка)
                        or last == "</div>"): # также пропускаем лишнюю пустую строку после блока выравнивания текста
                    i += 1
                    writepos += 1
            elif ch == '`':
                # Сначала считаем количество символов ` — это определит границу, где находится окончание span of code
                start = i
                i += 1
                while i < len(instr):
                    if instr[i] != '`':
                        break
                    i += 1
                end = instr.find((i - start)*'`', i)
                if end == -1:
                    exit_with_error('Unended ` started', start)
                write_to_pos(start, end + i - start)
                ins = instr[i:end]
                delta = ins.count("‘") - ins.count("’") # в `backticks` могут быть ‘кавычки’ и в [[[комментариях]]] (выглядит это, например, так: [[[‘]]]`Don’t`), для этого и нужны
                if delta > 0: # эти строки кода[:backticks]
                    for ii in range(delta): # ‘‘
                        ending_tags.append('’')
                else:
                    for ii in range(-delta):
                        assert(ending_tags.pop() == '’')
                ins = html_escape(ins)
                outfile.write('<code>' + ins[0:1]+ins[1:].replace("\n", "<br />\n") + '</code>') # разбивка строки ins[0:1]+ins[1:] нужна для пропуска первого \n
                i = end + i - start - 1
            elif ch == '[': # ]
                if i_next_str('http') or i_next_str('‘') or numbered_link(): # ’
                    s = i - 1
                    while s >= 0 and instr[s] not in "\r\n\t [{(‘“": # ”’)}]
                        s -= 1
                    if i_next_str('‘'): # ’ сноска/альтернативный текст/текст всплывающей подсказки
                        write_note(s + 1, i, 0)
                    elif i_next_str('http'):
                        write_http_link(s + 1, i, 0)
                    else:
                        write_to_pos(s + 1, endi+1)
                        outfile.write('<a href="' + link + '">' + html_escape(instr[s+1:i]) + '</a>')
                        i = endi
                elif i_next_str('[['): # ]] comment
                    comment_start = i
                    nesting_level = 0
                    while True:
                        ch = instr[i]
                        if ch == "[":
                            nesting_level += 1
                        elif ch == "]":
                            nesting_level -= 1
                            if nesting_level == 0:
                                break
                        elif ch == "‘": # [backticks:]а также эти строки кода
                            ending_tags.append('’') # ‘‘
                        elif ch == "’":
                            assert(ending_tags.pop() == '’')
                        i += 1
                        if i == len(instr):
                            exit_with_error('Unended comment started', comment_start)
                    write_to_pos(comment_start, i+1)
                    if instr[comment_start+3:comment_start+4] != '[': # это [[[такой]]] комментарий, а не [[[[такой]]]] или [[[[[такой и [[[[[[так далее]]]]]]]]]]], а [[[такие]]] комментарии следует транслировать в HTML: <!--[[[комментарий]...]...]-->
                        outfile.write('<!--')
                        outfile.write(instr[comment_start:i+1]) # берётся вся строка вместе со [[[скобочками]]] для [[[таких] ситуаций]]
                        outfile.write('-->')
                else:
                    write_to_i('<span class="sq"><span class="sq_brackets">'*ohd+'['+ohd*'</span>')
            elif ch == "]":
                write_to_i('<span class="sq_brackets">'*ohd+']'+ohd*'</span></span>')
            elif ch == "{":
                write_to_i('<span class="cu_brackets" onclick="return spoiler(this, event)"><span class="cu_brackets_b">'*ohd+'{'+ohd*'</span><span>…</span><span class="cu" style="display:none">')
            elif ch == "}":
                write_to_i('</span><span class="cu_brackets_b">'*ohd+'}'+ohd*'</span></span>')
            elif ch == "\n":
                write_to_i((new_line_tag if new_line_tag != None else "<br />") + ("\n" if new_line_tag != '' else "")) # код `"\n" if new_line_tag != ''` нужен только для списков (unordered/ordered list)
                new_line_tag = None

            i += 1

        close_ordered_list()
        close_unordered_list()

        write_to_pos(len(instr), 0)
        assert(len(ending_tags) == 0) # ‘слишком много открывающих одинарных кавычек’/‘где-то есть незакрытая открывающая кавычка’

        assert(self.to_html_called_inside_to_html_outer_pos_list.pop() == outer_pos)

        if isinstance(outfile, FileToStringProxy):
            return "".join(outfile.result)

def to_html(instr, outfile = None, ohd = 0, *, habrahabr_html = False):
    return Converter(habrahabr_html).to_html(instr, outfile, ohd)


if __name__ == '__main__':
    # Support running module as a command line command.
    parser = argparse.ArgumentParser(description = "A Python implementation of pq markup to HTML converter.", usage = "pqmarkup [options] [INPUTFILE]")
    parser.add_argument("--habrahabr-html", help = "for publishing posts on habrahabr.ru", action = 'store_true')
    parser.add_argument("--output-html-document", help = "add some html header for rough testing preview of your converted documents", action = 'store_true')
    parser.add_argument("infile",       nargs = '?', type = argparse.FileType('r', encoding = 'utf-8'), default=sys.stdin,  help = "input file (STDIN is assumed if no INPUT_FILE is given)", metavar = 'INPUT_FILE')
    parser.add_argument("-f", "--file", nargs = '?', type = argparse.FileType('w', encoding = 'utf-8'), default=sys.stdout, help = "write output to OUTPUT_FILE (defaults to STDOUT)", metavar = "OUTPUT_FILE", dest = 'outfile')
    args = parser.parse_args()
    if args.output_html_document and args.habrahabr_html:
        exit("Arguments --output-html-document and --habrahabr-html are mutually exclusive")

    if args.output_html_document:
        args.outfile.write('''\
<html>
<head>
<meta charset="utf-8" />
<base target="_blank">
<script type="text/javascript">
function spoiler(element, event)
{
    if (event.target.nodeName == 'A')//чтобы работали ссылки в спойлерах
        return;
    var e = element.firstChild.nextSibling.nextSibling;//element.getElementsByTagName('span')[0]
    e.previousSibling.style.display = e.style.display;//<span>…</span> must have inverted display style
    e.style.display = (e.style.display == "none" ? "" : "none");
    element.firstChild.style.fontWeight =
    element. lastChild.style.fontWeight = (e.style.display == "" ? "normal" : "bold");
    event.stopPropagation();
}
</script>
<style type="text/css">
    body td {
        font-size: 14px;
        font-family: Verdana, sans-serif;
        line-height: 160%;
    }
    span.cu_brackets_b {
        font-size: initial;
        font-family: initial;
        font-weight: bold;
    }
    a {
        text-decoration: none;
        color: #6da3bd;
    }
    a:hover {
        text-decoration: underline;
        color: #4d7285;
    }
    h3 {
        margin: 0;
        font-size: 137.5%;
        font-weight: 400;
    }
    td {text-align: justify; /* font-family: Tahoma, sans-serif*/}
    span.sq {color: gray; font-size: 0.8rem; font-weight: normal; /*pointer-events: none;*/}
    span.sq_brackets {color: #DDD}
    span.cu_brackets {cursor: pointer}
    span.cu {background-color: #F7F7FF}
    abbr {text-decoration: underline; text-decoration-style: dashed}
    pre, code {font-family: 'Courier New'}
    table table {margin: 1.5em 0; border-collapse: collapse}
    table table th, table table td {padding: .3em; border: 1px solid #ccc}
</style>
</head>
<body>
<table width="55%" align="center"><tr><td>
''')
    to_html(args.infile.read(), args.outfile, 1 if args.output_html_document else 0, habrahabr_html = args.habrahabr_html)
    if args.output_html_document:
        args.outfile.write('''
</td></tr></table>
</body>
</html>''')
