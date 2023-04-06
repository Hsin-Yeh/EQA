#!/usr/bin/env python3

from nptdms import TdmsFile
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-d',default="./",type=str,help='output directory')
parser.add_argument('--report','-r',default=10000,type=int,help='report every x events')
args = parser.parse_args()

def Read_Groups_and_Channels(tdms_file):
    # Loop through each group and print the channel names
    for group in tdms_file.groups():
        print(f"Group '{group.name}':")
        for channel in group.channels():
            print(f"- Channel '{channel.name}':")

def event_display(np):
    # Create a line plot of the data
    plt.plot(range(len(channel_chunk)), channel_chunk)
    # Add labels to the plot
    plt.title('Waveform')
    plt.xlabel('Index')
    plt.ylabel('Value')
    # Display the plot
    plt.show()

if __name__ == "__main__":

    for in_filename in args.in_filenames:
        with TdmsFile.open(in_filename) as tdms_file:
            metadata = tdms_file.properties
            metadata_df = pd.DataFrame(metadata.items(), columns=['metaKey', 'metaValue'])
            print(metadata_df)
            channel_sum = 0.0
            channel_length = 0

            Read_Groups_and_Channels(tdms_file)

            for chunk in tdms_file.data_chunks():
                channel_chunk = chunk['ADC Readout Channels']['ch0']._data()
                channel_length += len(channel_chunk)
                channel_sum += channel_chunk[:].sum()
                indices = np.where(channel_chunk > 0.3)[0]
                if (len(indices) > 0): print(indices[0])
                event_display(channel_chunk)

            channel_mean = channel_sum / channel_length
            print(channel_length, channel_mean)
