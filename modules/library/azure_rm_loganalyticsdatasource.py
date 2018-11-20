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
module: azure_rm_loganalyticsdatasource
version_added: "2.8"
short_description: Manage Data Source instance.
description:
    - Create, update and delete instance of Data Source.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
        required: True
    workspace_name:
        description:
            - Name of the Log Analytics Workspace that will contain the datasource
        required: True
    name:
        description:
            - The name of the datasource resource.
        required: True
    e_tag:
        description:
            - The ETag of the data source.
    kind:
        description:
            - "Possible values include: 'C(azure_activity_log)', 'C(change_tracking_path)', 'C(change_tracking_default_path)',
               'C(change_tracking_default_registry)', 'C(change_tracking_custom_registry)', 'C(custom_log)', 'C(custom_log_collection)',
               'C(generic_data_source)', 'C(iis_logs)', 'C(linux_performance_object)', 'C(linux_performance_collection)', 'C(linux_syslog)',
               'C(linux_syslog_collection)', 'C(windows_event)', 'C(windows_performance_counter)'"
            - Required when C(state) is I(present).
        choices:
            - 'azure_activity_log'
            - 'change_tracking_path'
            - 'change_tracking_default_path'
            - 'change_tracking_default_registry'
            - 'change_tracking_custom_registry'
            - 'custom_log'
            - 'custom_log_collection'
            - 'generic_data_source'
            - 'iis_logs'
            - 'linux_performance_object'
            - 'linux_performance_collection'
            - 'linux_syslog'
            - 'linux_syslog_collection'
            - 'windows_event'
            - 'windows_performance_counter'
    state:
      description:
        - Assert the state of the Data Source.
        - Use 'present' to create or update an Data Source and 'absent' to delete it.
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
  - name: Create (or update) Data Source
    azure_rm_loganalyticsdatasource:
      resource_group: OIAutoRest5123
      workspace_name: AzTest9724
      name: AzTestDS774
      kind: AzureActivityLog
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000005/resourceGroups/OIAutoRest5123/providers/Microsoft.OperationalInsights/workspaces/AzTest9724/
            datasources/AzTestDS774"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.loganalytics import OperationalInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDataSources(AzureRMModuleBase):
    """Configuration class for an Azure RM Data Source resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workspace_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            e_tag=dict(
                type='str'
            ),
            kind=dict(
                type='str',
                choices=['azure_activity_log',
                         'change_tracking_path',
                         'change_tracking_default_path',
                         'change_tracking_default_registry',
                         'change_tracking_custom_registry',
                         'custom_log',
                         'custom_log_collection',
                         'generic_data_source',
                         'iis_logs',
                         'linux_performance_object',
                         'linux_performance_collection',
                         'linux_syslog',
                         'linux_syslog_collection',
                         'windows_event',
                         'windows_performance_counter']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.workspace_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDataSources, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "e_tag":
                    self.parameters["e_tag"] = kwargs[key]
                elif key == "kind":
                    ev = kwargs[key]
                    if ev == 'iis_logs':
                        ev = 'IISLogs'
                    self.parameters["kind"] = _snake_to_camel(ev, True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(OperationalInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_datasource()

        if not old_response:
            self.log("Data Source instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Data Source instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Data Source instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_datasource()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Data Source instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_datasource()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_datasource():
                time.sleep(20)
        else:
            self.log("Data Source instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_datasource(self):
        '''
        Creates or updates Data Source with the specified configuration.

        :return: deserialized Data Source instance state dictionary
        '''
        self.log("Creating / Updating the Data Source instance {0}".format(self.name))

        try:
            response = self.mgmt_client.data_sources.create_or_update(resource_group_name=self.resource_group,
                                                                      workspace_name=self.workspace_name,
                                                                      data_source_name=self.name,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Data Source instance.')
            self.fail("Error creating the Data Source instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_datasource(self):
        '''
        Deletes specified Data Source instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Data Source instance {0}".format(self.name))
        try:
            response = self.mgmt_client.data_sources.delete(resource_group_name=self.resource_group,
                                                            workspace_name=self.workspace_name,
                                                            data_source_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Data Source instance.')
            self.fail("Error deleting the Data Source instance: {0}".format(str(e)))

        return True

    def get_datasource(self):
        '''
        Gets the properties of the specified Data Source.

        :return: deserialized Data Source instance state dictionary
        '''
        self.log("Checking if the Data Source instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.data_sources.get(resource_group_name=self.resource_group,
                                                         workspace_name=self.workspace_name,
                                                         data_source_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Data Source instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Data Source instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMDataSources()


if __name__ == '__main__':
    main()
