import yaml

from yaml import Loader, Dumper
from yaml.representer import SafeRepresenter
from collections import OrderedDict

TYPE_1 = 1
TYPE_2 = 2
TYPE_3 = 3

def call(source, export_type, table_classes, tr_classes, th_classes, td_classes):

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    def dict_constructor(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    Dumper.add_representer(OrderedDict, dict_representer)
    Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)

    Dumper.add_representer(str, SafeRepresenter.represent_str)

    with open(source, 'r') as stream:
        try:
            data = yaml.load(stream.read(), Loader=Loader)
        except Exception as e:
            raise(RuntimeError(e))

        table_format = detect_table_format(data)
        table_type, table = convert_to_table(data, table_format)

        if export_type == 'html':
            print_html(table_type, table, table_classes, tr_classes, th_classes, td_classes)


def detect_table_format(data):

    if isinstance(data, dict):
        key = list(data.keys())[0]
        return [dict] + detect_table_format(data[key])
    elif isinstance(data, list):
        return [list] + detect_table_format(data[0])
    else:
        return []


def convert_to_table(data, table_type):

    if table_type == [list]:

        result = []

        for one_data in data:
            result.append([one_data])

        return TYPE_1, result

    elif table_type == [dict, list]:

        table = [[]]
        i = 0

        for element in data:
            table[0].append(element)
            i = 1

            values = []
            for value in data[element]:
                if i + 1 > len(table):
                    table.append([])
                values.append(value)
                table[i].append(value)
                i += 1

        new_table = [table[0]]
        for element in table[1:]:
            new_table.append((element, 0, False))

        return TYPE_2, new_table

    else:

        voyager = data
        for field_type in table_type[:-1]:

            if field_type == list:
                voyager = voyager[0]
            elif field_type == dict:
                voyager = list(voyager.values())[0]

        nb_colum = len(voyager) + 1

        current_line = 0
        table = []

        colums = [' '] + [str(annee) for annee in voyager.keys()]
        creator = TableCreator(colums, nb_colum)
        creator.handler(data)

        return TYPE_3, creator.table

class TableCreator:

    def __init__(self, colums, nb_colum):
        self.table = []
        self.table.append(colums)
        self.nb_colum = nb_colum

    def handler(self, data):

        self._handler(data, 0)

    def _handler(self, data, level):

        if isinstance(data, dict):

            for key, subdata in data.items():

                if isinstance(subdata, dict):
                    is_sub = False
                    for subdata2 in subdata.values():
                        if isinstance(subdata2, dict):
                            is_sub = True
                            break

                    line = [' ' for j in range(0, self.nb_colum)]
                    line[0] = key

                    if is_sub:
                        self.table.append((line, level, is_sub))
                        self._handler(subdata, level + 1)
                    else:
                        i = 1
                        for key, value in subdata.items():
                            line[i] = value
                            i += 1
                        self.table.append((line, level, is_sub))
                else:
                    line = [' ' for j in range(0, self.nb_colum)]
                    line[0] = key
                    line[1] = subdata
                    self.table.append((line, -1, False))


def print_html(table_type, table, table_classes, tr_classes, th_classes, td_classes):

    print('<table class="{}">'.format(' '.join(table_classes)) if table_classes else '<table>')
    print('  <tr class="{}">'.format('') if tr_classes else '  <tr>')

    column = 0
    for subelem in table[0]:
        subelem_str = subelem

        if table_type == TYPE_1:
            print('    <td class="{}">{}</td>'.format(' '.join(td_classes), subelem_str) if td_classes else '    <td>{}</td>'.format(subelem_str))
        else:
            print('    <th class="{}">{}</th>'.format(' '.join(th_classes), subelem_str) if th_classes else '    <th>{}</th>'.format(subelem_str))
        column += 1
    print('  </tr>')

    for elem in table[1:]:

        if table_type == TYPE_1:
            print('  <tr>'.format(elem, ''))
            print('    <td class="{}">{}</td>'.format(' '.join(td_classes), elem) if td_classes else '    <td>{}</td>'.format(elem[0]))
            print('  </tr>')
        else:
            name = elem[0][0]
            if isinstance(name, str):
                classname = name.replace(' ', '-').lower().replace('(', '').replace(')', '')
            else:
                classname = name

            if elem[2]:
                if table_type == TYPE_3:
                    print('  <tr class="chokola-level-{0} chokola-{1} {2}">'.format(elem[1], classname, ' '.join(tr_classes) if tr_classes else ''))
                elif table_type == TYPE_2:
                    print('  <tr class="chokola-level-{0} {1}">'.format(elem[1], ''))

            else:
                if table_type == TYPE_3:
                    print('  <tr class="chokola-leef chokola-{1} {2}">'.format(elem[1], classname, ' '.join(tr_classes) if tr_classes else ''))
                elif table_type == TYPE_2:
                    print('  <tr class="chokola-leef {0}">'.format(''))

            column = 0
            for subelem in elem[0]:
                print('    <td class="{}">{}</td>'.format(' '.join(td_classes), subelem) if td_classes else '    <td>{}</td>'.format(subelem))
                column += 1
            print('  </tr>')

    print('</table>')
