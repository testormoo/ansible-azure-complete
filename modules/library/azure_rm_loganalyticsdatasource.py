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
short_description: Manage Azure Data Source instance.
description:
    - Create, update and delete instance of Azure Data Source.

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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMDataSource(AzureRMModuleBase):
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

        super(AzureRMDataSource, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['kind'], True)
        dict_map(self.parameters, ['kind'], {'iis_logs': 'IISLogs'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Data Source instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def main():
    """Main execution"""
    AzureRMDataSource()


if __name__ == '__main__':
    main()
