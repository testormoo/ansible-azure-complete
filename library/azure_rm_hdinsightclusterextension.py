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
module: azure_rm_hdinsightclusterextension
version_added: "2.8"
short_description: Manage Extension instance.
description:
    - Create, update and delete instance of Extension.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    cluster_name:
        description:
            - The name of the cluster.
        required: True
    workspace_id:
        description:
            - The workspace ID for the cluster monitoring extension.
    primary_key:
        description:
            - The certificate for the cluster monitoring extensions.
    name:
        description:
            - The name of the cluster extension.
        required: True
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
    azure_rm_hdinsightclusterextension:
      resource_group: rg1
      cluster_name: cluster1
      workspace_id: a2090ead-8c9f-4fba-b70e-533e3e003163
      primary_key: **********
      name: clustermonitoring
'''

RETURN = '''
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from azure.mgmt.cluster import HDInsightManagementClient
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
            workspace_id=dict(
                type='str'
            ),
            primary_key=dict(
                type='str'
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

        self.resource_group = None
        self.cluster_name = None
        self.parameters = dict()
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMExtension, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "workspace_id":
                    self.parameters["workspace_id"] = kwargs[key]
                elif key == "primary_key":
                    self.parameters["primary_key"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Extension instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Extension instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_extension()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
                                                             parameters=self.parameters,
                                                             extension_name=self.name)
            else:
                response = self.mgmt_client.extension.update()
            if isinstance(response, LROPoller):
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

    def format_item(self, item):
        d = item.as_dict()
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMExtension()


if __name__ == '__main__':
    main()
