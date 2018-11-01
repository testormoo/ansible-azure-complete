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
module: azure_rm_loganalyticslinkedservice
version_added: "2.8"
short_description: Manage Linked Service instance.
description:
    - Create, update and delete instance of Linked Service.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
        required: True
    workspace_name:
        description:
            - Name of the Log Analytics Workspace that will contain the linkedServices resource
        required: True
    linked_service_name:
        description:
            - Name of the linkedServices resource
        required: True
    resource_id:
        description:
            - The resource id of the resource that will be linked to the workspace.
        required: True
    state:
      description:
        - Assert the state of the Linked Service.
        - Use 'present' to create or update an Linked Service and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Linked Service
    azure_rm_loganalyticslinkedservice:
      resource_group: mms-eus
      workspace_name: TestLinkWS
      linked_service_name: TestLinkWS/Automation
      resource_id: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-00000000000/resourcegroups/mms-eus/providers/microsoft.operationalinsights/workspaces/testlinkws/linkedse
            rvices/automation"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.loganalytics import OperationalInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMLinkedServices(AzureRMModuleBase):
    """Configuration class for an Azure RM Linked Service resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workspace_name=dict(
                type='str',
                required=True
            ),
            linked_service_name=dict(
                type='str',
                required=True
            ),
            resource_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.workspace_name = None
        self.linked_service_name = None
        self.resource_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLinkedServices, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(OperationalInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_linkedservice()

        if not old_response:
            self.log("Linked Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Linked Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Linked Service instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Linked Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_linkedservice()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Linked Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_linkedservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_linkedservice():
                time.sleep(20)
        else:
            self.log("Linked Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_linkedservice(self):
        '''
        Creates or updates Linked Service with the specified configuration.

        :return: deserialized Linked Service instance state dictionary
        '''
        self.log("Creating / Updating the Linked Service instance {0}".format(self.linked_service_name))

        try:
            response = self.mgmt_client.linked_services.create_or_update(resource_group_name=self.resource_group,
                                                                         workspace_name=self.workspace_name,
                                                                         linked_service_name=self.linked_service_name,
                                                                         resource_id=self.resource_id)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Linked Service instance.')
            self.fail("Error creating the Linked Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_linkedservice(self):
        '''
        Deletes specified Linked Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Linked Service instance {0}".format(self.linked_service_name))
        try:
            response = self.mgmt_client.linked_services.delete(resource_group_name=self.resource_group,
                                                               workspace_name=self.workspace_name,
                                                               linked_service_name=self.linked_service_name)
        except CloudError as e:
            self.log('Error attempting to delete the Linked Service instance.')
            self.fail("Error deleting the Linked Service instance: {0}".format(str(e)))

        return True

    def get_linkedservice(self):
        '''
        Gets the properties of the specified Linked Service.

        :return: deserialized Linked Service instance state dictionary
        '''
        self.log("Checking if the Linked Service instance {0} is present".format(self.linked_service_name))
        found = False
        try:
            response = self.mgmt_client.linked_services.get(resource_group_name=self.resource_group,
                                                            workspace_name=self.workspace_name,
                                                            linked_service_name=self.linked_service_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Linked Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Linked Service instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMLinkedServices()


if __name__ == '__main__':
    main()
