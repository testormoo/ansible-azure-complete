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
module: azure_rm_datamigrationtask_facts
version_added: "2.8"
short_description: Get Azure Task facts.
description:
    - Get facts of Azure Task.

options:
    expand:
        description:
            - Expand the response
    group_name:
        description:
            - Name of the resource group
        required: True
    service_name:
        description:
            - Name of the service
        required: True
    project_name:
        description:
            - Name of the project
        required: True
    task_name:
        description:
            - Name of the Task
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Task
    azure_rm_datamigrationtask_facts:
      expand: expand
      group_name: group_name
      service_name: service_name
      project_name: project_name
      task_name: task_name
'''

RETURN = '''
tasks:
    description: A list of dictionaries containing facts for Task.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/fc04246f-04c5-437e-ac5e-206a19e7193f/resourceGroups/DmsSdkRg/providers/Microsoft.DataMigration/services/DmsSdkService/pro
                    jects/DmsSdkProject/tasks/DmsSdkTask"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: DmsSdkTask
        etag:
            description:
                - HTTP strong entity tag value. This is ignored if submitted.
            returned: always
            type: str
            sample: 0vPYxzfnDaDH9yhOJAnqTyTRpa09Kb7pm+LEukDBbw8=
        properties:
            description:
                - Custom task properties
            returned: always
            type: complex
            sample: properties
            contains:
                state:
                    description:
                        - "The state of the task. This is ignored if submitted. Possible values include: 'Unknown', 'Queued', 'Running', 'Canceled',
                           'Succeeded', 'Failed', 'FailedInputValidation', 'Faulted'"
                    returned: always
                    type: str
                    sample: Queued
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datamigration import DataMigrationServiceClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTasksFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            expand=dict(
                type='str'
            ),
            group_name=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            project_name=dict(
                type='str',
                required=True
            ),
            task_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.expand = None
        self.group_name = None
        self.service_name = None
        self.project_name = None
        self.task_name = None
        super(AzureRMTasksFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataMigrationServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['tasks'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tasks.get(group_name=self.group_name,
                                                  service_name=self.service_name,
                                                  project_name=self.project_name,
                                                  task_name=self.task_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tasks.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None),
            'properties': {
                'state': d.get('properties', {}).get('state', None)
            }
        }
        return d


def main():
    AzureRMTasksFacts()


if __name__ == '__main__':
    main()
