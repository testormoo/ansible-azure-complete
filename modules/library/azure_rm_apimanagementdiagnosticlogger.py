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
module: azure_rm_apimanagementdiagnosticlogger
version_added: "2.8"
short_description: Manage Diagnostic Logger instance.
description:
    - Create, update and delete instance of Diagnostic Logger.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    diagnostic_id:
        description:
            - Diagnostic identifier. Must be unique in the current API Management service instance.
        required: True
    loggerid:
        description:
            - Logger identifier. Must be unique in the API Management service instance.
        required: True
    state:
      description:
        - Assert the state of the Diagnostic Logger.
        - Use 'present' to create or update an Diagnostic Logger and 'absent' to delete it.
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
  - name: Create (or update) Diagnostic Logger
    azure_rm_apimanagementdiagnosticlogger:
      resource_group: rg1
      name: apimService1
      diagnostic_id: default
      loggerid: applicationinsights
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourcegroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/diagnostics/default/loggers/applicationinsights
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDiagnosticLogger(AzureRMModuleBase):
    """Configuration class for an Azure RM Diagnostic Logger resource"""

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
            diagnostic_id=dict(
                type='str',
                required=True
            ),
            loggerid=dict(
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
        self.name = None
        self.diagnostic_id = None
        self.loggerid = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDiagnosticLogger, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_diagnosticlogger()

        if not old_response:
            self.log("Diagnostic Logger instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Diagnostic Logger instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Diagnostic Logger instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_diagnosticlogger()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Diagnostic Logger instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_diagnosticlogger()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_diagnosticlogger():
                time.sleep(20)
        else:
            self.log("Diagnostic Logger instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_diagnosticlogger(self):
        '''
        Creates or updates Diagnostic Logger with the specified configuration.

        :return: deserialized Diagnostic Logger instance state dictionary
        '''
        self.log("Creating / Updating the Diagnostic Logger instance {0}".format(self.loggerid))

        try:
            response = self.mgmt_client.diagnostic_logger.create_or_update(resource_group_name=self.resource_group,
                                                                           service_name=self.name,
                                                                           diagnostic_id=self.diagnostic_id,
                                                                           loggerid=self.loggerid)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Diagnostic Logger instance.')
            self.fail("Error creating the Diagnostic Logger instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_diagnosticlogger(self):
        '''
        Deletes specified Diagnostic Logger instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Diagnostic Logger instance {0}".format(self.loggerid))
        try:
            response = self.mgmt_client.diagnostic_logger.delete(resource_group_name=self.resource_group,
                                                                 service_name=self.name,
                                                                 diagnostic_id=self.diagnostic_id,
                                                                 loggerid=self.loggerid)
        except CloudError as e:
            self.log('Error attempting to delete the Diagnostic Logger instance.')
            self.fail("Error deleting the Diagnostic Logger instance: {0}".format(str(e)))

        return True

    def get_diagnosticlogger(self):
        '''
        Gets the properties of the specified Diagnostic Logger.

        :return: deserialized Diagnostic Logger instance state dictionary
        '''
        self.log("Checking if the Diagnostic Logger instance {0} is present".format(self.loggerid))
        found = False
        try:
            response = self.mgmt_client.diagnostic_logger.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Diagnostic Logger instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Diagnostic Logger instance.')
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


def main():
    """Main execution"""
    AzureRMDiagnosticLogger()


if __name__ == '__main__':
    main()
