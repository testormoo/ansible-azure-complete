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
module: azure_rm_armservicemapmachinegroup
version_added: "2.8"
short_description: Manage Machine Group instance.
description:
    - Create, update and delete instance of Machine Group.

options:
    resource_group:
        description:
            - Resource group name within the specified subscriptionId.
        required: True
    workspace_name:
        description:
            - OMS workspace containing the resources of interest.
        required: True
    machine_group:
        description:
            - Machine Group resource to create.
        required: True
        suboptions:
            etag:
                description:
                    - Resource ETAG.
            kind:
                description:
                    - Constant filled by server.
                required: True
            group_type:
                description:
                    - Type of the machine group.
                choices:
                    - 'unknown'
                    - 'azure-cs'
                    - 'azure-sf'
                    - 'azure-vmss'
                    - 'user-static'
            display_name:
                description:
                    - User defined name for the group
            count:
                description:
                    - "Count of I(machines) in this group. The value of count may be bigger than the number of I(machines) in case of the group has been
                       truncated due to exceeding the max number of I(machines) a group can handle."
            machines:
                description:
                    - "References of the machines in this group. The hints within each reference do not represent the current value of the corresponding
                       fields. They are a snapshot created during the last time the machine group was updated."
                type: list
                suboptions:
                    id:
                        description:
                            - Resource URI.
                        required: True
                    kind:
                        description:
                            - Constant filled by server.
                        required: True
    state:
      description:
        - Assert the state of the Machine Group.
        - Use 'present' to create or update an Machine Group and 'absent' to delete it.
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
  - name: Create (or update) Machine Group
    azure_rm_armservicemapmachinegroup:
      resource_group: rg-sm
      workspace_name: D6F79F14-E563-469B-84B5-9286D2803B2F
      machine_group:
        etag: e20e75b5-5765-48a5-9503-9d1b7fd20925
        kind: machineGroup
'''

RETURN = '''
id:
    description:
        - Resource identifier.
    returned: always
    type: str
    sample: "/subscriptions/63BE4E24-FDF0-4E9C-9342-6A5D5A359722/resourceGroups/rg-sm/providers/Microsoft.OperationalInsights/workspaces/D6F79F14-E563-469B-8
            4B5-9286D2803B2F/machineGroups/ccfbf4bf-dc08-4371-9e9b-00a8d875d45a"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.armservicemap import ServiceMap
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMMachineGroups(AzureRMModuleBase):
    """Configuration class for an Azure RM Machine Group resource"""

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
            machine_group=dict(
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
        self.workspace_name = None
        self.machine_group = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMMachineGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "etag":
                    self.machine_group["etag"] = kwargs[key]
                elif key == "kind":
                    self.machine_group["kind"] = kwargs[key]
                elif key == "group_type":
                    self.machine_group["group_type"] = kwargs[key]
                elif key == "display_name":
                    self.machine_group["display_name"] = kwargs[key]
                elif key == "count":
                    self.machine_group["count"] = kwargs[key]
                elif key == "machines":
                    self.machine_group["machines"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceMap,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_machinegroup()

        if not old_response:
            self.log("Machine Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Machine Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Machine Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Machine Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_machinegroup()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Machine Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_machinegroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_machinegroup():
                time.sleep(20)
        else:
            self.log("Machine Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_machinegroup(self):
        '''
        Creates or updates Machine Group with the specified configuration.

        :return: deserialized Machine Group instance state dictionary
        '''
        self.log("Creating / Updating the Machine Group instance {0}".format(self.machine_group_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.machine_groups.create(resource_group_name=self.resource_group,
                                                                  workspace_name=self.workspace_name,
                                                                  machine_group=self.machine_group)
            else:
                response = self.mgmt_client.machine_groups.update(resource_group_name=self.resource_group,
                                                                  workspace_name=self.workspace_name,
                                                                  machine_group_name=self.machine_group_name,
                                                                  machine_group=self.machine_group)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Machine Group instance.')
            self.fail("Error creating the Machine Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_machinegroup(self):
        '''
        Deletes specified Machine Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Machine Group instance {0}".format(self.machine_group_name))
        try:
            response = self.mgmt_client.machine_groups.delete(resource_group_name=self.resource_group,
                                                              workspace_name=self.workspace_name,
                                                              machine_group_name=self.machine_group_name)
        except CloudError as e:
            self.log('Error attempting to delete the Machine Group instance.')
            self.fail("Error deleting the Machine Group instance: {0}".format(str(e)))

        return True

    def get_machinegroup(self):
        '''
        Gets the properties of the specified Machine Group.

        :return: deserialized Machine Group instance state dictionary
        '''
        self.log("Checking if the Machine Group instance {0} is present".format(self.machine_group_name))
        found = False
        try:
            response = self.mgmt_client.machine_groups.get(resource_group_name=self.resource_group,
                                                           workspace_name=self.workspace_name,
                                                           machine_group_name=self.machine_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Machine Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Machine Group instance.')
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
    AzureRMMachineGroups()


if __name__ == '__main__':
    main()
