import os
import pandas as pd
from sweeper.cloud.azure import AzureCloudProvider

def process_sms_list(result_list, csv_filename):
    result_elements = [o.__dict__ for o in result_list]
    df = pd.DataFrame(result_elements)
    df.to_csv(csv_filename, encoding='utf-8', index=False)
    return df


if __name__ == '__main__':
    subscription_id = '8ea1a328-9162-4a6e-9cdc-fcc8d6766608'
    pem_file = 'mycert.pem'
    cloud_provider = AzureCloudProvider(subscription_id, pem_file)
    sms = cloud_provider.sms

    if not os.path.exists('./data'):
        os.mkdir('./data')

    result = sms.list_os_images()
    process_sms_list(result.images, './data/azure_os_images.csv')
    print ('Azure OS images saved in azure_os_images.csv')

    result = sms.list_vm_images()
    process_sms_list(result.vm_images, './data/azure_vm_images.csv')
    print ('Azure VM images saved in azure_vm_images.csv')

    result = sms.list_role_sizes()
    process_sms_list(result.role_sizes, './data/azure_role_sizes.csv')
    print ('Azure Role sizes saved in azure_role_sizes.csv')

    result = sms.list_locations()
    process_sms_list(result.locations, './data/azure_locations.csv')
    print ('Azure Locations saved in azure_locations.csv')

    result = sms.list_storage_accounts()
    process_sms_list(result.storage_services, './data/azure_storage_accounts.csv')
    print ('Azure Storage accounts saved in azure_storage_accounts.csv')

    # Put this result always next to for loop!
    result = sms.list_hosted_services()
    process_sms_list(result.hosted_services, './data/azure_hosted_services.csv')
    print ('Azure Hosted services saved in azure_hosted_services.csv')

    for hs in result.hosted_services:
        subr = sms.list_service_certificates(hs.service_name)
        process_sms_list(subr.certificates, './data/azure_service_certificates-{0}.csv'.format(hs.service_name))
        print(('Azure Service certificates for {0} saved in azure_service_certificates-{0}.csv'.format(hs.service_name)))

        if hs.deployments:
            process_sms_list(hs.deployments, 'data/azure_service_deployments-{0}.csv'.format(hs.service_name))
            print(('Azure Service deployments for {0} saved in azure_service_deployments-{0}.csv'.format(hs.service_name)))
