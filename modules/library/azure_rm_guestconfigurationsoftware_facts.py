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
module: azure_rm_guestconfigurationsoftware_facts
version_added: "2.8"
short_description: Get Azure Software facts.
description:
    - Get facts of Azure Software.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    vm_name:
        description:
            - The name of the virtual machine.
        required: True
    software_id:
        description:
            - The software Id.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Software
    azure_rm_guestconfigurationsoftware_facts:
      resource_group: resource_group_name
      vm_name: vm_name
      software_id: software_id
'''

RETURN = '''
software:
    description: A list of dictionaries containing facts for Software.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.guestconfiguration import GuestConfigurationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSoftwareFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vm_name=dict(
                type='str',
                required=True
            ),
            software_id=dict(
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
        self.vm_name = None
        self.software_id = None
        super(AzureRMSoftwareFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(GuestConfigurationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['software'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.software.get(resource_group_name=self.resource_group,
                                                     vm_name=self.vm_name,
                                                     software_id=self.software_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Software.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMSoftwareFacts()


if __name__ == '__main__':
    main()
