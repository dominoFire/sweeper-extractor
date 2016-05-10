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
    prices = pd.read_csv('./data/azure_pricing_vm_common.csv')
    roles = pd.read_csv('./data/azure_role_sizes.csv')
    
    # Only we need a subset, using us-west region
    prices = prices[prices.region == 'us-west']
    prices['tier_name'] = prices.loc[:, 'description'].apply(tier_name_from_description) 
    # Price parsing
    series_prices = prices['Price'].str.split(' ', expand=True)
    ser_hour = series_prices[0].str.extract(r'\$(?P<price_hr>[\d\.]+)/hr')
    ser_month = series_prices[1].str.extract(r'\(~\$(?P<price_mo>[\d,]+)/mo\)').str.replace(',', '')
    prices['cost_hour_usd'] = pd.to_numeric(ser_hour)
    prices['cost_month_usd'] = pd.to_numeric(ser_month)
    print ("Prices")
    print (prices.sort_values(by='Instance').head(3))

    roles['role_name'] = roles.loc[:, 'name'].apply(role_name)
    roles['tier_name'] = roles.loc[:, 'name'].apply(tier_name)
    print ("Roles")    
    print (roles.sort_values(by='role_name').head(3))

    merged = pd.merge(prices, roles, left_on=['Instance', 'tier_name'], right_on=['role_name', 'tier_name'])

    print ("Merged")
    print (merged.head(3))

    merged.to_csv('./data/azure_role_pricing.csv', encoding='utf-8', index=None)
