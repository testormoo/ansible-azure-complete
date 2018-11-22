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
module: azure_rm_storagesyncworkflow_facts
version_added: "2.8"
short_description: Get Azure Workflow facts.
description:
    - Get facts of Azure Workflow.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    name:
        description:
            - Name of Storage Sync Service resource.
        required: True
    workflow_id:
        description:
            - workflow Id

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Workflow
    azure_rm_storagesyncworkflow_facts:
      resource_group: resource_group_name
      name: storage_sync_service_name
      workflow_id: workflow_id

  - name: List instances of Workflow
    azure_rm_storagesyncworkflow_facts:
      resource_group: resource_group_name
      name: storage_sync_service_name
'''

RETURN = '''
workflows:
    description: A list of dictionaries containing facts for Workflow.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/3a048283-338f-4002-a9dd-a50fdadcb392/resourceGroups/SampleResourceGroup_1/providers/Microsoft.StorageSync/storageSyncServ
                    ices/SampleStorageSyncService_1/workflows/828219ea-083e-48b5-89ea-8fd9991b2e75"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: 828219ea-083e-48b5-89ea-8fd9991b2e75
        status:
            description:
                - "workflow status. Possible values include: 'active', 'expired', 'succeeded', 'aborted', 'failed'"
            returned: always
            type: str
            sample: succeeded
        operation:
            description:
                - "operation direction. Possible values include: 'do', 'undo', 'cancel'"
            returned: always
            type: str
            sample: do
        steps:
            description:
                - workflow steps
            returned: always
            type: str
            sample: "[{'name':'validateInput','friendlyName':'validateInput','status':'Succeeded','error':null},{'name':'newServerEndpoint','friendlyName':'n
                    ewServerEndpoint','status':'Succeeded','error':null},{'name':'updateReplicaGroupCertificates','friendlyName':'updateReplicaGroupCertific
                    ates','status':'Succeeded','error':null},{'name':'runServerJob','friendlyName':'runServerJob','status':'Succeeded','error':null}]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storagesync import StorageSyncManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkflowFacts(AzureRMModuleBase):
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
            workflow_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.workflow_id = None
        super(AzureRMWorkflowFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.workflow_id is not None:
            self.results['workflows'] = self.get()
        else:
            self.results['workflows'] = self.list_by_storage_sync_service()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workflows.get(resource_group_name=self.resource_group,
                                                      storage_sync_service_name=self.name,
                                                      workflow_id=self.workflow_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workflow.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_storage_sync_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workflows.list_by_storage_sync_service(resource_group_name=self.resource_group,
                                                                               storage_sync_service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workflow.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'status': d.get('status', None),
            'operation': d.get('operation', None),
            'steps': d.get('steps', None)
        }
        return d


def main():
    AzureRMWorkflowFacts()


if __name__ == '__main__':
    main()
