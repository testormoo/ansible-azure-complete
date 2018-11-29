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
module: azure_rm_mediaservice
version_added: "2.8"
short_description: Manage Azure Mediaservice instance.
description:
    - Create, update and delete instance of Azure Mediaservice.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    name:
        description:
            - The Media Services account name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    storage_accounts:
        description:
            - The storage accounts for this resource.
        type: list
        suboptions:
            id:
                description:
                    - "The ID of the storage account resource. Media Services relies on tables and queues as well as blobs, so the C(primary) storage
                       account must be a Standard Storage account (either Microsoft.ClassicStorage or Microsoft.Storage). Blob only storage accounts can be
                       added as C(secondary) storage accounts."
            type:
                description:
                    - The type of the storage account.
                    - Required when C(state) is I(present).
                choices:
                    - 'primary'
                    - 'secondary'
    state:
      description:
        - Assert the state of the Mediaservice.
        - Use 'present' to create or update an Mediaservice and 'absent' to delete it.
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
  - name: Create (or update) Mediaservice
    azure_rm_mediaservice:
      resource_group: contoso
      name: contososports
      location: eastus
      storage_accounts:
        - id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso/providers/Microsoft.Storage/storageAccounts/contososportsstore
          type: Primary
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso/providers/Microsoft.Media/mediaservices/contososports
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMMediaservice(AzureRMModuleBase):
    """Configuration class for an Azure RM Mediaservice resource"""

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
            storage_accounts=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str',
                        choices=['primary',
                                 'secondary']
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
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMMediaservice, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['storage_accounts', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['storage_accounts', 'type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_mediaservice()

        if not old_response:
            self.log("Mediaservice instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Mediaservice instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Mediaservice instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_mediaservice()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Mediaservice instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_mediaservice()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Mediaservice instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_mediaservice(self):
        '''
        Creates or updates Mediaservice with the specified configuration.

        :return: deserialized Mediaservice instance state dictionary
        '''
        self.log("Creating / Updating the Mediaservice instance {0}".format(self.name))

        try:
            response = self.mgmt_client.mediaservices.create_or_update(resource_group_name=self.resource_group,
                                                                       account_name=self.name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Mediaservice instance.')
            self.fail("Error creating the Mediaservice instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_mediaservice(self):
        '''
        Deletes specified Mediaservice instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Mediaservice instance {0}".format(self.name))
        try:
            response = self.mgmt_client.mediaservices.delete(resource_group_name=self.resource_group,
                                                             account_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Mediaservice instance.')
            self.fail("Error deleting the Mediaservice instance: {0}".format(str(e)))

        return True

    def get_mediaservice(self):
        '''
        Gets the properties of the specified Mediaservice.

        :return: deserialized Mediaservice instance state dictionary
        '''
        self.log("Checking if the Mediaservice instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.mediaservices.get(resource_group_name=self.resource_group,
                                                          account_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Mediaservice instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Mediaservice instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMMediaservice()


if __name__ == '__main__':
    main()
