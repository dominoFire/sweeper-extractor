#!/usr/bin/python3

import pandas as pd


role_size = {
    'ExtraSmall': 'A0',
    'Small': 'A1',
    'Medium': 'A2',
    'Large': 'A3',
    'ExtraLarge': 'A4'
}

def role_name(x):
    if x in role_size.keys():
        return role_size[x]
    ret = x
    if '_' in x:
        ret = x.split('_')[1]
        
    if 'v2' in x:
        return ret + ' v2'
    return ret


def tier_name_from_description(x):
    if 'Basic' in x:
        return 'Basic'
    return 'Standard'


def tier_name(x):
    if x in role_size.keys():
        return 'Standard'
    ret = 'Standard'
    if '_' in x:
        ret = x.split('_')[0]
    return ret


if __name__ == '__main__':
    prices = pd.read_csv('./azure/data/azure_pricing_vm_common.csv')
    roles = pd.read_csv('./azure/data/azure_role_sizes.csv')
    benchs = pd.read_csv('./azure/data/azure_vm_performance.csv')
    
    # Only we need a subset, using us-west region
    prices = prices[prices.region == 'us-west']
    prices['tier_name'] = prices.loc[:, 'description'].apply(tier_name_from_description) 
    # Price parsing
    series_prices = prices['Price'].str.split(' ', expand=True)
    ser_hour = series_prices[0].str.extract(r'\$(?P<price_hr>[\d\.]+)/hr', expand=False)
    ser_month = series_prices[1].str.extract(r'\(~\$(?P<price_mo>[\d,]+)/mo\)', expand=False).str.replace(',', '')
    prices['cost_hour_usd'] = pd.to_numeric(ser_hour)
    prices['cost_month_usd'] = pd.to_numeric(ser_month)
    print ("Prices")
    print (prices.sort_values(by='Instance').head(3))

    print ("Roles")
    roles['role_name'] = roles.loc[:, 'name'].apply(role_name)
    roles['tier_name'] = roles.loc[:, 'name'].apply(tier_name)

    print("Benchmarks")
    benchs['role_name'] = benchs['Instance Type'].str.extract(r'^([\dA-Z]+)', expand=False)

    merged = pd.merge(prices, roles, left_on=['Instance', 'tier_name'], right_on=['role_name', 'tier_name'])
    merged_benchs = pd.merge(merged, benchs, left_on=['role_name'], right_on=['role_name'], how='inner')
    
    print ("Merged")
    print (merged_benchs.head(3))

    merged.to_csv('./azure/data/azure_role_pricing.csv', encoding='utf-8', index=None)
    merged_benchs.to_csv('./azure/data/azure_role_pricing_bench.csv', encoding='utf-8', index=None)
