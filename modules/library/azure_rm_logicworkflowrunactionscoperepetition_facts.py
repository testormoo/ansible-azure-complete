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
module: azure_rm_logicworkflowrunactionscoperepetition_facts
version_added: "2.8"
short_description: Get Azure Workflow Run Action Scope Repetition facts.
description:
    - Get facts of Azure Workflow Run Action Scope Repetition.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    workflow_name:
        description:
            - The workflow name.
        required: True
    run_name:
        description:
            - The workflow run name.
        required: True
    action_name:
        description:
            - The workflow action name.
        required: True
    name:
        description:
            - The workflow repetition.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Workflow Run Action Scope Repetition
    azure_rm_logicworkflowrunactionscoperepetition_facts:
      resource_group: resource_group_name
      workflow_name: workflow_name
      run_name: run_name
      action_name: action_name
      name: repetition_name
'''

RETURN = '''
workflow_run_action_scope_repetitions:
    description: A list of dictionaries containing facts for Workflow Run Action Scope Repetition.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/workflows/testFlow/runs/0
                    8586776228332053161046300351/actions/for_each/scopeRepetitions/000000"
        name:
            description:
                - Gets the resource name.
            returned: always
            type: str
            sample: 000000
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: tags
        correlation:
            description:
                - The correlation properties.
            returned: always
            type: complex
            sample: correlation
            contains:
        status:
            description:
                - "The status of the workflow scope repetition. Possible values include: 'NotSpecified', 'Paused', 'Running', 'Waiting', 'Succeeded',
                   'Skipped', 'Suspended', 'Cancelled', 'Failed', 'Faulted', 'TimedOut', 'Aborted', 'Ignored'"
            returned: always
            type: str
            sample: Succeeded
        code:
            description:
                - The workflow scope repetition code.
            returned: always
            type: str
            sample: NotSpecified
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkflowRunActionScopeRepetitionFacts(AzureRMModuleBase):
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
            run_name=dict(
                type='str',
                required=True
            ),
            action_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.workflow_name = None
        self.run_name = None
        self.action_name = None
        self.name = None
        self.tags = None
        super(AzureRMWorkflowRunActionScopeRepetitionFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['workflow_run_action_scope_repetitions'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workflow_run_action_scope_repetitions.get(resource_group_name=self.resource_group,
                                                                                  workflow_name=self.workflow_name,
                                                                                  run_name=self.run_name,
                                                                                  action_name=self.action_name,
                                                                                  repetition_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workflow Run Action Scope Repetition.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'correlation': {
            },
            'status': d.get('status', None),
            'code': d.get('code', None)
        }
        return d


def main():
    AzureRMWorkflowRunActionScopeRepetitionFacts()


if __name__ == '__main__':
    main()
