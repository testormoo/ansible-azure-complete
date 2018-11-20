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
module: azure_rm_customerinsightsconnector
version_added: "2.8"
short_description: Manage Connector instance.
description:
    - Create, update and delete instance of Connector.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    name:
        description:
            - The name of the connector.
        required: True
    connector_name:
        description:
            - Name of the connector.
    connector_type:
        description:
            - Type of connector.
            - Required when C(state) is I(present).
        choices:
            - 'none'
            - 'crm'
            - 'azure_blob'
            - 'salesforce'
            - 'exchange_online'
            - 'outbound'
    display_name:
        description:
            - Display name of the connector.
    description:
        description:
            - Description of the connector.
    connector_properties:
        description:
            - The connector properties.
            - Required when C(state) is I(present).
    is_internal:
        description:
            - If this is an internal connector.
    state:
      description:
        - Assert the state of the Connector.
        - Use 'present' to create or update an Connector and 'absent' to delete it.
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
  - name: Create (or update) Connector
    azure_rm_customerinsightsconnector:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      name: testConnector
      connector_type: AzureBlob
      display_name: testConnector
      description: Test connector
      connector_properties: {
  "connectionKeyVaultUrl": {
    "organizationId": "XXX",
    "organizationUrl": "https://XXX.crmlivetie.com/"
  }
}
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/sdkTestHub/connectors/tes
            tConnector"
state:
    description:
        - "State of connector. Possible values include: 'Creating', 'Created', 'Ready', 'Expiring', 'Deleting', 'Failed'"
    returned: always
    type: str
    sample: Creating
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMConnectors(AzureRMModuleBase):
    """Configuration class for an Azure RM Connector resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            connector_name=dict(
                type='str'
            ),
            connector_type=dict(
                type='str',
                choices=['none',
                         'crm',
                         'azure_blob',
                         'salesforce',
                         'exchange_online',
                         'outbound']
            ),
            display_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            connector_properties=dict(
                type='dict'
            ),
            is_internal=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConnectors, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "connector_name":
                    self.parameters["connector_name"] = kwargs[key]
                elif key == "connector_type":
                    ev = kwargs[key]
                    if ev == 'crm':
                        ev = 'CRM'
                    self.parameters["connector_type"] = _snake_to_camel(ev, True)
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "connector_properties":
                    self.parameters["connector_properties"] = kwargs[key]
                elif key == "is_internal":
                    self.parameters["is_internal"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_connector()

        if not old_response:
            self.log("Connector instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Connector instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Connector instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_connector()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Connector instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_connector()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_connector():
                time.sleep(20)
        else:
            self.log("Connector instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_connector(self):
        '''
        Creates or updates Connector with the specified configuration.

        :return: deserialized Connector instance state dictionary
        '''
        self.log("Creating / Updating the Connector instance {0}".format(self.name))

        try:
            response = self.mgmt_client.connectors.create_or_update(resource_group_name=self.resource_group,
                                                                    hub_name=self.hub_name,
                                                                    connector_name=self.name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Connector instance.')
            self.fail("Error creating the Connector instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_connector(self):
        '''
        Deletes specified Connector instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Connector instance {0}".format(self.name))
        try:
            response = self.mgmt_client.connectors.delete(resource_group_name=self.resource_group,
                                                          hub_name=self.hub_name,
                                                          connector_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Connector instance.')
            self.fail("Error deleting the Connector instance: {0}".format(str(e)))

        return True

    def get_connector(self):
        '''
        Gets the properties of the specified Connector.

        :return: deserialized Connector instance state dictionary
        '''
        self.log("Checking if the Connector instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.connectors.get(resource_group_name=self.resource_group,
                                                       hub_name=self.hub_name,
                                                       connector_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Connector instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Connector instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
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
    AzureRMConnectors()


if __name__ == '__main__':
    main()
