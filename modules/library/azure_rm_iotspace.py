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
module: azure_rm_iotspace
version_added: "2.8"
short_description: Manage Azure Io T Space instance.
description:
    - Create, update and delete instance of Azure Io T Space.

options:
    resource_group:
        description:
            - The name of the resource group that contains the IoTSpaces instance.
        required: True
    name:
        description:
            - The name of the IoTSpaces instance.
        required: True
    location:
        description:
            - The resource location.
            - Required when C(state) is I(present).
    storage_container:
        description:
            - The properties of the designated storage container.
        suboptions:
            connection_string:
                description:
                    - The connection string of the storage account.
            subscription_id:
                description:
                    - The subscription identifier of the storage account.
            resource_group:
                description:
                    - The name of the resource group of the storage account.
            container_name:
                description:
                    - The name of storage container in the storage account.
    sku:
        description:
            - A valid instance SKU.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - The name of the SKU.
                    - Required when C(state) is I(present).
                choices:
                    - 'f1'
                    - 's1'
                    - 's2'
                    - 's3'
    state:
      description:
        - Assert the state of the Io T Space.
        - Use 'present' to create or update an Io T Space and 'absent' to delete it.
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
  - name: Create (or update) Io T Space
    azure_rm_iotspace:
      resource_group: resRg
      name: myIoTSpacesService
      location: string
      storage_container:
        connection_string: string
        subscription_id: string
        resource_group: string
        container_name: string
      sku:
        name: F1
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/resRg/providers/Microsoft.IoTSpaces/IoTSpacesService/myIoTSpacesService
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.iotspaces import IoTSpacesClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIoTSpace(AzureRMModuleBase):
    """Configuration class for an Azure RM Io T Space resource"""

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
            location=dict(
                type='str'
            ),
            storage_container=dict(
                type='dict'
                options=dict(
                    connection_string=dict(
                        type='str'
                    ),
                    subscription_id=dict(
                        type='str'
                    ),
                    resource_group=dict(
                        type='str'
                    ),
                    container_name=dict(
                        type='str'
                    )
                )
            ),
            sku=dict(
                type='dict'
                options=dict(
                    name=dict(
                        type='str',
                        choices=['f1',
                                 's1',
                                 's2',
                                 's3']
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.iot_space_description = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIoTSpace, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.iot_space_description[key] = kwargs[key]

        dict_expand(self.iot_space_description, ['storage_container'])
        dict_camelize(self.iot_space_description, ['sku', 'name'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(IoTSpacesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_iotspace()

        if not old_response:
            self.log("Io T Space instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Io T Space instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.iot_space_description, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Io T Space instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_iotspace()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Io T Space instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_iotspace()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Io T Space instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_iotspace(self):
        '''
        Creates or updates Io T Space with the specified configuration.

        :return: deserialized Io T Space instance state dictionary
        '''
        self.log("Creating / Updating the Io T Space instance {0}".format(self.name))

        try:
            response = self.mgmt_client.io_tspaces.create_or_update(resource_group_name=self.resource_group,
                                                                    resource_name=self.name,
                                                                    iot_space_description=self.iot_space_description)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Io T Space instance.')
            self.fail("Error creating the Io T Space instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_iotspace(self):
        '''
        Deletes specified Io T Space instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Io T Space instance {0}".format(self.name))
        try:
            response = self.mgmt_client.io_tspaces.delete(resource_group_name=self.resource_group,
                                                          resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Io T Space instance.')
            self.fail("Error deleting the Io T Space instance: {0}".format(str(e)))

        return True

    def get_iotspace(self):
        '''
        Gets the properties of the specified Io T Space.

        :return: deserialized Io T Space instance state dictionary
        '''
        self.log("Checking if the Io T Space instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.io_tspaces.get(resource_group_name=self.resource_group,
                                                       resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Io T Space instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Io T Space instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def main():
    """Main execution"""
    AzureRMIoTSpace()


if __name__ == '__main__':
    main()
