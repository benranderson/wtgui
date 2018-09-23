import csv
import os
import json
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


class SettingsModel:
    """A model for saving settings"""

    variables = {
        'autofill date': {'type': 'bool', 'value': True},
        'autofill sheet data': {'type': 'bool', 'value': True}
    }

    def __init__(self, filename='wt_settings.json', path='~'):
        # determine the file path
        self.filepath = os.path.join(os.path.expanduser(path), filename)

        # load in saved values
        self.load()

    def set(self, key, value):
        """Set a variable value"""
        if (
            key in self.variables and
            type(value).__name__ == self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")

    def save(self):
        """Save the current settings to the file"""
        json_string = json.dumps(self.variables)
        with open(self.filepath, 'w') as fh:
            fh.write(json_string)

    def load(self):
        """Load the settings from the file"""

        # if the file doesn't exist, return
        if not os.path.exists(self.filepath):
            return

        # open the file and read in the raw values
        with open(self.filepath, 'r') as fh:
            raw_values = json.loads(fh.read())

        # don't implicitly trust the raw values,
        # but onlg get known keys
        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value
