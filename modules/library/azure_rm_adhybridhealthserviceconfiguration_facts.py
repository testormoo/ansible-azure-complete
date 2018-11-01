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
module: azure_rm_adhybridhealthserviceconfiguration_facts
version_added: "2.8"
short_description: Get Azure Configuration facts.
description:
    - Get facts of Azure Configuration.

options:

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Configuration
    azure_rm_adhybridhealthserviceconfiguration_facts:
'''

RETURN = '''
configuration:
    description: A list of dictionaries containing facts for Configuration.
    returned: always
    type: complex
    contains:
        disabled:
            description:
                - Indicates if the tenant is disabled in Azure Active Directory Connect Health.
            returned: always
            type: str
            sample: False
        onboarded:
            description:
                - Indicates if the tenant is already onboarded to Azure Active Directory Connect Health.
            returned: always
            type: str
            sample: True
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.adhybridhealthservice import ADHybridHealthService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMConfigurationFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        super(AzureRMConfigurationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ADHybridHealthService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['configuration'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.configuration.get()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Configuration.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'disabled': d.get('disabled', None),
            'onboarded': d.get('onboarded', None)
        }
        return d


def main():
    AzureRMConfigurationFacts()


if __name__ == '__main__':
    main()