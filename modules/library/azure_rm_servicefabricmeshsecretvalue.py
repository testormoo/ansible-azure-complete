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
module: azure_rm_servicefabricmeshsecretvalue
version_added: "2.8"
short_description: Manage Azure Secret Value instance.
description:
    - Create, update and delete instance of Azure Secret Value.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    secret_resource_name:
        description:
            - The name of the secret resource.
        required: True
    name:
        description:
            - The name of the secret resource I(value) which is typically the version identifier for the I(value).
        required: True
    location:
        description:
            - The geo-location where the resource lives
            - Required when C(state) is I(present).
    value:
        description:
            - The actual value of the secret.
    state:
      description:
        - Assert the state of the Secret Value.
        - Use 'present' to create or update an Secret Value and 'absent' to delete it.
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
  - name: Create (or update) Secret Value
    azure_rm_servicefabricmeshsecretvalue:
      resource_group: sbz_demo
      secret_resource_name: dbConnectionString
      name: v1
      value: mongodb://contoso123:0Fc3IolnL12312asdfawejunASDF@asdfYXX2t8a97kghVcUzcDv98hawelufhawefafnoQRGwNj2nMPL1Y9qsIr9Srdw==@contoso123.documents.azure.com:10255/mydatabase?ssl=true
'''

RETURN = '''
id:
    description:
        - "Fully qualified identifier for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/secrets/dbConnectionString/val
            ues/v1"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMSecretValue(AzureRMModuleBase):
    """Configuration class for an Azure RM Secret Value resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            secret_resource_name=dict(
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
            value=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.secret_resource_name = None
        self.name = None
        self.secret_value_resource_description = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSecretValue, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.secret_value_resource_description[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_secretvalue()

        if not old_response:
            self.log("Secret Value instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Secret Value instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.secret_value_resource_description, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Secret Value instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_secretvalue()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Secret Value instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_secretvalue()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Secret Value instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_secretvalue(self):
        '''
        Creates or updates Secret Value with the specified configuration.

        :return: deserialized Secret Value instance state dictionary
        '''
        self.log("Creating / Updating the Secret Value instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.secret_value.create(resource_group_name=self.resource_group,
                                                                secret_resource_name=self.secret_resource_name,
                                                                secret_value_resource_name=self.name,
                                                                secret_value_resource_description=self.secret_value_resource_description)
            else:
                response = self.mgmt_client.secret_value.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Secret Value instance.')
            self.fail("Error creating the Secret Value instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_secretvalue(self):
        '''
        Deletes specified Secret Value instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Secret Value instance {0}".format(self.name))
        try:
            response = self.mgmt_client.secret_value.delete(resource_group_name=self.resource_group,
                                                            secret_resource_name=self.secret_resource_name,
                                                            secret_value_resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Secret Value instance.')
            self.fail("Error deleting the Secret Value instance: {0}".format(str(e)))

        return True

    def get_secretvalue(self):
        '''
        Gets the properties of the specified Secret Value.

        :return: deserialized Secret Value instance state dictionary
        '''
        self.log("Checking if the Secret Value instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.secret_value.get(resource_group_name=self.resource_group,
                                                         secret_resource_name=self.secret_resource_name,
                                                         secret_value_resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Secret Value instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Secret Value instance.')
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


def main():
    """Main execution"""
    AzureRMSecretValue()


if __name__ == '__main__':
    main()
