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
module: azure_rm_operationsmanagementmanagementassociation
version_added: "2.8"
short_description: Manage Azure Management Association instance.
description:
    - Create, update and delete instance of Azure Management Association.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
        required: True
    self.config.provider_name:
        description:
            - Provider name for the parent resource.
        required: True
    self.config.resource_type:
        description:
            - Resource type for the parent resource
        required: True
    self.config.resource_name:
        description:
            - Parent resource name.
        required: True
    name:
        description:
            - User ManagementAssociation Name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    application_id:
        description:
            - The applicationId of the appliance for this association.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Management Association.
        - Use 'present' to create or update an Management Association and 'absent' to delete it.
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
  - name: Create (or update) Management Association
    azure_rm_operationsmanagementmanagementassociation:
      resource_group: rg1
      self.config.provider_name: NOT FOUND
      self.config.resource_type: NOT FOUND
      self.config.resource_name: NOT FOUND
      name: managementAssociation1
      location: eastus
      application_id: /subscriptions/sub1/resourcegroups/rg1/providers/Microsoft.Appliance/Appliances/appliance1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourcegroups/rg1/providers/Microsoft.OperationalInsights/workspaces/ws1/Microsoft.OperationsManagement/ManagementAssociat
            ions/managementAssociation1"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.operationsmanagement import OperationsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagementAssociation(AzureRMModuleBase):
    """Configuration class for an Azure RM Management Association resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            self.config.provider_name=dict(
                type='str',
                required=True
            ),
            self.config.resource_type=dict(
                type='str',
                required=True
            ),
            self.config.resource_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            application_id=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.self.config.provider_name = None
        self.self.config.resource_type = None
        self.self.config.resource_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagementAssociation, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_expand(self.parameters, ['application_id'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(OperationsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_managementassociation()

        if not old_response:
            self.log("Management Association instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Management Association instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Management Association instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managementassociation()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Management Association instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managementassociation()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Management Association instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_managementassociation(self):
        '''
        Creates or updates Management Association with the specified configuration.

        :return: deserialized Management Association instance state dictionary
        '''
        self.log("Creating / Updating the Management Association instance {0}".format(self.name))

        try:
            response = self.mgmt_client.management_associations.create_or_update(resource_group_name=self.resource_group,
                                                                                 self.config.provider_name=self.self.config.provider_name,
                                                                                 self.config.resource_type=self.self.config.resource_type,
                                                                                 self.config.resource_name=self.self.config.resource_name,
                                                                                 management_association_name=self.name,
                                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Management Association instance.')
            self.fail("Error creating the Management Association instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_managementassociation(self):
        '''
        Deletes specified Management Association instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Management Association instance {0}".format(self.name))
        try:
            response = self.mgmt_client.management_associations.delete(resource_group_name=self.resource_group,
                                                                       self.config.provider_name=self.self.config.provider_name,
                                                                       self.config.resource_type=self.self.config.resource_type,
                                                                       self.config.resource_name=self.self.config.resource_name,
                                                                       management_association_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Management Association instance.')
            self.fail("Error deleting the Management Association instance: {0}".format(str(e)))

        return True

    def get_managementassociation(self):
        '''
        Gets the properties of the specified Management Association.

        :return: deserialized Management Association instance state dictionary
        '''
        self.log("Checking if the Management Association instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.management_associations.get(resource_group_name=self.resource_group,
                                                                    self.config.provider_name=self.self.config.provider_name,
                                                                    self.config.resource_type=self.self.config.resource_type,
                                                                    self.config.resource_name=self.self.config.resource_name,
                                                                    management_association_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Management Association instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Management Association instance.')
        if found is True:
            return response.as_dict()

        return False


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
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
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def main():
    """Main execution"""
    AzureRMManagementAssociation()


if __name__ == '__main__':
    main()
