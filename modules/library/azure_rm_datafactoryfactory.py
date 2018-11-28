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
module: azure_rm_datafactoryfactory
version_added: "2.8"
short_description: Manage Azure Factory instance.
description:
    - Create, update and delete instance of Azure Factory.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    name:
        description:
            - The factory name.
        required: True
    location:
        description:
            - The resource location.
    additional_properties:
        description:
            - Unmatched properties from the message are deserialized this collection
    identity:
        description:
            - Managed service identity of the factory.
        suboptions:
            type:
                description:
                    - "The identity type. Currently the only supported type is 'SystemAssigned'."
                    - Required when C(state) is I(present).
    repo_configuration:
        description:
            - Git repo information of the factory.
        suboptions:
            account_name:
                description:
                    - Account name.
                    - Required when C(state) is I(present).
            repository_name:
                description:
                    - Rrepository name.
                    - Required when C(state) is I(present).
            collaboration_branch:
                description:
                    - Collaboration branch.
                    - Required when C(state) is I(present).
            root_folder:
                description:
                    - Root folder.
                    - Required when C(state) is I(present).
            last_commit_id:
                description:
                    - Last commit id.
            type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    if_match:
        description:
            - ETag of the factory entity. Should only be specified for update, for which it should match existing entity or can be * for unconditional update.
    state:
      description:
        - Assert the state of the Factory.
        - Use 'present' to create or update an Factory and 'absent' to delete it.
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
  - name: Create (or update) Factory
    azure_rm_datafactoryfactory:
      resource_group: exampleResourceGroup
      name: exampleFactoryName
      location: East US
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: /subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/exampleFactoryName
version:
    description:
        - Version of the factory.
    returned: always
    type: str
    sample: 2018-06-01
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMFactory(AzureRMModuleBase):
    """Configuration class for an Azure RM Factory resource"""

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
            additional_properties=dict(
                type='dict'
            ),
            identity=dict(
                type='dict'
                options=dict(
                    type=dict(
                        type='str'
                    )
                )
            ),
            repo_configuration=dict(
                type='dict'
                options=dict(
                    account_name=dict(
                        type='str'
                    ),
                    repository_name=dict(
                        type='str'
                    ),
                    collaboration_branch=dict(
                        type='str'
                    ),
                    root_folder=dict(
                        type='str'
                    ),
                    last_commit_id=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            if_match=dict(
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
        self.factory = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFactory, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.factory[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_factory()

        if not old_response:
            self.log("Factory instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Factory instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.factory, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Factory instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_factory()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Factory instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_factory()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Factory instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'version': response.get('version', None)
                })
        return self.results

    def create_update_factory(self):
        '''
        Creates or updates Factory with the specified configuration.

        :return: deserialized Factory instance state dictionary
        '''
        self.log("Creating / Updating the Factory instance {0}".format(self.name))

        try:
            response = self.mgmt_client.factories.create_or_update(resource_group_name=self.resource_group,
                                                                   factory_name=self.name,
                                                                   factory=self.factory)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Factory instance.')
            self.fail("Error creating the Factory instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_factory(self):
        '''
        Deletes specified Factory instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Factory instance {0}".format(self.name))
        try:
            response = self.mgmt_client.factories.delete(resource_group_name=self.resource_group,
                                                         factory_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Factory instance.')
            self.fail("Error deleting the Factory instance: {0}".format(str(e)))

        return True

    def get_factory(self):
        '''
        Gets the properties of the specified Factory.

        :return: deserialized Factory instance state dictionary
        '''
        self.log("Checking if the Factory instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.factories.get(resource_group_name=self.resource_group,
                                                      factory_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Factory instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Factory instance.')
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


def main():
    """Main execution"""
    AzureRMFactory()


if __name__ == '__main__':
    main()
