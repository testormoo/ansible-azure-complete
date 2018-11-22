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
module: azure_rm_logicworkflowrunoperation_facts
version_added: "2.8"
short_description: Get Azure Workflow Run Operation facts.
description:
    - Get facts of Azure Workflow Run Operation.

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
    operation_id:
        description:
            - The workflow operation id.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Workflow Run Operation
    azure_rm_logicworkflowrunoperation_facts:
      resource_group: resource_group_name
      workflow_name: workflow_name
      name: run_name
      operation_id: operation_id
'''

RETURN = '''
workflow_run_operations:
    description: A list of dictionaries containing facts for Workflow Run Operation.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/workflows/testFlow/runs/0
                    8586774142730039209110422528"
        status:
            description:
                - "Gets the status. Possible values include: 'NotSpecified', 'Paused', 'Running', 'Waiting', 'Succeeded', 'Skipped', 'Suspended',
                   'Cancelled', 'Failed', 'Faulted', 'TimedOut', 'Aborted', 'Ignored'"
            returned: always
            type: str
            sample: Succeeded
        correlation:
            description:
                - The run correlation.
            returned: always
            type: complex
            sample: correlation
            contains:
        workflow:
            description:
                - Gets the reference to workflow version.
            returned: always
            type: complex
            sample: workflow
            contains:
                id:
                    description:
                        - The resource id.
                    returned: always
                    type: str
                    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/workflows/testFlo
                            w/versions/08586993867806980512"
                name:
                    description:
                        - Gets the resource name.
                    returned: always
                    type: str
                    sample: 08586993867806980512
                type:
                    description:
                        - Gets the resource type.
                    returned: always
                    type: str
                    sample: Microsoft.Logic/workflows/versions
        trigger:
            description:
                - Gets the fired trigger.
            returned: always
            type: complex
            sample: trigger
            contains:
                name:
                    description:
                        - Gets the name.
                    returned: always
                    type: str
                    sample: Recurrence
                correlation:
                    description:
                        - The run correlation.
                    returned: always
                    type: complex
                    sample: correlation
                    contains:
                code:
                    description:
                        - Gets the code.
                    returned: always
                    type: str
                    sample: OK
                status:
                    description:
                        - "Gets the status. Possible values include: 'NotSpecified', 'Paused', 'Running', 'Waiting', 'Succeeded', 'Skipped', 'Suspended',
                           'Cancelled', 'Failed', 'Faulted', 'TimedOut', 'Aborted', 'Ignored'"
                    returned: always
                    type: str
                    sample: Succeeded
        outputs:
            description:
                - Gets the outputs.
            returned: always
            type: complex
            sample: {}
        name:
            description:
                - Gets the workflow run name.
            returned: always
            type: str
            sample: 08586774142730039209110422528
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkflowRunOperationFacts(AzureRMModuleBase):
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
            ),
            operation_id=dict(
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
        self.operation_id = None
        super(AzureRMWorkflowRunOperationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['workflow_run_operations'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workflow_run_operations.get(resource_group_name=self.resource_group,
                                                                    workflow_name=self.workflow_name,
                                                                    run_name=self.name,
                                                                    operation_id=self.operation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workflow Run Operation.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'status': d.get('status', None),
            'correlation': {
            },
            'workflow': {
                'id': d.get('workflow', {}).get('id', None),
                'name': d.get('workflow', {}).get('name', None),
                'type': d.get('workflow', {}).get('type', None)
            },
            'trigger': {
                'name': d.get('trigger', {}).get('name', None),
                'correlation': {
                },
                'code': d.get('trigger', {}).get('code', None),
                'status': d.get('trigger', {}).get('status', None)
            },
            'outputs': d.get('outputs', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMWorkflowRunOperationFacts()


if __name__ == '__main__':
    main()
