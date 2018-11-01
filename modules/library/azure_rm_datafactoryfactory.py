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
short_description: Manage Factory instance.
description:
    - Create, update and delete instance of Factory.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The I(factory) name.
        required: True
    factory:
        description:
            - Factory resource definition.
        required: True
        suboptions:
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
                        required: True
            repo_configuration:
                description:
                    - Git repo information of the factory.
                suboptions:
                    account_name:
                        description:
                            - Account name.
                        required: True
                    repository_name:
                        description:
                            - Rrepository name.
                        required: True
                    collaboration_branch:
                        description:
                            - Collaboration branch.
                        required: True
                    root_folder:
                        description:
                            - Root folder.
                        required: True
                    last_commit_id:
                        description:
                            - Last commit id.
                    type:
                        description:
                            - Constant filled by server.
                        required: True
    if_match:
        description:
            - "ETag of the I(factory) entity. Should only be specified for update, for which it should match existing entity or can be * for unconditional
               update."
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
      factory_name: exampleFactoryName
      factory:
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


class AzureRMFactories(AzureRMModuleBase):
    """Configuration class for an Azure RM Factory resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            factory_name=dict(
                type='str',
                required=True
            ),
            factory=dict(
                type='dict',
                required=True
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
        self.factory_name = None
        self.factory = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFactories, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.factory["location"] = kwargs[key]
                elif key == "additional_properties":
                    self.factory["additional_properties"] = kwargs[key]
                elif key == "identity":
                    self.factory["identity"] = kwargs[key]
                elif key == "repo_configuration":
                    self.factory["repo_configuration"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Factory instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Factory instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_factory()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Factory instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_factory()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_factory():
                time.sleep(20)
        else:
            self.log("Factory instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_factory(self):
        '''
        Creates or updates Factory with the specified configuration.

        :return: deserialized Factory instance state dictionary
        '''
        self.log("Creating / Updating the Factory instance {0}".format(self.factory_name))

        try:
            response = self.mgmt_client.factories.create_or_update(resource_group_name=self.resource_group,
                                                                   factory_name=self.factory_name,
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
        self.log("Deleting the Factory instance {0}".format(self.factory_name))
        try:
            response = self.mgmt_client.factories.delete(resource_group_name=self.resource_group,
                                                         factory_name=self.factory_name)
        except CloudError as e:
            self.log('Error attempting to delete the Factory instance.')
            self.fail("Error deleting the Factory instance: {0}".format(str(e)))

        return True

    def get_factory(self):
        '''
        Gets the properties of the specified Factory.

        :return: deserialized Factory instance state dictionary
        '''
        self.log("Checking if the Factory instance {0} is present".format(self.factory_name))
        found = False
        try:
            response = self.mgmt_client.factories.get(resource_group_name=self.resource_group,
                                                      factory_name=self.factory_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Factory instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Factory instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'version': d.get('version', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMFactories()


if __name__ == '__main__':
    main()