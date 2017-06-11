import click
import os, sys
import errno
import pandas as pd
import numpy as np
import dnamodel as dm
from sklearn.preprocessing import MinMaxScaler




all_colors = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', \
             'cyan', 'white'

@click.command()
@click.argument('input_file')
@click.option('--model', '-m', type=click.Path(), help='An existing dnamodel .h5 file')
@click.option('--config', '-c', type=click.Path(), help='A json configuration file')


def main(input_file, model, config):
    """Automated, experimentally-driven design and optimization of DNA sequences."""
    greet = 'Hello'


    raw_data = pd.read_excel(input_file, header=0)
    
    col_names = ['sequence']
    for i in range(1, len(raw_data.columns)):
        col_names.append('output'+str(i))
    raw_data.columns = col_names
    

    #TO DO: should do this for each column
    df = raw_data[np.isfinite(raw_data['output1'])]

    dnaCNN = dm.dnaModel(df, filename=model, config = config) 
    
    dnaCNN.train()
    
    dnaCNN.design()

    dnaCNN.save()

    dnaCNN.test()
