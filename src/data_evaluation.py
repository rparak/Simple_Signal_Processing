# System (Default)
import sys
# Time (Time access and conversions)
import time
# Pandas (Data analysis and manipulation) [pip3 install pandas]
import pandas as pd
# Numpy (Array computing) [pip3 install numpy]
import numpy as np
# Matplotlib (Visualization) [pip3 install matplotlib]
import matplotlib.pyplot as plt
# OS (Operating system interfaces)
import os
# Lib.Signal.Filter (Filters: SMA, BLP)
import Signal.Filter as Filter

def Data_Filter(input_rd, filter_cls):
    """
    Description:
        Auxiliary function for data filtering and time evaluation.

    Args:
        (1) input_rd [Float Vector]: Input raw data.
        (2) filter_cls [Class: Signal.Filter]: Type of signal processing filter.
        
    Returns:
        (1) parameter [Float Vector]: The new value of the filter model.
        (2) parameter [Float]: Time to filter the entire data set.
    """

    # t_{0}: time start
    t_0 = time.time()

    # SMA filter calculation
    result_fd = []
    for _, input_dat in enumerate(input_rd):
        result_fd.append(filter_cls.Compute(input_dat))

    # t_{1}: time stop
    #   t = t_{1} - t_{0}
    return (result_fd, time.time() - t_0)

def main():
    # Input Data:    
    file_name   = 'Test_data'
    folder_name = 'Data'
    #   Visible name of title
    title_visibility = True
    #   Visibility of filter results: SMA, BLP, BLPMA
    filter_result_visibility = [True, True, True]

    # Read Data from the File (P5_Results Folder)
    current_directory_name = os.getcwd()
    p5_glove_data = pd.read_csv(current_directory_name + '\\' + folder_name + '\\' + file_name + '.txt')
    print('[INFO] The data is successfully read from the file.')

    # Assign data to variables
    #   Sequence [-]
    sequence = p5_glove_data[p5_glove_data.columns[0]]
    #   Raw Data
    data = p5_glove_data['DATA']
    print(f'[INFO] Number of input data: {len(data)}')

    # Initialization of filters:
    #   Simple Moving Average (SMA)
    SMA = Filter.Simple_Moving_Average([-22.5, 22.5], 100)
    #   Butterworth Low Pass (BLP)
    BLP = Filter.Butterworth_Low_Pass([-22.5, 22.5], 100, 1/0.004, 1.95, 3)
    #   Butterworth Low Pass Moving Average (BLPMA)
    BLPMA = Filter.Butterworth_Low_Pass_Moving_Average([-22.5, 22.5], 100, 20, 1/0.004, 1.95, 3)

    # Filter vector
    #   Used for better program processing
    FILTERS = [SMA, BLP, BLPMA]

    # Create figure
    fig, ax = plt.subplots()
    if title_visibility == True:
        fig.suptitle(f'File name: {file_name}.txt', fontsize = 20)

    # Color for each filter
    C = [[1.0,0.85,0.75,1.0], 
         [1.0,0.75,0.5,1.0], 
         [0.8,0.4,0.0,1.0]]
    # Short name of filters
    FILTER_NAME = ['SMA', 'BLP', 'BLPMA']
    # Set axis name: Depends on the input file
    AXIS_NAME = 'X (cm)'

    # Plot {y} versus {x} as lines.
    #   Raw Data
    ax.plot(sequence, data, '-', linewidth=1.0, color=[0.2,0.4,0.6,0.50], label='Raw Data')

    print('[INFO] Data filtering:')
    for i, (f, f_vis) in enumerate(zip(FILTERS, filter_result_visibility)):
        if f_vis == True:
            # Raw data filter
            (data_f, t) = Data_Filter(data, f)
            print(f'[INFO]  Time ({FILTER_NAME[i]}): {t:0.03f} (s)')
            # Plot of filtered data
            ax.plot(sequence, data_f, '-', linewidth=1.0, color=C[i], label=f'Filtered Data: {FILTER_NAME[i]}')

    # Axis Parameters:
    #   Limits:
    #       X-Limit:
    x_min = np.minimum.reduce([np.minimum.reduce(sequence), np.minimum.reduce(sequence)])
    x_max = np.maximum.reduce([np.maximum.reduce(sequence), np.maximum.reduce(sequence)])
    x_lim_factor = np.abs(x_max - x_min)
    ax.set_xlim([x_min - x_lim_factor*0.01, 
                 x_max + x_lim_factor*0.01])
    #       Y-Limit:
    y_min = np.minimum.reduce([np.minimum.reduce(data), np.minimum.reduce(data)])
    y_max = np.maximum.reduce([np.maximum.reduce(data), np.maximum.reduce(data)])
    y_lim_factor = np.abs(y_max - y_min)
    ax.set_ylim([y_min - y_lim_factor*0.01, 
                 y_max + y_lim_factor*0.01])
    #   Label
    ax.set_xlabel(r'Sequence (-)')
    ax.set_ylabel(f'{AXIS_NAME}')
    #   Other dependencies
    ax.grid(linewidth = 0.75, linestyle = '--')
    ax.legend(fontsize=10.0)

    print('[INFO] Display the result.')
    # Display the result
    plt.show()

if __name__ == '__main__':
    sys.exit(main())
