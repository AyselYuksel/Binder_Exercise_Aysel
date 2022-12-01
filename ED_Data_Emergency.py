#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:16:17 2022

@author: ayselyuksel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

LONG_URL = 'https://raw.githubusercontent.com/health-data-science-OR/' \
            + 'hpdm139-datasets/main/syn_ts_ed_long.csv'
WIDE_URL = 'https://raw.githubusercontent.com/health-data-science-OR/' \
            + 'hpdm139-datasets/main/syn_ts_ed_wide.csv'
    
long_df = pd.read_csv(LONG_URL)
long_df.head()
print(long_df.head())

wide_df = pd.read_csv(WIDE_URL)
wide_df.head()
print(wide_df.head())

def ed_data_to_wide(file_path):
    '''
    Return the ED data in wide format.
    
    1. Pivot table
    2. Transpose and drop the ('attends', hosp_i) multi-index
    3. Rename columns [0, 1, 2, 4] tp ['hosp_1', 'hosp_2', 'hosp_3', 'hosp_4']
    4. Index to DateTimeIndex
    5. Drop the additional uneeded series 'date' (as stored in index as well)
    6. Convert attendence numbers from int64 to int16
    
    Params:
    ------
    file_path: str
        Path to wide format file
        
    Returns:
    -------
    pandas.DataFrame
    '''
    # column name transfers
    translated_names = {0:'hosp_1', 
                        1:'hosp_2',
                        2:'hosp_3',
                        3:'hosp_4'}

    data_types = {'hosp_1':np.int16, 
                  'hosp_2':np.int16,
                  'hosp_3':np.int16,
                  'hosp_4':np.int16}

    df = (pd.read_csv(file_path)
            .pivot_table(values=['attends'], index=['date'], columns=['hosp'])
            .T.reset_index(drop=True)
            .T.rename(columns=translated_names)
            .assign(date=lambda x: pd.to_datetime(x.index))
            .set_index('date')
            .astype(data_types)
         )

    return df

wide_df = ed_data_to_wide(LONG_URL)
wide_df.info()
print(wide_df.info)