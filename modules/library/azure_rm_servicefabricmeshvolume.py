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
module: azure_rm_servicefabricmeshvolume
version_added: "2.8"
short_description: Manage Volume instance.
description:
    - Create, update and delete instance of Volume.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    volume_resource_name:
        description:
            - The identity of the volume.
        required: True
    volume_resource_description:
        description:
            - Description for creating a Volume resource.
        required: True
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                required: True
            description:
                description:
                    - User readable description of the volume.
            provider:
                description:
                    - Provider of the volume.
                required: True
            azure_file_parameters:
                description:
                    - This type describes a volume provided by an Azure Files file share.
                suboptions:
                    account_name:
                        description:
                            - Name of the Azure storage account for the File Share.
                        required: True
                    account_key:
                        description:
                            - Access key of the Azure storage account for the File Share.
                    share_name:
                        description:
                            - Name of the Azure Files file share that provides storage for the volume.
                        required: True
    state:
      description:
        - Assert the state of the Volume.
        - Use 'present' to create or update an Volume and 'absent' to delete it.
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
  - name: Create (or update) Volume
    azure_rm_servicefabricmeshvolume:
      resource_group: sbz_demo
      volume_resource_name: sampleVolume
      volume_resource_description:
        location: EastUS
'''

RETURN = '''
id:
    description:
        - "Fully qualified identifier for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/volumes/sampleVolume
status:
    description:
        - "Status of the volume. Possible values include: 'Unknown', 'Ready', 'Upgrading', 'Creating', 'Deleting', 'Failed'"
    returned: always
    type: str
    sample: Ready
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.servicefabricmesh import ServiceFabricMeshManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVolume(AzureRMModuleBase):
    """Configuration class for an Azure RM Volume resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            volume_resource_name=dict(
                type='str',
                required=True
            ),
            volume_resource_description=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.volume_resource_name = None
        self.volume_resource_description = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVolume, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.volume_resource_description["location"] = kwargs[key]
                elif key == "description":
                    self.volume_resource_description["description"] = kwargs[key]
                elif key == "provider":
                    self.volume_resource_description["provider"] = kwargs[key]
                elif key == "azure_file_parameters":
                    self.volume_resource_description["azure_file_parameters"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_volume()

        if not old_response:
            self.log("Volume instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Volume instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Volume instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Volume instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_volume()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Volume instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_volume()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_volume():
                time.sleep(20)
        else:
            self.log("Volume instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_volume(self):
        '''
        Creates or updates Volume with the specified configuration.

        :return: deserialized Volume instance state dictionary
        '''
        self.log("Creating / Updating the Volume instance {0}".format(self.volume_resource_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.volume.create(resource_group_name=self.resource_group,
                                                          volume_resource_name=self.volume_resource_name,
                                                          volume_resource_description=self.volume_resource_description)
            else:
                response = self.mgmt_client.volume.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Volume instance.')
            self.fail("Error creating the Volume instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_volume(self):
        '''
        Deletes specified Volume instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Volume instance {0}".format(self.volume_resource_name))
        try:
            response = self.mgmt_client.volume.delete(resource_group_name=self.resource_group,
                                                      volume_resource_name=self.volume_resource_name)
        except CloudError as e:
            self.log('Error attempting to delete the Volume instance.')
            self.fail("Error deleting the Volume instance: {0}".format(str(e)))

        return True

    def get_volume(self):
        '''
        Gets the properties of the specified Volume.

        :return: deserialized Volume instance state dictionary
        '''
        self.log("Checking if the Volume instance {0} is present".format(self.volume_resource_name))
        found = False
        try:
            response = self.mgmt_client.volume.get(resource_group_name=self.resource_group,
                                                   volume_resource_name=self.volume_resource_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Volume instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Volume instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMVolume()


if __name__ == '__main__':
    main()
