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
short_description: Manage A D C Catalog instance.
description:
    - Create, update and delete instance of A D C Catalog.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    self.config.catalog_name:
        description:
            - The name of the data catlog in the specified subscription and resource group.
        required: True
    location:
        description:
            - Resource location
    etag:
        description:
            - Resource etag
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
      self.config.catalog_name: exampleCatalog
      location: North US
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


class AzureRMADCCatalogs(AzureRMModuleBase):
    """Configuration class for an Azure RM A D C Catalog resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            self.config.catalog_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            etag=dict(
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
                type='list'
            ),
            users=dict(
                type='list'
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
        self.self.config.catalog_name = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMADCCatalogs, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.properties["location"] = kwargs[key]
                elif key == "etag":
                    self.properties["etag"] = kwargs[key]
                elif key == "sku":
                    self.properties["sku"] = _snake_to_camel(kwargs[key], True)
                elif key == "units":
                    self.properties["units"] = kwargs[key]
                elif key == "admins":
                    self.properties["admins"] = kwargs[key]
                elif key == "users":
                    self.properties["users"] = kwargs[key]
                elif key == "successfully_provisioned":
                    self.properties["successfully_provisioned"] = kwargs[key]
                elif key == "enable_automatic_unit_adjustment":
                    self.properties["enable_automatic_unit_adjustment"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if A D C Catalog instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the A D C Catalog instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_adccatalog()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("A D C Catalog instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_adccatalog()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_adccatalog():
                time.sleep(20)
        else:
            self.log("A D C Catalog instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_adccatalog(self):
        '''
        Creates or updates A D C Catalog with the specified configuration.

        :return: deserialized A D C Catalog instance state dictionary
        '''
        self.log("Creating / Updating the A D C Catalog instance {0}".format(self.self.config.catalog_name))

        try:
            response = self.mgmt_client.adc_catalogs.create_or_update(resource_group_name=self.resource_group,
                                                                      self.config.catalog_name=self.self.config.catalog_name,
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
        self.log("Deleting the A D C Catalog instance {0}".format(self.self.config.catalog_name))
        try:
            response = self.mgmt_client.adc_catalogs.delete(resource_group_name=self.resource_group,
                                                            self.config.catalog_name=self.self.config.catalog_name)
        except CloudError as e:
            self.log('Error attempting to delete the A D C Catalog instance.')
            self.fail("Error deleting the A D C Catalog instance: {0}".format(str(e)))

        return True

    def get_adccatalog(self):
        '''
        Gets the properties of the specified A D C Catalog.

        :return: deserialized A D C Catalog instance state dictionary
        '''
        self.log("Checking if the A D C Catalog instance {0} is present".format(self.self.config.catalog_name))
        found = False
        try:
            response = self.mgmt_client.adc_catalogs.get(resource_group_name=self.resource_group,
                                                         self.config.catalog_name=self.self.config.catalog_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("A D C Catalog instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the A D C Catalog instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMADCCatalogs()


if __name__ == '__main__':
    main()
