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
module: azure_rm_mediaservice
version_added: "2.8"
short_description: Manage Mediaservice instance.
description:
    - Create, update and delete instance of Mediaservice.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    storage_accounts:
        description:
            - The storage accounts for this resource.
        type: list
        suboptions:
            id:
                description:
                    - "The ID of the storage account resource. Media Services relies on tables and queues as well as blobs, so the C(primary) storage
                       account must be a Standard Storage account (either Microsoft.ClassicStorage or Microsoft.Storage). Blob only storage accounts can be
                       added as C(secondary) storage accounts."
            type:
                description:
                    - The type of the storage account.
                required: True
                choices:
                    - 'primary'
                    - 'secondary'
    state:
      description:
        - Assert the state of the Mediaservice.
        - Use 'present' to create or update an Mediaservice and 'absent' to delete it.
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
  - name: Create (or update) Mediaservice
    azure_rm_mediaservice:
      resource_group: contoso
      account_name: contososports
      location: eastus
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso/providers/Microsoft.Media/mediaservices/contososports
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMMediaservices(AzureRMModuleBase):
    """Configuration class for an Azure RM Mediaservice resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            storage_accounts=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMMediaservices, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "storage_accounts":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'primary':
                            ev['type'] = 'Primary'
                        elif ev['type'] == 'secondary':
                            ev['type'] = 'Secondary'
                    self.parameters["storage_accounts"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_mediaservice()

        if not old_response:
            self.log("Mediaservice instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Mediaservice instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Mediaservice instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Mediaservice instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_mediaservice()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Mediaservice instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_mediaservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_mediaservice():
                time.sleep(20)
        else:
            self.log("Mediaservice instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_mediaservice(self):
        '''
        Creates or updates Mediaservice with the specified configuration.

        :return: deserialized Mediaservice instance state dictionary
        '''
        self.log("Creating / Updating the Mediaservice instance {0}".format(self.account_name))

        try:
            response = self.mgmt_client.mediaservices.create_or_update(resource_group_name=self.resource_group,
                                                                       account_name=self.account_name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Mediaservice instance.')
            self.fail("Error creating the Mediaservice instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_mediaservice(self):
        '''
        Deletes specified Mediaservice instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Mediaservice instance {0}".format(self.account_name))
        try:
            response = self.mgmt_client.mediaservices.delete(resource_group_name=self.resource_group,
                                                             account_name=self.account_name)
        except CloudError as e:
            self.log('Error attempting to delete the Mediaservice instance.')
            self.fail("Error deleting the Mediaservice instance: {0}".format(str(e)))

        return True

    def get_mediaservice(self):
        '''
        Gets the properties of the specified Mediaservice.

        :return: deserialized Mediaservice instance state dictionary
        '''
        self.log("Checking if the Mediaservice instance {0} is present".format(self.account_name))
        found = False
        try:
            response = self.mgmt_client.mediaservices.get(resource_group_name=self.resource_group,
                                                          account_name=self.account_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Mediaservice instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Mediaservice instance.')
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
    AzureRMMediaservices()


if __name__ == '__main__':
    main()
