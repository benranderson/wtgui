import csv
import os
from .constants import FieldTypes as FT


class CSVModel:
    """CSV file storage"""

    fields = {
        'Project': {'req': False, 'type': FT.string},
        'Originator': {'req': True, 'type': FT.string},
        'Date': {'req': True, 'type': FT.iso_date_string},
        'Checker': {'req': True, 'type': FT.string},
        'CheckDate': {'req': True, 'type': FT.iso_date_string},
        'D_o': {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000,
                'inc': .01},
        't_sel': {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000,
                  'inc': .01},
        't_cor': {'req': False, 'type': FT.decimal, 'min': 0, 'max': 1000,
                  'inc': .01},
        'tol': {'req': False, 'type': FT.decimal, 'min': 0, 'max': 100,
                'inc': .01},
        'B': {'req': False, 'type': FT.decimal, 'min': 0, 'max': 100,
              'inc': .01},
        'SMYS': {'req': True, 'type': FT.decimal, 'min': 0, 'max': 100000,
                 'inc': .01},
        'E': {'req': True, 'type': FT.decimal, 'min': 0, 'max': 100000,
              'inc': .01},
        'v': {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1,
              'inc': .01},
    }

    def __init__(self, filename):
        self.filename = filename

    def save_record(self, data):
        """Save a dict of data to the CSV file"""

        newfile = not os.path.exists(self.filename)

        with open(self.filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
