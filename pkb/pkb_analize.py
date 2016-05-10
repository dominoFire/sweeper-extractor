# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 23:13:52 2016

@author: microkid
"""

import json
import numpy as np
import pandas as pd


if __name__ == '__main__':
    filepath = 'data/pkb_results.json'
    with open(filepath, 'r') as fh:
        results =json.load(fh)
        
    pkb_results = pd.DataFrame(results)
    machine_type_list = pkb_results['labels'].str.replace('|', '').str.split(',') 
    labels_dict = machine_type_list.apply(lambda li: { e.split(':')[0] : e.split(':')[1] for e in li })
    
    pkb_results['machine_type']= labels_dict.apply(lambda d: d['machine_type'])
    pkb_results['zone'] = labels_dict.apply(lambda d: d['zones'])
    
    pkb = pkb_results[pkb_results.test == 'unixbench']
    
    pkb_stats = pkb.groupby(['machine_type', 'metric', 'zone'])['value'].agg([np.mean, np.std, len])
    
    pkb_stats.to_csv('./data/results.csv', encoding='UTF-8')
    