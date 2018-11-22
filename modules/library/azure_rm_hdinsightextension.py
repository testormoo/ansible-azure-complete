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
module: azure_rm_hdinsightextension
version_added: "2.8"
short_description: Manage Azure Extension instance.
description:
    - Create, update and delete instance of Azure Extension.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    cluster_name:
        description:
            - The name of the cluster.
        required: True
    name:
        description:
            - The name of the cluster extension.
        required: True
    workspace_id:
        description:
            - The workspace ID for the cluster monitoring extension.
    primary_key:
        description:
            - The certificate for the cluster monitoring extensions.
    state:
      description:
        - Assert the state of the Extension.
        - Use 'present' to create or update an Extension and 'absent' to delete it.
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
  - name: Create (or update) Extension
    azure_rm_hdinsightextension:
      resource_group: rg1
      cluster_name: cluster1
      name: clustermonitoring
      workspace_id: NOT FOUND
      primary_key: NOT FOUND
'''

RETURN = '''
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.hdinsight import HDInsightManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMExtension(AzureRMModuleBase):
    """Configuration class for an Azure RM Extension resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            workspace_id=dict(
                type='str'
            ),
            primary_key=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.cluster_name = None
        self.name = None
        self.workspace_id = None
        self.primary_key = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMExtension, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(HDInsightManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_extension()

        if not old_response:
            self.log("Extension instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Extension instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Extension instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_extension()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Extension instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_extension()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_extension():
                time.sleep(20)
        else:
            self.log("Extension instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_extension(self):
        '''
        Creates or updates Extension with the specified configuration.

        :return: deserialized Extension instance state dictionary
        '''
        self.log("Creating / Updating the Extension instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.extension.create(resource_group_name=self.resource_group,
                                                             cluster_name=self.cluster_name,
                                                             extension_name=self.name)
            else:
                response = self.mgmt_client.extension.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Extension instance.')
            self.fail("Error creating the Extension instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_extension(self):
        '''
        Deletes specified Extension instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Extension instance {0}".format(self.name))
        try:
            response = self.mgmt_client.extension.delete(resource_group_name=self.resource_group,
                                                         cluster_name=self.cluster_name,
                                                         extension_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Extension instance.')
            self.fail("Error deleting the Extension instance: {0}".format(str(e)))

        return True

    def get_extension(self):
        '''
        Gets the properties of the specified Extension.

        :return: deserialized Extension instance state dictionary
        '''
        self.log("Checking if the Extension instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.extension.get(resource_group_name=self.resource_group,
                                                      cluster_name=self.cluster_name,
                                                      extension_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Extension instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Extension instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def expand(d, path, **kwargs):
    expandx = kwargs.get('expand', None)
    rename = kwargs.get('rename', None)
    camelize = kwargs.get('camelize', False)
    camelize_lower = kwargs.get('camelize_lower', False)
    upper = kwargs.get('upper', False)
    map = kwargs.get('map', None)
    if isinstance(d, list):
        for i in range(len(d)):
            expand(d[i], path, **kwargs)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_name = path[0]
            new_name = old_name if rename is None else rename
            old_value = d.get(old_name, None)
            new_value = None
            if old_value is not None:
                if map is not None:
                    new_value = map.get(old_value, None)
                if new_value is None:
                    if camelize:
                        new_value = _snake_to_camel(old_value, True)
                    elif camelize_lower:
                        new_value = _snake_to_camel(old_value, False)
                    elif upper:
                        new_value = old_value.upper()
            if expandx is None:
                # just rename
                if new_name != old_name:
                    d.pop(old_name, None)
            else:
                # expand and rename
                d[expandx] = d.get(expandx, {})
                d.pop(old_name, None)
                d = d[expandx]
            d[new_name] = new_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                expand(sd, path[1:], **kwargs)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMExtension()


if __name__ == '__main__':
    main()
