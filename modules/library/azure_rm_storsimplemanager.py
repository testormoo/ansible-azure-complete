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
short_description: Manage Azure Manager instance.
description:
    - Create, update and delete instance of Azure Manager.

options:
    location:
        description:
            - The Geo location of the Manager
            - Required when C(state) is I(present).
    cis_intrinsic_settings:
        description:
            - Specifies if the Manager is Garda or Helsinki
        suboptions:
            type:
                description:
                    - Refers to the type of the StorSimple Manager.
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
    resource_group:
        description:
            - The resource group name
        required: True
    name:
        description:
            - The manager name
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
      location: westus
      cis_intrinsic_settings:
        type: HelsinkiV1
      sku:
        name: Standard
      resource_group: ResourceGroupForSDKTest
      name: hManagerForSDKTest
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMManager(AzureRMModuleBase):
    """Configuration class for an Azure RM Manager resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            location=dict(
                type='str'
            ),
            cis_intrinsic_settings=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str',
                        choices=['garda_v1',
                                 'helsinki_v1']
                    )
                )
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    )
                )
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManager, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.manager[key] = kwargs[key]

        dict_camelize(self.manager, ['cis_intrinsic_settings', 'type'], True)

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
                if (not default_compare(self.manager, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Manager instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_manager()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Manager instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_manager()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Manager instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_manager(self):
        '''
        Creates or updates Manager with the specified configuration.

        :return: deserialized Manager instance state dictionary
        '''
        self.log("Creating / Updating the Manager instance {0}".format(self.name))

        try:
            response = self.mgmt_client.managers.create_or_update(manager=self.manager,
                                                                  resource_group_name=self.resource_group,
                                                                  manager_name=self.name)
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
        self.log("Deleting the Manager instance {0}".format(self.name))
        try:
            response = self.mgmt_client.managers.delete(resource_group_name=self.resource_group,
                                                        manager_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Manager instance.')
            self.fail("Error deleting the Manager instance: {0}".format(str(e)))

        return True

    def get_manager(self):
        '''
        Gets the properties of the specified Manager.

        :return: deserialized Manager instance state dictionary
        '''
        self.log("Checking if the Manager instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.managers.get(resource_group_name=self.resource_group,
                                                     manager_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Manager instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Manager instance.')
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
            else:
                key = list(old[0])[0]
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
    AzureRMManager()


if __name__ == '__main__':
    main()
