# Questo file elimina ogni precedente out file

import os

# Clearing options

clear_figures = True
clear_outfiles = True
clear_cloud = True
clear_IDA = True
clear_PP = True
clear_connectionFragility = True

figures_directories = [
    'Figures\Acc_Envelopes',
    'Figures\Base_Shear_Disp',
    'Figures\Disp_Time',
    'Figures\Drift_Envelopes',
    'Figures\Velocity_Envelopes'
]

outfiles_directories = [
    'Output\TimeHistory',
    'Output\Pushover',
    'Output\Processed',
    'Output\Modal'
]

cloud_directories = [
    'Output\Cloud',
    'Output\Fragility',
    'Output\Fragility\Figures'
]

IDA_directories = [
    'Output\IDA\Curves',
    'Output\IDA\Figures',
    'Output\IDA\Fragility',
    'Output\IDA\Outputs_Junk'
]

PP_directories = [
    'Output\PerformancePoint'
]

ConnectionFragility_directories = [
    'Output\Connection_Fragility\Data\Cloud',
    'Output\Connection_Fragility\Data\Fragility',
    'Output\Connection_Fragility\Figures\DS1',
    'Output\Connection_Fragility\Figures\DS2',
    'Output\Connection_Fragility\Figures\DST', 
]

directories = []

if clear_figures:

    [directories.append(dir) for dir in figures_directories]

if clear_outfiles:

    [directories.append(dir) for dir in outfiles_directories]

if clear_cloud:

    [directories.append(dir) for dir in cloud_directories]

if clear_IDA:

    [directories.append(dir) for dir in IDA_directories]

if clear_PP:

    [directories.append(dir) for dir in PP_directories]

if clear_connectionFragility:

    [directories.append(dir) for dir in ConnectionFragility_directories]

# print(directories)

for directory in directories:

    for filename in os.listdir(directory):

        try:

            os.remove(f'{directory}/{filename}')
        
        except:

            print(f'could not delete file {directory}\{filename}. If it is a folder, ignore this msg.')

       
