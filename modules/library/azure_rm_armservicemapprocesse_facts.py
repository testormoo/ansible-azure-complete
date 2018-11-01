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
module: azure_rm_armservicemapprocesse_facts
version_added: "2.8"
short_description: Get Azure Processe facts.
description:
    - Get facts of Azure Processe.

options:
    resource_group:
        description:
            - Resource group name within the specified subscriptionId.
        required: True
    workspace_name:
        description:
            - OMS workspace containing the resources of interest.
        required: True
    machine_name:
        description:
            - Machine resource name.
        required: True
    process_name:
        description:
            - Process resource name.
        required: True
    timestamp:
        description:
            - UTC date and time specifying a time instance relative to which to evaluate a resource. When not specified, the service uses DateTime.UtcNow.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Processe
    azure_rm_armservicemapprocesse_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      machine_name: machine_name
      process_name: process_name
      timestamp: timestamp
'''

RETURN = '''
processes:
    description: A list of dictionaries containing facts for Processe.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/A9C800F7-342E-45B7-8EB4-6C9A6F7FE466/resourceGroups/rg-sm/providers/Microsoft.OperationalInsights/workspaces/D6F79F14-E56
                    3-469B-84B5-9286D2803B2F/features/serviceMap/machines/m-36b83664-0822-4fb3-99a3-8332754f3eae/processes/p-bbf99526b8fc5e7ee4f75568958a040
                    d08489160"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: p-bbf99526b8fc5e7ee4f75568958a040d08489160
        kind:
            description:
                - Constant filled by server.
            returned: always
            type: str
            sample: process
        machine:
            description:
                - Machine hosting this process.
            returned: always
            type: complex
            sample: machine
            contains:
                id:
                    description:
                        - Resource URI.
                    returned: always
                    type: str
                    sample: "/subscriptions/A9C800F7-342E-45B7-8EB4-6C9A6F7FE466/resourceGroups/rg-sm/providers/Microsoft.OperationalInsights/workspaces/D6F7
                            9F14-E563-469B-84B5-9286D2803B2F/features/serviceMap/machines/m-36b83664-0822-4fb3-99a3-8332754f3eae"
                type:
                    description:
                        - Resource type qualifier.
                    returned: always
                    type: str
                    sample: Microsoft.OperationalInsights/workspaces/features/machines
                name:
                    description:
                        - Resource name.
                    returned: always
                    type: str
                    sample: m-36b83664-0822-4fb3-99a3-8332754f3eae
                kind:
                    description:
                        - Constant filled by server.
                    returned: always
                    type: str
                    sample: "ref:machine"
        role:
            description:
                - "The inferred role of this process based on its name, command line, etc. Possible values include: 'webServer', 'appServer',
                   'databaseServer', 'ldapServer', 'smbServer'"
            returned: always
            type: str
            sample: webServer
        group:
            description:
                - The name of the product or suite of the process. The group is determined by its executable name, command line, etc.
            returned: always
            type: str
            sample: Foo-bar Suite
        details:
            description:
                - Process metadata (command line, product name, etc.).
            returned: always
            type: complex
            sample: details
            contains:
                description:
                    description:
                        - Process description.
                    returned: always
                    type: str
                    sample: A special process
        user:
            description:
                - Information about the account under which the process is executing.
            returned: always
            type: complex
            sample: user
            contains:
        hosting:
            description:
                - Information about the hosting environment
            returned: always
            type: complex
            sample: hosting
            contains:
                provider:
                    description:
                        - "The hosting provider of the VM. Possible values include: 'azure'"
                    returned: always
                    type: str
                    sample: azure
                kind:
                    description:
                        - Constant filled by server.
                    returned: always
                    type: str
                    sample: "provider:azure"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.armservicemap import ServiceMap
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProcessesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workspace_name=dict(
                type='str',
                required=True
            ),
            machine_name=dict(
                type='str',
                required=True
            ),
            process_name=dict(
                type='str',
                required=True
            ),
            timestamp=dict(
                type='datetime'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.workspace_name = None
        self.machine_name = None
        self.process_name = None
        self.timestamp = None
        super(AzureRMProcessesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceMap,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['processes'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.processes.get(resource_group_name=self.resource_group,
                                                      workspace_name=self.workspace_name,
                                                      machine_name=self.machine_name,
                                                      process_name=self.process_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Processes.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'kind': d.get('kind', None),
            'machine': {
                'id': d.get('machine', {}).get('id', None),
                'type': d.get('machine', {}).get('type', None),
                'name': d.get('machine', {}).get('name', None),
                'kind': d.get('machine', {}).get('kind', None)
            },
            'role': d.get('role', None),
            'group': d.get('group', None),
            'details': {
                'description': d.get('details', {}).get('description', None)
            },
            'user': {
            },
            'hosting': {
                'provider': d.get('hosting', {}).get('provider', None),
                'kind': d.get('hosting', {}).get('kind', None)
            }
        }
        return d


def main():
    AzureRMProcessesFacts()


if __name__ == '__main__':
    main()
