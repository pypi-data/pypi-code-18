"""
Provides a wrapper for csv (kinda) and allows for transforming a csv file to a
json file.
"""

import csv
import json

class CSVToJson(object):
    """Houses all of the functionality for CSVToJson"""

    def __init__(self):
        """Initialize the class"""

        self.csv_file = None
        self.json_file = None
        self.columns = []

    def _check_columns(self, columns, row):
        """Check for the ValueError"""

        if len(columns) != len(row):
            exception_message = ''
            row_len = len(row)
            col_len = len(columns)

            if col_len > row_len:
                exception_message = (
                    'Expected only {row_len} columns but got {col_len} columns.'
                )
            else:
                exception_message = (
                    'Expected {row_len} columns but only got {col_len} columns.'
                )

            exception_message = exception_message.format(row_len=row_len, col_len=col_len)

            raise ValueError(exception_message)

        return True

    def _handle_row(self, row):
        """Handle the specified row, turn it into a dict"""

        columns = self.columns

        current_dict = {}

        for i, column in enumerate(columns):
            current_dict[column] = row[i]

        return current_dict

    def start(self, csv_file, columns):
        """Start the program"""

        self.csv_file = csv_file

        json_file_name = '{without_extension}.json'.format(without_extension=csv_file.name[:-4])

        self.json_file = open(json_file_name, 'w')
        self.columns = columns

        file_decoded = csv.reader(csv_file, delimiter=',', quotechar='|')
        json_file = self.json_file

        current_list = []

        for i, row in enumerate(file_decoded):
            
            if i == 0:
                self._check_columns(columns, row)
            else:
                current_object = self._handle_row(row)

                current_list.append(current_object)

        json_file.write(str(json.dumps(current_list)))

        return current_list
