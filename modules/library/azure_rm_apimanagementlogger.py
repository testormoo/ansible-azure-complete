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
module: azure_rm_apimanagementlogger
version_added: "2.8"
short_description: Manage Logger instance.
description:
    - Create, update and delete instance of Logger.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    loggerid:
        description:
            - Logger identifier. Must be unique in the API Management service instance.
        required: True
    logger_type:
        description:
            - Logger type.
        required: True
        choices:
            - 'azure_event_hub'
            - 'application_insights'
    description:
        description:
            - Logger description.
    credentials:
        description:
            - The name and SendRule connection string of the event hub for C(azure_event_hub) logger.
            - Instrumentation key for C(application_insights) logger.
        required: True
    is_buffered:
        description:
            - Whether records are buffered in the logger before publishing. Default is assumed to be true.
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Logger.
        - Use 'present' to create or update an Logger and 'absent' to delete it.
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
  - name: Create (or update) Logger
    azure_rm_apimanagementlogger:
      resource_group: rg1
      service_name: apimService1
      loggerid: loggerId
      if_match: NOT FOUND
'''

RETURN = '''
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


class AzureRMLogger(AzureRMModuleBase):
    """Configuration class for an Azure RM Logger resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            loggerid=dict(
                type='str',
                required=True
            ),
            logger_type=dict(
                type='str',
                choices=['azure_event_hub',
                         'application_insights'],
                required=True
            ),
            description=dict(
                type='str'
            ),
            credentials=dict(
                type='dict',
                required=True
            ),
            is_buffered=dict(
                type='str'
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
        self.service_name = None
        self.loggerid = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLogger, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "logger_type":
                    ev = kwargs[key]
                    if ev == 'azure_event_hub':
                        ev = 'azureEventHub'
                    elif ev == 'application_insights':
                        ev = 'applicationInsights'
                    self.parameters["logger_type"] = ev
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "credentials":
                    self.parameters["credentials"] = kwargs[key]
                elif key == "is_buffered":
                    self.parameters["is_buffered"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_logger()

        if not old_response:
            self.log("Logger instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Logger instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Logger instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Logger instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_logger()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Logger instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_logger()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_logger():
                time.sleep(20)
        else:
            self.log("Logger instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_logger(self):
        '''
        Creates or updates Logger with the specified configuration.

        :return: deserialized Logger instance state dictionary
        '''
        self.log("Creating / Updating the Logger instance {0}".format(self.loggerid))

        try:
            response = self.mgmt_client.logger.create_or_update(resource_group_name=self.resource_group,
                                                                service_name=self.service_name,
                                                                loggerid=self.loggerid,
                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Logger instance.')
            self.fail("Error creating the Logger instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_logger(self):
        '''
        Deletes specified Logger instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Logger instance {0}".format(self.loggerid))
        try:
            response = self.mgmt_client.logger.delete(resource_group_name=self.resource_group,
                                                      service_name=self.service_name,
                                                      loggerid=self.loggerid,
                                                      if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Logger instance.')
            self.fail("Error deleting the Logger instance: {0}".format(str(e)))

        return True

    def get_logger(self):
        '''
        Gets the properties of the specified Logger.

        :return: deserialized Logger instance state dictionary
        '''
        self.log("Checking if the Logger instance {0} is present".format(self.loggerid))
        found = False
        try:
            response = self.mgmt_client.logger.get(resource_group_name=self.resource_group,
                                                   service_name=self.service_name,
                                                   loggerid=self.loggerid)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Logger instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Logger instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMLogger()


if __name__ == '__main__':
    main()