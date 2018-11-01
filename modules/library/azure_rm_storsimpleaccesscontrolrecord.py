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
module: azure_rm_storsimpleaccesscontrolrecord
version_added: "2.8"
short_description: Manage Access Control Record instance.
description:
    - Create, update and delete instance of Access Control Record.

options:
    access_control_record_name:
        description:
            - The name of the access control record.
        required: True
    access_control_record:
        description:
            - The access control record to be added or updated.
        required: True
        suboptions:
            initiator_name:
                description:
                    - The Iscsi initiator name (IQN)
                required: True
    resource_group:
        description:
            - The resource group name
        required: True
    manager_name:
        description:
            - The manager name
        required: True
    state:
      description:
        - Assert the state of the Access Control Record.
        - Use 'present' to create or update an Access Control Record and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Access Control Record
    azure_rm_storsimpleaccesscontrolrecord:
      access_control_record_name: AcrForSDKTest
      resource_group: ResourceGroupForSDKTest
      manager_name: hAzureSDKOperations
'''

RETURN = '''
id:
    description:
        - The identifier.
    returned: always
    type: str
    sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzureSDKOper
            ations/accessControlRecords/AcrForSDKTest"
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


class AzureRMAccessControlRecords(AzureRMModuleBase):
    """Configuration class for an Azure RM Access Control Record resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            access_control_record_name=dict(
                type='str',
                required=True
            ),
            access_control_record=dict(
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

        self.access_control_record_name = None
        self.access_control_record = dict()
        self.resource_group = None
        self.manager_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAccessControlRecords, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "initiator_name":
                    self.access_control_record["initiator_name"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_accesscontrolrecord()

        if not old_response:
            self.log("Access Control Record instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Access Control Record instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Access Control Record instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Access Control Record instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_accesscontrolrecord()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Access Control Record instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_accesscontrolrecord()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_accesscontrolrecord():
                time.sleep(20)
        else:
            self.log("Access Control Record instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_accesscontrolrecord(self):
        '''
        Creates or updates Access Control Record with the specified configuration.

        :return: deserialized Access Control Record instance state dictionary
        '''
        self.log("Creating / Updating the Access Control Record instance {0}".format(self.manager_name))

        try:
            response = self.mgmt_client.access_control_records.create_or_update(access_control_record_name=self.access_control_record_name,
                                                                                access_control_record=self.access_control_record,
                                                                                resource_group_name=self.resource_group,
                                                                                manager_name=self.manager_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Access Control Record instance.')
            self.fail("Error creating the Access Control Record instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_accesscontrolrecord(self):
        '''
        Deletes specified Access Control Record instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Access Control Record instance {0}".format(self.manager_name))
        try:
            response = self.mgmt_client.access_control_records.delete(access_control_record_name=self.access_control_record_name,
                                                                      resource_group_name=self.resource_group,
                                                                      manager_name=self.manager_name)
        except CloudError as e:
            self.log('Error attempting to delete the Access Control Record instance.')
            self.fail("Error deleting the Access Control Record instance: {0}".format(str(e)))

        return True

    def get_accesscontrolrecord(self):
        '''
        Gets the properties of the specified Access Control Record.

        :return: deserialized Access Control Record instance state dictionary
        '''
        self.log("Checking if the Access Control Record instance {0} is present".format(self.manager_name))
        found = False
        try:
            response = self.mgmt_client.access_control_records.get(access_control_record_name=self.access_control_record_name,
                                                                   resource_group_name=self.resource_group,
                                                                   manager_name=self.manager_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Access Control Record instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Access Control Record instance.')
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
    AzureRMAccessControlRecords()


if __name__ == '__main__':
    main()
