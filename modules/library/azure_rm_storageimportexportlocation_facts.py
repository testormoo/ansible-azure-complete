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
module: azure_rm_storageimportexportlocation_facts
version_added: "2.8"
short_description: Get Azure Location facts.
description:
    - Get facts of Azure Location.

options:
    name:
        description:
            - The name of the location. For example, West US or westus.
        required: True
    self.config.accept_language:
        description:
            - Specifies the preferred language for the response.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Location
    azure_rm_storageimportexportlocation_facts:
      name: location_name
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
locations:
    description: A list of dictionaries containing facts for Location.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Specifies the resource identifier of the location.
            returned: always
            type: str
            sample: /providers/Microsoft.ImportExport/locations/westus
        name:
            description:
                - Specifies the name of the location. Use List Locations to get all supported locations.
            returned: always
            type: str
            sample: West US
        city:
            description:
                - The city name to use when shipping the drives to the Azure data center.
            returned: always
            type: str
            sample: Santa Clara
        phone:
            description:
                - The phone number for the Azure data center.
            returned: always
            type: str
            sample: 408 352 7600
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storageimportexport import StorageImportExport
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLocationsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            self.config.accept_language=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.name = None
        self.self.config.accept_language = None
        super(AzureRMLocationsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorageImportExport,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['locations'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.locations.get(location_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Locations.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'city': d.get('city', None),
            'phone': d.get('phone', None)
        }
        return d


def main():
    AzureRMLocationsFacts()


if __name__ == '__main__':
    main()
