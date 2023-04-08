#!/usr/bin/env python3

from nptdms import TdmsFile
import pandas as pd
import csv
import numpy as np

import argparse
parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-d',default="./",type=str,help='output directory')
parser.add_argument('--report','-r',default=10000,type=int,help='report every x events')
args = parser.parse_args()

for in_filename in args.in_filenames:
    print (f'Processing {in_filename}')
    with TdmsFile.open(in_filename) as tdms_file:
        # Read Meta Data (Basic information)
        metadata = tdms_file.properties
        metadata_df = pd.DataFrame(metadata.items(), columns=['metaKey', 'metaValue'])
        # read the TDMS file into a dictionary of channels
        tdms_data = tdms_file.as_dataframe()
        # convert the dictionary to a Pandas DataFrame
        data_df = pd.DataFrame(tdms_data)

        csv_filename = in_filename.rsplit('/',1)[1].split('.tdms')[0] + '.csv'
        # write metadata to csv file
        metadata_df.to_csv(csv_filename, index=False)
        # append the DataFrame to a CSV file
        data_df.to_csv(csv_filename, index=False, mode='a')
