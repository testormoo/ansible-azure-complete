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
module: azure_rm_logicworkflowrun_facts
version_added: "2.8"
short_description: Get Azure Workflow Run facts.
description:
    - Get facts of Azure Workflow Run.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    workflow_name:
        description:
            - The workflow name.
        required: True
    name:
        description:
            - The workflow run name.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Workflow Run
    azure_rm_logicworkflowrun_facts:
      resource_group: resource_group_name
      workflow_name: workflow_name
      name: run_name
'''

RETURN = '''
workflow_runs:
    description: A list of dictionaries containing facts for Workflow Run.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: id
        status:
            description:
                - "Gets the status. Possible values include: 'NotSpecified', 'Paused', 'Running', 'Waiting', 'Succeeded', 'Skipped', 'Suspended',
                   'Cancelled', 'Failed', 'Faulted', 'TimedOut', 'Aborted', 'Ignored'"
            returned: always
            type: str
            sample: status
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkflowRunFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workflow_name=dict(
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
        self.resource_group = None
        self.workflow_name = None
        self.name = None
        super(AzureRMWorkflowRunFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['workflow_runs'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workflow_runs.get(resource_group_name=self.resource_group,
                                                          workflow_name=self.workflow_name,
                                                          run_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workflow Run.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMWorkflowRunFacts()


if __name__ == '__main__':
    main()
