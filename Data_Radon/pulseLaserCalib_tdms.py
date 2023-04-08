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
    plt.plot(range(len(np)), np)
    # Add labels to the plot
    plt.title('Waveform')
    plt.xlabel('Index')
    plt.ylabel('Value')
    # Display the plot
    plt.show()

if __name__ == "__main__":

    for in_filename in args.in_filenames:
        with TdmsFile.open(in_filename) as tdms_file:
            # Read Meta Data (Basic information)
            metadata = tdms_file.properties
            metadata_df = pd.DataFrame(metadata.items(), columns=['metaKey', 'metaValue'])
            print(metadata_df)
            # Read Groups and Channels
            Read_Groups_and_Channels(tdms_file)

            channel_sum = 0.0
            channel_length = 0
            nPass=0
            ranges=[]
            # Start Looping through events
            for event, chunk in enumerate(tdms_file.data_chunks()):
                if ( event % args.report == 0 ): print ("Processing event", event )
                ch1 = chunk['ADC Readout Channels']['ch0']._data() # Read ch1 into np array
                threshold=0.3
                if (len(ch1)>0 and (ch1 > threshold).any() ):
                    nPass+=1 # Count events passing the selection
                    channel_length += len(ch1) # Count total samples
                    channel_sum += ch1[:].sum() # Sum over all samples, useful to calculate pedestal average
                    # Calculate pulse amplitude(range) --> Maximum - pedestal
                    pedestal_average = np.mean(ch1[0:25])
                    maximum = np.max(ch1)
                    range = maximum - pedestal_average
                    ranges.append(range)

                    indices = np.where(ch1 > 0.3)[0]
                    # if (len(indices) > 0): print(indices[0])
                    # event_display(ch1)

            channel_mean = channel_sum / channel_length
            print(channel_length, channel_mean)

            # Create an empty histogram using matplotlib.pyplot.hist()
            hist, bins, patches = plt.hist(ranges, bins=50, range=(0, 1), alpha=0.5, color='blue')
            plt.show()
