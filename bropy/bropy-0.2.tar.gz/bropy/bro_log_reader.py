import datetime

class BroLogReader(object):
    
    def __init__(self):
        """ Sets default separators and unset values of bro log.
            
            """
        self.separator     = '\t'      # default separator
        self.set_separator = ','       # default set separator
        self.empty_field   = '(empty)' # default empty field
        self.unset_field   = '-'       # default unset field

    def read_logs(self, filename):
        """ Read logs from file filename.
            
            Parameters
            ----------
            filename : string
                Path to file to be read.
                
            Returns
            -------
            result : iterator
                Iterator over logs from filename
                Each value from iterator is a dictionary of field -> value
                
            """
        fields = []
        types  = []
        with open(filename, 'rb') as inputfile:
            for line in inputfile.readlines():
                if not line.startswith('#'):
                    yield self.make_dict(fields, types, line.strip().split(self.separator))                    
                elif line.startswith('#separator'):
                    self.separator = line[:-1].split(' ', 1)[1]
                    if self.separator.startswith('\\x'):
                        self.separator = self.separator[2:].decode('hex')
                elif line.startswith('#set_separator'):
                    self.set_separator = line[:-1].split(self.separator)[1]
                elif line.startswith('#empty_field'):
                    self.empty_field = line[:-1].split(self.separator)[1]
                elif line.startswith('#unset_field'):
                    self.unset_field = line[:-1].split(self.separator)[1]
                elif line.startswith('#fields'):
                    fields = line.strip().split('\t')[1:]
                elif line.startswith('#types'):
                    types = line.strip().split('\t')[1:]

    def make_dict(self, fields, types, values):
        """ Create dictionary from log.
            
            Parameters
            ----------
            fields : list of string
                Field names of corresponding values
                
            types : list of string
                Types of corresponding vlaues
                
            values : list of string
                Values of log
                
            Returns
            -------
            result : dict()
                result[field] -> type(value)
            
            """
        result = dict()
        for field, field_type, value in zip(fields, types, values):
            # Cast field to timestamp
            if field_type == 'time':
                result[field] = datetime.datetime.fromtimestamp(float(value)) if value != self.empty_field and value != self.unset_field else None
            # Cast field to string
            elif field_type == 'string':
                result[field] = value if value != self.empty_field and value != self.unset_field else None
            # Cast field to boolean
            elif field_type == 'bool':
                result[field] = value == 'T' if value != self.empty_field and value != self.unset_field else None
            # Cast field to first successful cast: int - float - string
            else:
                result[field] = self._cast_value(value) if value != self.empty_field and value != self.unset_field else None
        return result
    
    def _cast_value(self, value):
        """ Try to cast unknown type to int, float, or string.
            The first to succeed is returned.
            
            Parameters
            ----------
            value : string
                Value to be cast
            
            Returns
            -------
            value : int/float/string
                First type to be cast successfully
            """
        test_types = (int, float)
        for cast_test in test_types:
            try:
                return cast_test(value)
            except ValueError:
                continue
        return value