#!/usr/bin/env python3

import pandas as pd
import requests
import json


if __name__ == '__main__':
	role_benchs = pd.read_csv('./azure/data/azure_role_pricing_bench.csv')

	role_benchs['spec_estimate'] = role_benchs['SPECint [estimate]']
	role_benchs['provider'] = 'azure'

	azure_data = role_benchs.loc[:,['name', 'provider', 'cores', 'memory_in_mb', 'cost_hour_usd', 'spec_estimate']]

	azure_data.to_json('./azure/data/configs.json', orient='records')
