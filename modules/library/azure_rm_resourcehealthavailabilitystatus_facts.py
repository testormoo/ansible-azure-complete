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
module: azure_rm_resourcehealthavailabilitystatus_facts
version_added: "2.8"
short_description: Get Azure Availability Status facts.
description:
    - Get facts of Azure Availability Status.

options:
    resource_group:
        description:
            - The name of the resource group.
    filter:
        description:
            - "The filter to apply on the operation. For more information please see
               https://docs.microsoft.com/en-us/rest/api/apimanagement/apis?redirectedfrom=MSDN"
    expand:
        description:
            - Setting $expand=recommendedactions in url query expands the recommendedactions in the response.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Availability Status
    azure_rm_resourcehealthavailabilitystatus_facts:
      resource_group: resource_group_name
      filter: filter
      expand: expand

  - name: List instances of Availability Status
    azure_rm_resourcehealthavailabilitystatus_facts:
      filter: filter
      expand: expand
'''

RETURN = '''
availability_statuses:
    description: A list of dictionaries containing facts for Availability Status.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.resourcehealth import MicrosoftResourceHealth
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAvailabilityStatusFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
            expand=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.filter = None
        self.expand = None
        super(AzureRMAvailabilityStatusFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MicrosoftResourceHealth,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None:
            self.results['availability_statuses'] = self.list_by_resource_group()
        else:
            self.results['availability_statuses'] = self.list_by_subscription_id()
        return self.results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.availability_statuses.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Availability Status.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_subscription_id(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.availability_statuses.list_by_subscription_id()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Availability Status.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMAvailabilityStatusFacts()


if __name__ == '__main__':
    main()
