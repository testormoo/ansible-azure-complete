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
module: azure_rm_datacatalogadccatalog
version_added: "2.8"
short_description: Manage Azure A D C Catalog instance.
description:
    - Create, update and delete instance of Azure A D C Catalog.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    name:
        description:
            - The name of the data catlog in the specified subscription and resource group.
        required: True
    location:
        description:
            - Resource location
    sku:
        description:
            - Azure data catalog SKU.
        choices:
            - 'free'
            - 'standard'
    units:
        description:
            - Azure data catalog units.
    admins:
        description:
            - Azure data catalog admin list.
        type: list
        suboptions:
            upn:
                description:
                    - UPN of the user.
            object_id:
                description:
                    - Object Id for the user
    users:
        description:
            - Azure data catalog user list.
        type: list
        suboptions:
            upn:
                description:
                    - UPN of the user.
            object_id:
                description:
                    - Object Id for the user
    successfully_provisioned:
        description:
            - Azure data catalog provision status.
    enable_automatic_unit_adjustment:
        description:
            - Automatic unit adjustment enabled or not.
    state:
      description:
        - Assert the state of the A D C Catalog.
        - Use 'present' to create or update an A D C Catalog and 'absent' to delete it.
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
  - name: Create (or update) A D C Catalog
    azure_rm_datacatalogadccatalog:
      resource_group: exampleResourceGroup
      name: exampleCatalog
      location: North US
      sku: Standard
      units: 1
      admins:
        - upn: myupn@microsoft.com
          object_id: 99999999-9999-9999-999999999999
      users:
        - upn: myupn@microsoft.com
          object_id: 99999999-9999-9999-999999999999
      enable_automatic_unit_adjustment: False
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/12345678-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataCatalog/catalogs/exampleCatalog
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datacatalog import DataCatalogRestClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMADCCatalog(AzureRMModuleBase):
    """Configuration class for an Azure RM A D C Catalog resource"""

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
            sku=dict(
                type='str',
                choices=['free',
                         'standard']
            ),
            units=dict(
                type='int'
            ),
            admins=dict(
                type='list',
                options=dict(
                    upn=dict(
                        type='str'
                    ),
                    object_id=dict(
                        type='str'
                    )
                )
            ),
            users=dict(
                type='list',
                options=dict(
                    upn=dict(
                        type='str'
                    ),
                    object_id=dict(
                        type='str'
                    )
                )
            ),
            successfully_provisioned=dict(
                type='str'
            ),
            enable_automatic_unit_adjustment=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMADCCatalog, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.properties[key] = kwargs[key]

        dict_camelize(self.properties, ['sku'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataCatalogRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_adccatalog()

        if not old_response:
            self.log("A D C Catalog instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("A D C Catalog instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the A D C Catalog instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_adccatalog()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("A D C Catalog instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_adccatalog()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("A D C Catalog instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_adccatalog(self):
        '''
        Creates or updates A D C Catalog with the specified configuration.

        :return: deserialized A D C Catalog instance state dictionary
        '''
        self.log("Creating / Updating the A D C Catalog instance {0}".format(self.name))

        try:
            response = self.mgmt_client.adc_catalogs.create_or_update(resource_group_name=self.resource_group,
                                                                      self.config.catalog_name=self.name,
                                                                      properties=self.properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the A D C Catalog instance.')
            self.fail("Error creating the A D C Catalog instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_adccatalog(self):
        '''
        Deletes specified A D C Catalog instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the A D C Catalog instance {0}".format(self.name))
        try:
            response = self.mgmt_client.adc_catalogs.delete(resource_group_name=self.resource_group,
                                                            self.config.catalog_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the A D C Catalog instance.')
            self.fail("Error deleting the A D C Catalog instance: {0}".format(str(e)))

        return True

    def get_adccatalog(self):
        '''
        Gets the properties of the specified A D C Catalog.

        :return: deserialized A D C Catalog instance state dictionary
        '''
        self.log("Checking if the A D C Catalog instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.adc_catalogs.get(resource_group_name=self.resource_group,
                                                         self.config.catalog_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("A D C Catalog instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the A D C Catalog instance.')
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
    AzureRMADCCatalog()


if __name__ == '__main__':
    main()
