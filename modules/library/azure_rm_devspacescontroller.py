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
module: azure_rm_devspacescontroller
version_added: "2.8"
short_description: Manage Controller instance.
description:
    - Create, update and delete instance of Controller.

options:
    resource_group:
        description:
            - Resource group to which the resource belongs.
        required: True
    name:
        description:
            - Name of the resource.
        required: True
    controller:
        description:
            - Controller create parameters.
        required: True
        suboptions:
            location:
                description:
                    - Region where the Azure resource is located.
            host_suffix:
                description:
                    - DNS suffix for public endpoints running in the Azure Dev Spaces Controller.
                    - Required when C(state) is I(present).
            target_container_host_resource_id:
                description:
                    - Resource ID of the target container host
                    - Required when C(state) is I(present).
            target_container_host_credentials_base64:
                description:
                    - Credentials of the target container host (base64).
                    - Required when C(state) is I(present).
            sku:
                description:
                    - Required when C(state) is I(present).
                suboptions:
                    name:
                        description:
                            - The name of the SKU for Azure Dev Spaces Controller.
                            - Required when C(state) is I(present).
                    tier:
                        description:
                            - The tier of the SKU for Azure Dev Spaces Controller.
                        choices:
                            - 'standard'
    state:
      description:
        - Assert the state of the Controller.
        - Use 'present' to create or update an Controller and 'absent' to delete it.
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
  - name: Create (or update) Controller
    azure_rm_devspacescontroller:
      resource_group: myResourceGroup
      name: myControllerResource
      controller:
        location: eastus
        host_suffix: suffix
        target_container_host_resource_id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.ContainerService/managedCluster/myCluster
        target_container_host_credentials_base64: QmFzZTY0IEVuY29kZWQgVmFsdWUK
        sku:
          name: S1
          tier: Standard
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.DevSpaces/controllers/myControllerResource
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.devspaces import DevSpacesManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMControllers(AzureRMModuleBase):
    """Configuration class for an Azure RM Controller resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            controller=dict(
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
        self.name = None
        self.controller = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMControllers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.controller["location"] = kwargs[key]
                elif key == "host_suffix":
                    self.controller["host_suffix"] = kwargs[key]
                elif key == "target_container_host_resource_id":
                    self.controller["target_container_host_resource_id"] = kwargs[key]
                elif key == "target_container_host_credentials_base64":
                    self.controller["target_container_host_credentials_base64"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'tier' in ev:
                        if ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                    self.controller["sku"] = ev

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevSpacesManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_controller()

        if not old_response:
            self.log("Controller instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Controller instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Controller instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_controller()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Controller instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_controller()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_controller():
                time.sleep(20)
        else:
            self.log("Controller instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_controller(self):
        '''
        Creates or updates Controller with the specified configuration.

        :return: deserialized Controller instance state dictionary
        '''
        self.log("Creating / Updating the Controller instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.controllers.create(resource_group_name=self.resource_group,
                                                               name=self.name,
                                                               controller=self.controller)
            else:
                response = self.mgmt_client.controllers.update(resource_group_name=self.resource_group,
                                                               name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Controller instance.')
            self.fail("Error creating the Controller instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_controller(self):
        '''
        Deletes specified Controller instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Controller instance {0}".format(self.name))
        try:
            response = self.mgmt_client.controllers.delete(resource_group_name=self.resource_group,
                                                           name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Controller instance.')
            self.fail("Error deleting the Controller instance: {0}".format(str(e)))

        return True

    def get_controller(self):
        '''
        Gets the properties of the specified Controller.

        :return: deserialized Controller instance state dictionary
        '''
        self.log("Checking if the Controller instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.controllers.get(resource_group_name=self.resource_group,
                                                        name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Controller instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Controller instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def main():
    """Main execution"""
    AzureRMControllers()


if __name__ == '__main__':
    main()
