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
module: azure_rm_adhybridhealthserviceaddsservice_facts
version_added: "2.8"
short_description: Get Azure Adds Service facts.
description:
    - Get facts of Azure Adds Service.

options:
    name:
        description:
            - The name of the service.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Adds Service
    azure_rm_adhybridhealthserviceaddsservice_facts:
      name: service_name
'''

RETURN = '''
adds_services:
    description: A list of dictionaries containing facts for Adds Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The id of the service.
            returned: always
            type: str
            sample: ServiceId
        disabled:
            description:
                - Indicates if the service is disabled or not.
            returned: always
            type: str
            sample: False
        health:
            description:
                - The health of the service.
            returned: always
            type: str
            sample: Healthy
        signature:
            description:
                - The signature of the service.
            returned: always
            type: str
            sample: SampleSignature
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.adhybridhealthservice import ADHybridHealthService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAddsServicesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.name = None
        super(AzureRMAddsServicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ADHybridHealthService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['adds_services'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.adds_services.get(service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AddsServices.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'disabled': d.get('disabled', None),
            'health': d.get('health', None),
            'signature': d.get('signature', None)
        }
        return d


def main():
    AzureRMAddsServicesFacts()


if __name__ == '__main__':
    main()
