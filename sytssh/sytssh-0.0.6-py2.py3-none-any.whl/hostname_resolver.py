import database
import re
import sqlite3
import math

class HostnameResolver:
    
    def __init__(self, value):
        self.value = value
        self.hostname = value if not self.has_port(value) else value[:value.find(':')]
    
    def is_multiple_hosts(self):
        return re.match('.*{\d+\-\d+}.*', self.hostname) is not None

    def get_instance_number(self):
        try:
            row = database.execute('select max(instance)+1 from control where datetime(\'now\') < \
                datetime(time, \'+1 minutes\')').fetchone()
            next_val = 1 if row[0] is None else row[0]
            database.execute('insert into control(instance, time) values (?, datetime(\'now\'))', (next_val,))
            database.con.commit()
            return next_val
        except sqlite3.OperationalError:
            self.get_instance_number()

    def get_hostname(self, instance=0):
        if not self.is_multiple_hosts():
            return self.hostname
        if instance > 0:
            return re.sub(r'\{.*\}', '%s' % instance, self.hostname) 

        process_number = self.get_instance_number()

        start = int(self.start_range())
        end = int(self.end_range())
        range = end - start + 1

        percent = round(math.modf(float(process_number) / float(range))[0], 2)
        instance_number = int(range  * percent) if percent != 0.0 else end

        return re.sub(r'\{.*\}', '%s' % instance_number, self.hostname) 

    def get_port(self, default_port=22):
        return self.value[self.value.find(':')+1:] if self.has_port(self.value) else default_port

    def has_port(self, str):
        return ':' in str

    def start_range(self):
        found = re.search('{\d+-', self.value).group()
        return re.sub("[\{\-\}]", "", found)
    
    def end_range(self):
        found = re.search('-\d+}', self.value).group()
        return re.sub("[\{\-\}]", "", found)



