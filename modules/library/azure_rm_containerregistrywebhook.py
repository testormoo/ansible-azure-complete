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
module: azure_rm_containerregistrywebhook
version_added: "2.8"
short_description: Manage Azure Webhook instance.
description:
    - Create, update and delete instance of Azure Webhook.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        required: True
    registry_name:
        description:
            - The name of the container registry.
        required: True
    name:
        description:
            - The name of the webhook.
        required: True
    location:
        description:
            - The location of the webhook. This cannot be changed after the resource is created.
            - Required when C(state) is I(present).
    service_uri:
        description:
            - The service URI for the webhook to post notifications.
    custom_headers:
        description:
            - Custom headers that will be added to the webhook notifications.
    status:
        description:
            - "The status of the webhook at the time the operation was called. Possible values include: 'enabled', 'disabled'"
        type: bool
    scope:
        description:
            - "The scope of repositories where the event can be triggered. For example, 'foo:*' means events for all tags under repository 'foo'. 'foo:bar'
               means events for 'foo:bar' only. 'foo' is equivalent to 'foo:latest'. Empty means all events."
    actions:
        description:
            - The list of actions that trigger the webhook to post notifications.
        type: list
    state:
      description:
        - Assert the state of the Webhook.
        - Use 'present' to create or update an Webhook and 'absent' to delete it.
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
  - name: Create (or update) Webhook
    azure_rm_containerregistrywebhook:
      resource_group: myResourceGroup
      registry_name: myRegistry
      name: myWebhook
      location: westus
      service_uri: http://myservice.com
      custom_headers: {
  "Authorization": "Basic 000000000000000000000000000000000000000000000000000"
}
      status: status
      scope: myRepository
      actions:
        - [
  "push"
]
'''

RETURN = '''
id:
    description:
        - The resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.ContainerRegistry/registries/myRegistry/w
            ebhooks/myWebhook"
status:
    description:
        - "The status of the webhook at the time the operation was called. Possible values include: 'enabled', 'disabled'"
    returned: always
    type: str
    sample: enabled
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.containerregistry import ContainerRegistryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWebhook(AzureRMModuleBase):
    """Configuration class for an Azure RM Webhook resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registry_name=dict(
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
            service_uri=dict(
                type='str'
            ),
            custom_headers=dict(
                type='dict'
            ),
            status=dict(
                type='bool'
            ),
            scope=dict(
                type='str'
            ),
            actions=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.registry_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWebhook, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.webhook_create_parameters[key] = kwargs[key]

        dict_map(self.webhook_create_parameters, ['status'], {True: 'Enabled', False: 'Disabled'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ContainerRegistryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_webhook()

        if not old_response:
            self.log("Webhook instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Webhook instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.webhook_create_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Webhook instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_webhook()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Webhook instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_webhook()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Webhook instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': response.get('status', None)
                })
        return self.results

    def create_update_webhook(self):
        '''
        Creates or updates Webhook with the specified configuration.

        :return: deserialized Webhook instance state dictionary
        '''
        self.log("Creating / Updating the Webhook instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.webhooks.create(resource_group_name=self.resource_group,
                                                            registry_name=self.registry_name,
                                                            webhook_name=self.name,
                                                            webhook_create_parameters=self.parameters)
            else:
                response = self.mgmt_client.webhooks.update(resource_group_name=self.resource_group,
                                                            registry_name=self.registry_name,
                                                            webhook_name=self.name,
                                                            webhook_update_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Webhook instance.')
            self.fail("Error creating the Webhook instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_webhook(self):
        '''
        Deletes specified Webhook instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Webhook instance {0}".format(self.name))
        try:
            response = self.mgmt_client.webhooks.delete(resource_group_name=self.resource_group,
                                                        registry_name=self.registry_name,
                                                        webhook_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Webhook instance.')
            self.fail("Error deleting the Webhook instance: {0}".format(str(e)))

        return True

    def get_webhook(self):
        '''
        Gets the properties of the specified Webhook.

        :return: deserialized Webhook instance state dictionary
        '''
        self.log("Checking if the Webhook instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.webhooks.get(resource_group_name=self.resource_group,
                                                     registry_name=self.registry_name,
                                                     webhook_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Webhook instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Webhook instance.')
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
    AzureRMWebhook()


if __name__ == '__main__':
    main()
