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
module: azure_rm_powerbiembeddedworkspacecollection
version_added: "2.8"
short_description: Manage Workspace Collection instance.
description:
    - Create, update and delete instance of Workspace Collection.

options:
    resource_group:
        description:
            - Azure resource group
        required: True
    workspace_collection_name:
        description:
            - Power BI Embedded Workspace Collection name
        required: True
    location:
        description:
            - Azure location
    state:
      description:
        - Assert the state of the Workspace Collection.
        - Use 'present' to create or update an Workspace Collection and 'absent' to delete it.
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
  - name: Create (or update) Workspace Collection
    azure_rm_powerbiembeddedworkspacecollection:
      resource_group: NOT FOUND
      workspace_collection_name: NOT FOUND
      location: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource id
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.powerbiembedded import PowerBIEmbeddedManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWorkspaceCollections(AzureRMModuleBase):
    """Configuration class for an Azure RM Workspace Collection resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workspace_collection_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.workspace_collection_name = None
        self.location = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWorkspaceCollections, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(PowerBIEmbeddedManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_workspacecollection()

        if not old_response:
            self.log("Workspace Collection instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Workspace Collection instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Workspace Collection instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Workspace Collection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_workspacecollection()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Workspace Collection instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_workspacecollection()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_workspacecollection():
                time.sleep(20)
        else:
            self.log("Workspace Collection instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_workspacecollection(self):
        '''
        Creates or updates Workspace Collection with the specified configuration.

        :return: deserialized Workspace Collection instance state dictionary
        '''
        self.log("Creating / Updating the Workspace Collection instance {0}".format(self.workspace_collection_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.workspace_collections.create(resource_group_name=self.resource_group,
                                                                         workspace_collection_name=self.workspace_collection_name)
            else:
                response = self.mgmt_client.workspace_collections.update(resource_group_name=self.resource_group,
                                                                         workspace_collection_name=self.workspace_collection_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Workspace Collection instance.')
            self.fail("Error creating the Workspace Collection instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_workspacecollection(self):
        '''
        Deletes specified Workspace Collection instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Workspace Collection instance {0}".format(self.workspace_collection_name))
        try:
            response = self.mgmt_client.workspace_collections.delete(resource_group_name=self.resource_group,
                                                                     workspace_collection_name=self.workspace_collection_name)
        except CloudError as e:
            self.log('Error attempting to delete the Workspace Collection instance.')
            self.fail("Error deleting the Workspace Collection instance: {0}".format(str(e)))

        return True

    def get_workspacecollection(self):
        '''
        Gets the properties of the specified Workspace Collection.

        :return: deserialized Workspace Collection instance state dictionary
        '''
        self.log("Checking if the Workspace Collection instance {0} is present".format(self.workspace_collection_name))
        found = False
        try:
            response = self.mgmt_client.workspace_collections.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Workspace Collection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Workspace Collection instance.')
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
    AzureRMWorkspaceCollections()


if __name__ == '__main__':
    main()