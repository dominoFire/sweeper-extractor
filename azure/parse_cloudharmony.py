# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 13:46:48 2016

@author: microkid
"""

import pandas as pd
from bs4 import BeautifulSoup


if __name__ == '__main__':
    html_file = 'azure/archives/cloudharmony.html'
    with open(html_file, 'r') as fh:
        html_doc = fh.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    tables = soup.find_all('table')

    tbls = pd.read_html(str(tables[0]), parse_dates=False, flavor='html5lib')

    for i,df in enumerate(tbls):
        df.to_csv('azure/archives/cloudharmony{}.csv'.format(i), index=False, encoding='UTF-8')

    # Analizamos solo el primer resultado    
    tbl_all = tbls[0]
    # La tabla del archivo solo contiene una parte de tests hechos con el
    # SpecINT    

    tbl_azure = tbl_all[ tbl_all['Service'].str.contains("Azure") ]
    #tbl_azure['instance_type'] = tbl_azure.loc[:, 'Instance Type'].str.extract(r'([A-Za-z0-9]+) - ')
    tbl_azure.to_csv('azure/data/azure_vm_performance.csv', index=False, encoding='UTF-8')

