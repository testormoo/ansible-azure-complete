#!/usr/bin/python
#
# Copyright (c) 2018 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_storageblobcontainer_facts
version_added: "2.8"
short_description: Get Azure Blob Container facts.
description:
    - Get facts of Azure Blob Container.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    account_name:
        description:
            - "The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and
               use numbers and lower-case letters only."
        required: True
    container_name:
        description:
            - "The name of the blob container within the specified storage account. Blob container names must be between 3 and 63 characters in length and
               use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number."
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Blob Container
    azure_rm_storageblobcontainer_facts:
      resource_group: resource_group_name
      account_name: account_name
      container_name: container_name
'''

RETURN = '''
blob_containers:
    description: A list of dictionaries containing facts for Blob Container.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/{subscription-id}/resourceGroups/res9871/providers/Microsoft.Storage/storageAccounts/sto6217/blobServices/default/contain
                    ers/container1634"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: container1634
        etag:
            description:
                - Resource Etag.
            returned: always
            type: str
            sample: "'0x8D592D74CC20EBA'"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storage import StorageManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBlobContainersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            container_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.account_name = None
        self.container_name = None
        super(AzureRMBlobContainersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorageManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['blob_containers'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.blob_containers.get(resource_group_name=self.resource_group,
                                                            account_name=self.account_name,
                                                            container_name=self.container_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for BlobContainers.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMBlobContainersFacts()


if __name__ == '__main__':
    main()
