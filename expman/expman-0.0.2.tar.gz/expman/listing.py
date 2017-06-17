import records
import json
import datetime
import os
from tabulate import tabulate
from expman.experiment import Experiment


class Listing:

    def __init__(self, root):
        self.root = root
        self.experiments = []
        for root, dirs, files in os.walk(root):
            if 'results.json' in files:
                fresult = os.path.join(root, 'results.json')
                exp = Experiment.load(root)
                with open(fresult) as f:
                    results = json.load(f)
                    results['last_modified'] = datetime.datetime.fromtimestamp(int(os.path.getmtime(fresult)))
                d = exp.exp_dict()
                d.update(results)
                self.experiments.append(d)

    @property
    def header(self):
        header = set()
        for exp in self.experiments:
            header = header.union(set(list(exp.keys())))
        header = sorted(list(header))
        return header

    def sorted_rows(self, sort_key='last_modified', desc=True):
        sorted_listings = sorted(self.experiments, key=lambda d: d[sort_key], reverse=desc)
        rows = []
        for exp in sorted_listings:
            row = [exp.get(k, None) for k in self.header]
            rows.append(row)
        return rows

    def print_listings(self, sort_key='last_modified', desc=True):
        rows = self.sorted_rows(sort_key, desc)
        print(tabulate(rows, headers=self.header))

    def create_db(self, fdb):
        db = records.Database('sqlite:///{}'.format(fdb))
        types = ['REAL'] * len(self.header)
        header = self.header
        rows = self.sorted_rows()
        for row in rows:
            for j, c in enumerate(row):
                try:
                    float(c)
                except Exception:
                    types[j] = 'TEXT'
        types[header.index('name')] = 'TEXT PRIMARY KEY'
        columns = ['{} {}'.format(h, t) for h, t in zip(header, types)]
        db.query('DROP TABLE if exists experiments')
        db.query('CREATE TABLE experiments ({})'.format(', '.join(columns)))
        keys = [':{}'.format(k) for k in header]
        for row in rows:
            values = {k: v for k, v in zip(header, row)}
            db.query('INSERT INTO experiments VALUES ({})'.format(', '.join(keys)), **values)
        return db
