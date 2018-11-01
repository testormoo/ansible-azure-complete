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
module: azure_rm_storsimplemanager
version_added: "2.8"
short_description: Manage Manager instance.
description:
    - Create, update and delete instance of Manager.

options:
    manager:
        description:
            - The manager.
        required: True
        suboptions:
            location:
                description:
                    - The Geo location of the Manager
                required: True
            cis_intrinsic_settings:
                description:
                    - Specifies if the Manager is Garda or Helsinki
                suboptions:
                    type:
                        description:
                            - Refers to the type of the StorSimple Manager.
                        required: True
                        choices:
                            - 'garda_v1'
                            - 'helsinki_v1'
            sku:
                description:
                    - Specifies the Sku
                suboptions:
                    name:
                        description:
                            - "Refers to the sku name which should be 'Standard'"
                        required: True
            etag:
                description:
                    - ETag of the Manager
    resource_group:
        description:
            - The resource group name
        required: True
    manager_name:
        description:
            - The I(manager) name
        required: True
    state:
      description:
        - Assert the state of the Manager.
        - Use 'present' to create or update an Manager and 'absent' to delete it.
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
  - name: Create (or update) Manager
    azure_rm_storsimplemanager:
      manager:
        location: westus
      resource_group: ResourceGroupForSDKTest
      manager_name: hManagerForSDKTest
'''

RETURN = '''
id:
    description:
        - The Resource Id
    returned: always
    type: str
    sample: "/subscriptions/4385cf00-2d3a-425a-832f-f4285b1c9dce/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/Managers/ManagerForSDK
            Test2"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagers(AzureRMModuleBase):
    """Configuration class for an Azure RM Manager resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            manager=dict(
                type='dict',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            manager_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.manager = dict()
        self.resource_group = None
        self.manager_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.manager["location"] = kwargs[key]
                elif key == "cis_intrinsic_settings":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'garda_v1':
                            ev['type'] = 'GardaV1'
                        elif ev['type'] == 'helsinki_v1':
                            ev['type'] = 'HelsinkiV1'
                    self.manager["cis_intrinsic_settings"] = ev
                elif key == "sku":
                    self.manager["sku"] = kwargs[key]
                elif key == "etag":
                    self.manager["etag"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_manager()

        if not old_response:
            self.log("Manager instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Manager instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Manager instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Manager instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_manager()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Manager instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_manager()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_manager():
                time.sleep(20)
        else:
            self.log("Manager instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_manager(self):
        '''
        Creates or updates Manager with the specified configuration.

        :return: deserialized Manager instance state dictionary
        '''
        self.log("Creating / Updating the Manager instance {0}".format(self.manager_name))

        try:
            response = self.mgmt_client.managers.create_or_update(manager=self.manager,
                                                                  resource_group_name=self.resource_group,
                                                                  manager_name=self.manager_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Manager instance.')
            self.fail("Error creating the Manager instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_manager(self):
        '''
        Deletes specified Manager instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Manager instance {0}".format(self.manager_name))
        try:
            response = self.mgmt_client.managers.delete(resource_group_name=self.resource_group,
                                                        manager_name=self.manager_name)
        except CloudError as e:
            self.log('Error attempting to delete the Manager instance.')
            self.fail("Error deleting the Manager instance: {0}".format(str(e)))

        return True

    def get_manager(self):
        '''
        Gets the properties of the specified Manager.

        :return: deserialized Manager instance state dictionary
        '''
        self.log("Checking if the Manager instance {0} is present".format(self.manager_name))
        found = False
        try:
            response = self.mgmt_client.managers.get(resource_group_name=self.resource_group,
                                                     manager_name=self.manager_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Manager instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Manager instance.')
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
    AzureRMManagers()


if __name__ == '__main__':
    main()
