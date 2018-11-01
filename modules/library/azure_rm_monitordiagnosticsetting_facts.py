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
module: azure_rm_monitordiagnosticsetting_facts
version_added: "2.8"
short_description: Get Azure Diagnostic Setting facts.
description:
    - Get facts of Azure Diagnostic Setting.

options:
    resource_uri:
        description:
            - The identifier of the resource.
        required: True
    name:
        description:
            - The name of the diagnostic setting.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Diagnostic Setting
    azure_rm_monitordiagnosticsetting_facts:
      resource_uri: resource_uri
      name: name
'''

RETURN = '''
diagnostic_settings:
    description: A list of dictionaries containing facts for Diagnostic Setting.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Azure resource Id
            returned: always
            type: str
            sample: "/subscriptions/1a66ce04-b633-4a0b-b2bc-a912ec8986a6/resourcegroups/viruela1/providers/microsoft.logic/workflows/viruela6/diagnosticSetti
                    ngs/service"
        name:
            description:
                - Azure resource name
            returned: always
            type: str
            sample: mysetting
        metrics:
            description:
                - the list of metric settings.
            returned: always
            type: complex
            sample: metrics
            contains:
        logs:
            description:
                - the list of logs settings.
            returned: always
            type: complex
            sample: logs
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDiagnosticSettingsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_uri=dict(
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
        self.resource_uri = None
        self.name = None
        super(AzureRMDiagnosticSettingsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['diagnostic_settings'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.diagnostic_settings.get(resource_uri=self.resource_uri,
                                                                name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DiagnosticSettings.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'metrics': {
            },
            'logs': {
            }
        }
        return d


def main():
    AzureRMDiagnosticSettingsFacts()


if __name__ == '__main__':
    main()
