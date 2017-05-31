#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
A library to get index of refraction (delta) or attenuation length.

Author: Maksim Rakitin (BNL)
2016
"""

import json
import math
import os
from io import StringIO  # StringIO behaves like a file object

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from bnlcrl.utils import convert_types, defaults_file, read_json

parms = defaults_file(suffix='delta')
DAT_DIR = parms['dat_dir']
CONFIG_DIR = parms['config_dir']
DEFAULTS_FILE = parms['defaults_file']


class DeltaFinder:
    def __init__(self, **kwargs):
        # Check importable libs:
        self._check_imports()

        # Get input variables:
        d = read_json(DEFAULTS_FILE)

        self.server_info = d['server_info']
        self.parameters = convert_types(d['parameters'])

        self.default_e_min = self.parameters['e_min']['type'](self.parameters['e_min']['default'])
        self.default_e_max = self.parameters['e_max']['type'](self.parameters['e_max']['default'])

        for key, default_val in self.parameters.items():
            if key in kwargs.keys():
                setattr(self, key, self.parameters[key]['type'](kwargs[key]))
            elif not hasattr(self, key) or getattr(self, key) is None:
                setattr(self, key, default_val['default'])

        self.characteristic_value = None
        self.analytical_delta = None
        self.closest_energy = None
        self.content = None
        self.raw_content = None
        self.method = None  # can be 'file', 'server', 'calculation'
        self.output = None
        self.elements = self.formula.split(',')
        self.element = self.elements[-1]

        if self.outfile:
            self.save_to_file()
            return

        if not self.data_file:
            self.method = 'server'
            self._request_from_server()
        else:
            self.method = 'file'
            self.data_file = os.path.join(DAT_DIR, self.data_file)

        if self.calc_delta:
            if self.available_libs['periodictable']:
                self.method = 'calculation'
                self.calculate_delta()
                self.characteristic_value = self.analytical_delta
                self.closest_energy = self.energy
            else:
                raise ValueError('"periodictable" library is not available. Install it if you want to use it.')
        else:
            self._find_characteristic_value()

        if self.verbose:
            self.print_info()

        if self.save_output:
            return_dict = {}
            for k in d['cli_functions']['find_delta']['returns']:
                return_dict[k] = getattr(self, k)
            file_name = '{}.json'.format(self._output_file_name(self.elements, self.characteristic))
            with open(file_name, 'w') as f:
                json.dump(return_dict, f)

    def calculate_delta(self):
        rho = getattr(self.periodictable, self.formula).density
        z = getattr(self.periodictable, self.formula).number
        mass = getattr(self.periodictable, self.formula).mass
        z_over_a = z / mass
        wl = 2 * math.pi * 1973 / self.energy  # lambda= (2pi (hc))/E
        self.analytical_delta = 2.7e-6 * wl ** 2 * rho * z_over_a

    def plot_data(self, df, elements, property, file_name='data', x_label=None, figsize=(10, 6)):
        thickness = ', thickness={} [$\mathrm{{\mu}}$m]'.format(self.thickness) if property == 'transmission' else ''

        fig = plt.figure(figsize=figsize)
        axes = fig.add_subplot(111)
        ax = df.plot(x_label, grid=True, ax=axes)
        ax.set_title(r'{}: {} ({}-{} eV, {} points{})'.format(
            property.capitalize(),
            ', '.join(elements),
            self.e_min,
            self.e_max,
            self.n_points,
            thickness,
        ))
        ax.set_xlabel(x_label)
        ax.set_ylabel('{}'.format(property.capitalize()))
        plt.savefig('{}.png'.format(file_name))
        if self.show_plot:
            plt.show()

    def print_info(self):
        msg = 'Found {}={} for the closest energy={} eV from {}.'
        print(msg.format(self.characteristic, self.characteristic_value, self.closest_energy, self.method))

    def save_to_csv(self, df, file_name='data', index=False):
        df.to_csv('{}.csv'.format(file_name), index=index)

    def save_to_file(self):
        self.e_min = self.default_e_min
        self.e_max = self.e_min
        counter = 0
        try:
            os.remove(self.outfile)
        except:
            pass
        while self.e_max < self.default_e_max:
            self.e_max += self.n_points * self.e_step
            if self.e_max > self.default_e_max:
                self.e_max = self.default_e_max

            self._request_from_server()

            if counter > 0:
                # Get rid of headers (2 first rows) and the first data row to avoid data overlap:
                content = self.content.split('\n')
                self.content = '\n'.join(content[3:])

            with open(self.outfile, 'a') as f:
                f.write(self.content)

            counter += 1
            self.e_min = self.e_max

        if self.verbose:
            print('Data from {} eV to {} eV saved to the <{}> file.'.format(
                self.default_e_min, self.default_e_max, self.outfile))
            print('Energy step: {} eV, number of points/chunk: {}, number of chunks {}.'.format(
                self.e_step, self.n_points, counter))

    def _check_imports(self):
        self.available_libs = {
            'numpy': None,
            'periodictable': None,
            'requests': None,
        }
        for key in self.available_libs.keys():
            try:
                __import__(key)
                setattr(self, key, __import__(key))
                self.available_libs[key] = True
            except:
                self.available_libs[key] = False

    def _find_characteristic_value(self):
        skiprows = 2
        energy_column = 0
        characteristic_value_column = 1
        error_msg = 'Error! Use energy range from {} to {} eV.'
        if self.use_numpy and self.available_libs['numpy']:
            if self.data_file:
                data = self.numpy.loadtxt(self.data_file, skiprows=skiprows)

                self.default_e_min = data[0, energy_column]
                self.default_e_max = data[-1, energy_column]

                try:
                    idx_previous = self.numpy.where(data[:, energy_column] <= self.energy)[0][-1]
                    idx_next = self.numpy.where(data[:, energy_column] > self.energy)[0][0]
                except IndexError:
                    raise Exception(error_msg.format(self.default_e_min, self.default_e_max))

                idx = idx_previous if abs(data[idx_previous, energy_column] - self.energy) <= abs(
                    data[idx_next, energy_column] - self.energy) else idx_next

                self.characteristic_value = data[idx][characteristic_value_column]
                self.closest_energy = data[idx][energy_column]
            else:
                raise Exception('Processing with NumPy is only possible with the specified file, not content.')
        else:
            if not self.content:
                with open(self.data_file, 'r') as f:
                    self.raw_content = f.read()
            else:
                if type(self.content) != list:
                    self.raw_content = self.content

            self.content = self.raw_content.strip().split('\n')

            energies = []
            characteristic_values = []
            for i in range(skiprows, len(self.content)):
                energies.append(float(self.content[i].split()[energy_column]))
                characteristic_values.append(float(self.content[i].split()[characteristic_value_column]))

            self.default_e_min = energies[0]
            self.default_e_max = energies[-1]

            indices_previous = []
            indices_next = []
            try:
                for i in range(len(energies)):
                    if energies[i] <= self.energy:
                        indices_previous.append(i)
                    else:
                        indices_next.append(i)
                idx_previous = indices_previous[-1]
                idx_next = indices_next[0]
            except IndexError:
                raise Exception(error_msg.format(self.default_e_min, self.default_e_max))

            idx = idx_previous if abs(energies[idx_previous] - self.energy) <= abs(
                energies[idx_next] - self.energy) else idx_next

            self.characteristic_value = characteristic_values[idx]
            self.closest_energy = energies[idx]
        if self.characteristic == 'atten':
            self.characteristic_value *= 1e-6  # Atten Length (microns)

    def _get_remote_file_content(self):
        get_url = '{}{}'.format(self.server_info['server'], self.file_name)
        r = self.requests.get(get_url)
        self.content = r.text
        return self.content

    def _get_remote_file_name(self, formula=None):
        if self.precise:
            e_min = self.energy - 1.0
            e_max = self.energy + 1.0
        else:
            e_min = self.e_min
            e_max = self.e_max
        payload = {
            self.server_info[self.characteristic]['fields']['density']: -1,
            self.server_info[self.characteristic]['fields']['formula']: formula,
            self.server_info[self.characteristic]['fields']['material']: 'Enter Formula',
            self.server_info[self.characteristic]['fields']['max']: e_max,
            self.server_info[self.characteristic]['fields']['min']: e_min,
            self.server_info[self.characteristic]['fields']['npts']: self.n_points,
            self.server_info[self.characteristic]['fields']['output']: 'Text File',
            self.server_info[self.characteristic]['fields']['scan']: 'Energy',
        }
        if self.characteristic == 'atten':
            payload[self.server_info[self.characteristic]['fields']['fixed']] = 90.0
            payload[self.server_info[self.characteristic]['fields']['plot']] = 'Log'
            payload[self.server_info[self.characteristic]['fields']['output']] = 'Plot',
        elif self.characteristic == 'transmission':
            payload[self.server_info[self.characteristic]['fields']['plot']] = 'Linear'
            payload[self.server_info[self.characteristic]['fields']['output']] = 'Plot',
            payload[self.server_info[self.characteristic]['fields']['thickness']] = self.thickness  # um
        r = self.requests.post(
            '{}{}'.format(self.server_info['server'], self.server_info[self.characteristic]['post_url']),
            payload
        )
        content = r.text

        # The file name should be something like '/tmp/xray2565.dat':
        try:
            self.file_name = str(
                content.split('{}='.format(self.server_info[self.characteristic]['file_tag']))[1]
                    .split('>')[0]
                    .replace('"', '')
            )
        except:
            raise Exception('\n\nFile name cannot be found! Server response:\n<{}>'.format(content.strip()))

    @staticmethod
    def _output_file_name(elements, characteristic):
        return '{}_{}'.format(','.join(elements), characteristic) if len(elements) > 1 else characteristic

    def _request_from_server(self):
        if self.available_libs['requests']:
            d = []
            for f in self.formula.split(','):  # to support multiple chemical elements comma-separated list
                self._get_remote_file_name(formula=f)
                r = self._get_remote_file_content()
                d.append(r)
            if self.plot or self.save:
                df, columns = self._to_dataframe(d, self.elements)
                if df is not None and columns is not None:
                    file_name = self._output_file_name(self.elements, self.characteristic)
                    if self.plot:
                        self.plot_data(
                            df=df,
                            elements=self.elements,
                            property=self.characteristic,
                            file_name=file_name,
                            x_label=columns[0],
                        )
                    if self.save:
                        self.save_to_csv(df=df, file_name=file_name)
        else:
            msg = 'Cannot use online resource <{}> to get {}. Use local file instead.'
            raise Exception(msg.format(self.server_info['server'], self.characteristic))

    def _to_dataframe(self, d, elements):
        """Convert a list of strings, each representing the read data, to a Pandas DataFrame object.

        :param d: a list of strings, each representing the read data.
        :param elements: Chemical elements of interest.
        :return: a tuple of DataFrame and the parsed columns.
        """
        df = None
        columns = None
        for i, str_data in enumerate(d):
            element = elements[i]
            c = StringIO(str_data)
            title, columns = str_data.split('\n')[0:2]
            columns = [x.strip() for x in columns.strip().split(',')]
            columns[1] = '{} {}'.format(columns[1], element) if len(elements) > 1 else columns[1]
            data = np.loadtxt(c, skiprows=2)
            if df is None:
                df = pd.DataFrame(data[:, :2], columns=columns[:2])
            else:
                df[columns[1]] = data[:, 1]
        return df, columns
