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
module: azure_rm_apimanagementdiagnosticlogger_facts
version_added: "2.8"
short_description: Get Azure Diagnostic Logger facts.
description:
    - Get facts of Azure Diagnostic Logger.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    diagnostic_id:
        description:
            - Diagnostic identifier. Must be unique in the current API Management service instance.
        required: True
    filter:
        description:
            - | Field       | Supported operators    | Supported functions               |
            - |-------------|------------------------|-----------------------------------|
            - | id          | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | type        | eq                     |                                   |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Diagnostic Logger
    azure_rm_apimanagementdiagnosticlogger_facts:
      resource_group: resource_group_name
      name: service_name
      diagnostic_id: diagnostic_id
      filter: filter
      top: top
      skip: skip
'''

RETURN = '''
diagnostic_logger:
    description: A list of dictionaries containing facts for Diagnostic Logger.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDiagnosticLoggerFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            diagnostic_id=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.diagnostic_id = None
        self.filter = None
        self.top = None
        self.skip = None
        super(AzureRMDiagnosticLoggerFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['diagnostic_logger'] = self.list_by_service()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.diagnostic_logger.list_by_service(resource_group_name=self.resource_group,
                                                                          service_name=self.name,
                                                                          diagnostic_id=self.diagnostic_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Diagnostic Logger.')

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
    AzureRMDiagnosticLoggerFacts()


if __name__ == '__main__':
    main()
