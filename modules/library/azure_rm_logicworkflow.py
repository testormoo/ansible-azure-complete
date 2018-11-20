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
module: azure_rm_logicworkflow
version_added: "2.8"
short_description: Manage Workflow instance.
description:
    - Create, update and delete instance of Workflow.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    name:
        description:
            - The I(workflow) name.
        required: True
    workflow:
        description:
            - The workflow.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            state:
                description:
                    - The state.
                choices:
                    - 'not_specified'
                    - 'completed'
                    - 'enabled'
                    - 'disabled'
                    - 'deleted'
                    - 'suspended'
            sku:
                description:
                    - The sku.
                suboptions:
                    name:
                        description:
                            - The name.
                            - Required when C(state) is I(present).
                        choices:
                            - 'not_specified'
                            - 'free'
                            - 'shared'
                            - 'basic'
                            - 'standard'
                            - 'premium'
                    plan:
                        description:
                            - The reference to plan.
            integration_account:
                description:
                    - The integration account.
            definition:
                description:
                    - The definition.
            parameters:
                description:
                    - The parameters.
    state:
      description:
        - Assert the state of the Workflow.
        - Use 'present' to create or update an Workflow and 'absent' to delete it.
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
  - name: Create (or update) Workflow
    azure_rm_logicworkflow:
      resource_group: test-resource-group
      name: test-workflow
      workflow:
        location: brazilsouth
        integration_account: {
  "name": "test-integration-account",
  "id": "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/test-resource-group/providers/Microsoft.Logic/integrationAccounts/test-integration-account",
  "type": "Microsoft.Logic/integrationAccounts"
}
        definition: {
  "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "$connections": {
      "defaultValue": {},
      "type": "Object"
    }
  },
  "triggers": {
    "manual": {
      "type": "Request",
      "kind": "Http",
      "inputs": {
        "schema": {}
      }
    }
  },
  "actions": {
    "Find_pet_by_ID": {
      "runAfter": {},
      "type": "ApiConnection",
      "inputs": {
        "host": {
          "connection": {
            "name": "@parameters('$connections')['test-custom-connector']['connectionId']"
          }
        },
        "method": "get",
        "path": "/pet/@{encodeURIComponent('1')}"
      }
    }
  },
  "outputs": {}
}
        parameters: {
  "$connections": {
    "value": {
      "test-custom-connector": {
        "connectionId": "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/test-resource-group/providers/Microsoft.Web/connections/test-custom-connector",
        "connectionName": "test-custom-connector",
        "id": "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/providers/Microsoft.Web/locations/brazilsouth/managedApis/test-custom-connector"
      }
    }
  }
}
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: id
state:
    description:
        - "The state. Possible values include: 'NotSpecified', 'Completed', 'Enabled', 'Disabled', 'Deleted', 'Suspended'"
    returned: always
    type: str
    sample: state
version:
    description:
        - Gets the version.
    returned: always
    type: str
    sample: version
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWorkflows(AzureRMModuleBase):
    """Configuration class for an Azure RM Workflow resource"""

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
            workflow=dict(
                type='dict',
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
        self.workflow = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWorkflows, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.workflow["location"] = kwargs[key]
                elif key == "state":
                    self.workflow["state"] = _snake_to_camel(kwargs[key], True)
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'not_specified':
                            ev['name'] = 'NotSpecified'
                        elif ev['name'] == 'free':
                            ev['name'] = 'Free'
                        elif ev['name'] == 'shared':
                            ev['name'] = 'Shared'
                        elif ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                        elif ev['name'] == 'premium':
                            ev['name'] = 'Premium'
                    self.workflow["sku"] = ev
                elif key == "integration_account":
                    self.workflow["integration_account"] = kwargs[key]
                elif key == "definition":
                    self.workflow["definition"] = kwargs[key]
                elif key == "parameters":
                    self.workflow["parameters"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_workflow()

        if not old_response:
            self.log("Workflow instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Workflow instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Workflow instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_workflow()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Workflow instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_workflow()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_workflow():
                time.sleep(20)
        else:
            self.log("Workflow instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_workflow(self):
        '''
        Creates or updates Workflow with the specified configuration.

        :return: deserialized Workflow instance state dictionary
        '''
        self.log("Creating / Updating the Workflow instance {0}".format(self.name))

        try:
            response = self.mgmt_client.workflows.create_or_update(resource_group_name=self.resource_group,
                                                                   workflow_name=self.name,
                                                                   workflow=self.workflow)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Workflow instance.')
            self.fail("Error creating the Workflow instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_workflow(self):
        '''
        Deletes specified Workflow instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Workflow instance {0}".format(self.name))
        try:
            response = self.mgmt_client.workflows.delete(resource_group_name=self.resource_group,
                                                         workflow_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Workflow instance.')
            self.fail("Error deleting the Workflow instance: {0}".format(str(e)))

        return True

    def get_workflow(self):
        '''
        Gets the properties of the specified Workflow.

        :return: deserialized Workflow instance state dictionary
        '''
        self.log("Checking if the Workflow instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.workflows.get(resource_group_name=self.resource_group,
                                                      workflow_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Workflow instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Workflow instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None),
            'version': d.get('version', None)
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
    AzureRMWorkflows()


if __name__ == '__main__':
    main()
