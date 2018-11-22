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
module: azure_rm_adhybridhealthserviceaddsservicesuserpreference_facts
version_added: "2.8"
short_description: Get Azure Adds Services User Preference facts.
description:
    - Get facts of Azure Adds Services User Preference.

options:
    service_name:
        description:
            - The name of the service.
        required: True
    name:
        description:
            - The name of the feature.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Adds Services User Preference
    azure_rm_adhybridhealthserviceaddsservicesuserpreference_facts:
      service_name: service_name
      name: feature_name
'''

RETURN = '''
adds_services_user_preference:
    description: A list of dictionaries containing facts for Adds Services User Preference.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.adhybridhealthservice import ADHybridHealthService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAddsServicesUserPreferenceFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            service_name=dict(
                type='str',
                required=True
            ),
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
        self.service_name = None
        self.name = None
        super(AzureRMAddsServicesUserPreferenceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ADHybridHealthService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['adds_services_user_preference'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.adds_services_user_preference.get(service_name=self.service_name,
                                                                          feature_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Adds Services User Preference.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMAddsServicesUserPreferenceFacts()


if __name__ == '__main__':
    main()
