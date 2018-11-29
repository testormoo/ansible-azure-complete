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
short_description: Manage Azure Connector instance.
description:
    - Create, update and delete instance of Azure Connector.

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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMConnector(AzureRMModuleBase):
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

        super(AzureRMConnector, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['connector_type'], True)
        dict_map(self.parameters, ['connector_type'], {'crm': 'CRM'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Connector instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None)
                })
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
    AzureRMConnector()


if __name__ == '__main__':
    main()
