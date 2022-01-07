"""
## =========================================================================== ## 
MIT License
Copyright (c) 2021 Roman Parak
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
## =========================================================================== ## 
Author   : Roman Parak
Email    : Roman.Parak@outlook.com
Github   : https://github.com/rparak
File Name: data_evaluation_anim.py
## =========================================================================== ## 
"""

# System (Default)
import sys
# Pandas (Data analysis and manipulation) [pip3 install pandas]
import pandas as pd
# Numpy (Array computing) [pip3 install numpy]
import numpy as np
# Matplotlib (Visualization) [pip3 install matplotlib]
import matplotlib.pyplot as plt
from matplotlib import animation
# OS (Operating system interfaces)
import os
# Lib.Signal.Filter (Filters: SMA, BLP)
import Signal.Filter as Filter

# Input Data:    
file_name   = 'Test_data'
folder_name = 'Data'
#   Visible name of title
title_visibility = True
#   Name of GIF file
gif_file_name = 'ALL'

# Create figure
fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5, forward=True)

# Initialization of filters:
#   Simple Moving Average (SMA)
SMA = Filter.Simple_Moving_Average([-22.5, 22.5], 100)
#   Butterworth Low Pass (BLP)
BLP = Filter.Butterworth_Low_Pass([-22.5, 22.5], 100, 1/0.004, 1.95, 3)
#   Butterworth Low Pass Moving Average (BLPMA)
BLPMA = Filter.Butterworth_Low_Pass_Moving_Average([-22.5, 22.5], 100, 20, 1/0.004, 1.95, 3)

# Initialization of lines and vectorization of variables:
#   Filter vector: 
#       [SMA, BLP, BLPMA]
#   Line vector: 
#       [Line_RD, Line_SMA, Line_BLP, Line_BLPMA]
if gif_file_name == 'RAW': 
    Line_RD, = ax.plot([], [], '-', linewidth=0.75, color=[0.2,0.4,0.6,1.0], label='Raw Data')
    Filters  = [None]
    Lines    = [Line_RD]
elif gif_file_name == 'SMA':
    Line_RD,  = ax.plot([], [], '-', linewidth=0.75, color=[0.2,0.4,0.6,1.0], label='Raw Data')
    Line_SMA, = ax.plot([], [], '-', linewidth=1.25, color=[1.0,0.85,0.75,1.0], label='Filtered Data: SMA')
    Filters  = [SMA]
    Lines    = [Line_RD, Line_SMA]
elif gif_file_name == 'BLP':
    Line_RD,  = ax.plot([], [], '-', linewidth=0.75, color=[0.2,0.4,0.6,1.0], label='Raw Data')
    Line_BLP, = ax.plot([], [], '-', linewidth=1.25, color=[1.0,0.75,0.5,1.0], label='Filtered Data: BLP')
    Filters  = [BLP]
    Lines    = [Line_RD, Line_BLP]
elif gif_file_name == 'BLPMA': 
    Line_RD,    = ax.plot([], [], '-', linewidth=0.75, color=[0.2,0.4,0.6,1.0], label='Raw Data')
    Line_BLPMA, = ax.plot([], [], '-', linewidth=1.25, color=[0.8,0.4,0.0,1.0], label='Filtered Data: BLPMA')
    Filters  = [BLPMA]
    Lines    = [Line_RD, Line_BLPMA]
elif gif_file_name == 'ALL': 
    Line_RD,    = ax.plot([], [], '-', linewidth=0.75, color=[0.2,0.4,0.6,1.0], label='Raw Data')
    Line_SMA,   = ax.plot([], [], '-', linewidth=1.25, color=[1.0,0.85,0.75,1.0], label='Filtered Data: SMA')
    Line_BLP,   = ax.plot([], [], '-', linewidth=1.25, color=[1.0,0.75,0.5,1.0], label='Filtered Data: BLP')
    Line_BLPMA, = ax.plot([], [], '-', linewidth=1.25, color=[0.8,0.4,0.0,1.0], label='Filtered Data: BLPMA')
    Filters  = [SMA, BLP, BLPMA]
    Lines    = [Line_RD, Line_SMA, Line_BLP, Line_BLPMA]

# Data initialization for animation:
x_data = [] 
y_data = [[], [], [], []]

def init_animation():
    """
    Description: 
        Initialize the individual animated lines that will move in the animation.

    Returns:
        (1) parameter [Float Vector]: Array of individual lines.
    """

    for _, l in enumerate(Lines):
        l.set_data([], [])

    return Lines

def update_animation(idx, Data, Filters):
    """
    Description:
        Line graph animation update.

    Args:
        (1) i [INT]: Iteration of the graph. 
        (2) Data [Float Vector, Float Vector]: Sequence, raw data read from a file. 
        (3) Filters [Class Vector: Signal.Filter]: Vector of signal processing filters.

    Returns:
        (1) parameter [Float Vector]: Array of individual lines. 

    """

    x_data.append(Data[0][idx])

    for i, (y, l) in enumerate(zip(y_data, Lines)):
        if i == 0:
            y.append(Data[1][idx])
        else:
            y.append(Filters[i - 1].Compute(Data[1][idx]))
        
        l.set_data(x_data, y)

    print(f'[INFO] Progress in GIF creation: {np.round(100 * np.float(idx)/np.float(len(Data[0])),1)} %')

    return Lines

def main():
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

    if title_visibility == True:
        fig.suptitle(f'File name: {file_name}.txt', fontsize = 20)

    # Set axis name: Depends on the input file
    AXIS_NAME = 'X (cm)'

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

    # Start Animation
    anim = animation.FuncAnimation(fig, update_animation, init_func=init_animation, frames=len(data), interval=4, 
                                   fargs=([sequence, data], Filters, ), blit=True, repeat=False)
    # Save Animation
    anim.save(f'GIF\\{gif_file_name}.gif', fps=30, bitrate=1000)
    print(f'[INFO] Progress in GIF creation: 100.0 %')
    print(f'[INFO] The GIF animation is successfully saved.')

if __name__ == '__main__':
    sys.exit(main())
