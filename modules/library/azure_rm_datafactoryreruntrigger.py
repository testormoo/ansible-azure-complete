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
module: azure_rm_datafactoryreruntrigger
version_added: "2.8"
short_description: Manage Rerun Trigger instance.
description:
    - Create, update and delete instance of Rerun Trigger.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    trigger_name:
        description:
            - The trigger name.
        required: True
    name:
        description:
            - The rerun trigger name.
        required: True
    start_time:
        description:
            - The start time for the time period for which restatement is initiated. Only UTC time is currently supported.
            - Required when C(state) is I(present).
    end_time:
        description:
            - The end time for the time period for which restatement is initiated. Only UTC time is currently supported.
            - Required when C(state) is I(present).
    max_concurrency:
        description:
            - The max number of parallel time windows (ready for execution) for which a rerun is triggered.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Rerun Trigger.
        - Use 'present' to create or update an Rerun Trigger and 'absent' to delete it.
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
  - name: Create (or update) Rerun Trigger
    azure_rm_datafactoryreruntrigger:
      resource_group: exampleResourceGroup
      factory_name: exampleFactoryName
      trigger_name: exampleTrigger
      name: NOT FOUND
      start_time: 2018-06-16T00:39:13.8441801Z
      end_time: 2018-06-16T00:55:13.8441801Z
      max_concurrency: 4
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: "/subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/exampleFactoryN
            ame/triggers/exampleTrigger/rerunTriggers/exampleRerunTrigger"
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


class AzureRMRerunTriggers(AzureRMModuleBase):
    """Configuration class for an Azure RM Rerun Trigger resource"""

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
            trigger_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            start_time=dict(
                type='datetime'
            ),
            end_time=dict(
                type='datetime'
            ),
            max_concurrency=dict(
                type='int'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.factory_name = None
        self.trigger_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRerunTriggers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "start_time":
                    self.parameters["start_time"] = kwargs[key]
                elif key == "end_time":
                    self.parameters["end_time"] = kwargs[key]
                elif key == "max_concurrency":
                    self.parameters["max_concurrency"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_reruntrigger()

        if not old_response:
            self.log("Rerun Trigger instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Rerun Trigger instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Rerun Trigger instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_reruntrigger()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Rerun Trigger instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_reruntrigger()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_reruntrigger():
                time.sleep(20)
        else:
            self.log("Rerun Trigger instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_reruntrigger(self):
        '''
        Creates or updates Rerun Trigger with the specified configuration.

        :return: deserialized Rerun Trigger instance state dictionary
        '''
        self.log("Creating / Updating the Rerun Trigger instance {0}".format(self.))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.rerun_triggers.create(resource_group_name=self.resource_group,
                                                                  factory_name=self.factory_name,
                                                                  trigger_name=self.trigger_name,
                                                                  rerun_trigger_name=self.name,
                                                                  rerun_tumbling_window_trigger_action_parameters=self.parameters)
            else:
                response = self.mgmt_client.rerun_triggers.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Rerun Trigger instance.')
            self.fail("Error creating the Rerun Trigger instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_reruntrigger(self):
        '''
        Deletes specified Rerun Trigger instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Rerun Trigger instance {0}".format(self.))
        try:
            response = self.mgmt_client.rerun_triggers.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Rerun Trigger instance.')
            self.fail("Error deleting the Rerun Trigger instance: {0}".format(str(e)))

        return True

    def get_reruntrigger(self):
        '''
        Gets the properties of the specified Rerun Trigger.

        :return: deserialized Rerun Trigger instance state dictionary
        '''
        self.log("Checking if the Rerun Trigger instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.rerun_triggers.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Rerun Trigger instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Rerun Trigger instance.')
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
    AzureRMRerunTriggers()


if __name__ == '__main__':
    main()
