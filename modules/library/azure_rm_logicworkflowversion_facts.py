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
module: azure_rm_logicworkflowversion_facts
version_added: "2.8"
short_description: Get Azure Workflow Version facts.
description:
    - Get facts of Azure Workflow Version.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    name:
        description:
            - The workflow name.
        required: True
    version_id:
        description:
            - The workflow versionId.
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
  - name: Get instance of Workflow Version
    azure_rm_logicworkflowversion_facts:
      resource_group: resource_group_name
      name: workflow_name
      version_id: version_id
'''

RETURN = '''
workflow_versions:
    description: A list of dictionaries containing facts for Workflow Version.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: id
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: tags
        state:
            description:
                - "The state. Possible values include: 'NotSpecified', 'Completed', 'Enabled', 'Disabled', 'Deleted', 'Suspended'"
            returned: always
            type: str
            sample: state
        version:
            description:
                - Gets the version.
            returned: always
            type: str
            sample: version
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkflowVersionsFacts(AzureRMModuleBase):
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
            version_id=dict(
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
        self.name = None
        self.version_id = None
        self.tags = None
        super(AzureRMWorkflowVersionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['workflow_versions'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workflow_versions.get(resource_group_name=self.resource_group,
                                                              workflow_name=self.name,
                                                              version_id=self.version_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WorkflowVersions.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'tags': d.get('tags', None),
            'state': d.get('state', None),
            'version': d.get('version', None)
        }
        return d


def main():
    AzureRMWorkflowVersionsFacts()


if __name__ == '__main__':
    main()
