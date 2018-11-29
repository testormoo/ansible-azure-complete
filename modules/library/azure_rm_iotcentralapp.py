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
module: azure_rm_iotcentralapp
version_added: "2.8"
short_description: Manage Azure App instance.
description:
    - Create, update and delete instance of Azure App.

options:
    resource_group:
        description:
            - The name of the resource group that contains the IoT Central application.
        required: True
    name:
        description:
            - The ARM resource name of the IoT Central application.
        required: True
    location:
        description:
            - The resource location.
            - Required when C(state) is I(present).
    display_name:
        description:
            - The display name of the application.
    subdomain:
        description:
            - The subdomain of the application.
    template:
        description:
            - "The ID of the application template, which is a blueprint that defines the characteristics and behaviors of an application. Optional; if not
               specified, defaults to a blank blueprint and allows the application to be defined from scratch."
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
    state:
      description:
        - Assert the state of the App.
        - Use 'present' to create or update an App and 'absent' to delete it.
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
  - name: Create (or update) App
    azure_rm_iotcentralapp:
      resource_group: resRg
      name: myIoTCentralApp
      location: westus
      display_name: My IoT Central App
      subdomain: my-iot-central-app
      template: iotc-default@1.0.0
      sku:
        name: F1
'''

RETURN = '''
id:
    description:
        - The ARM resource identifier.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/resRg/providers/Microsoft.IoTCentral/IoTApps/myIoTCentralApp
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.iotcentral import IotCentralClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApp(AzureRMModuleBase):
    """Configuration class for an Azure RM App resource"""

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
            display_name=dict(
                type='str'
            ),
            subdomain=dict(
                type='str'
            ),
            template=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['f1',
                                 's1']
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
        self.app = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApp, self).__init__(derived_arg_spec=self.module_arg_spec,
                                         supports_check_mode=True,
                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.app[key] = kwargs[key]

        dict_camelize(self.app, ['sku', 'name'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(IotCentralClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_app()

        if not old_response:
            self.log("App instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("App instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.app, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the App instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_app()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("App instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_app()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("App instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_app(self):
        '''
        Creates or updates App with the specified configuration.

        :return: deserialized App instance state dictionary
        '''
        self.log("Creating / Updating the App instance {0}".format(self.name))

        try:
            response = self.mgmt_client.apps.create_or_update(resource_group_name=self.resource_group,
                                                              resource_name=self.name,
                                                              app=self.app)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the App instance.')
            self.fail("Error creating the App instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_app(self):
        '''
        Deletes specified App instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the App instance {0}".format(self.name))
        try:
            response = self.mgmt_client.apps.delete(resource_group_name=self.resource_group,
                                                    resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the App instance.')
            self.fail("Error deleting the App instance: {0}".format(str(e)))

        return True

    def get_app(self):
        '''
        Gets the properties of the specified App.

        :return: deserialized App instance state dictionary
        '''
        self.log("Checking if the App instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.apps.get(resource_group_name=self.resource_group,
                                                 resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("App instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the App instance.')
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
    AzureRMApp()


if __name__ == '__main__':
    main()
