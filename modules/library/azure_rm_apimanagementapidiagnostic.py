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
module: azure_rm_apimanagementapidiagnostic
version_added: "2.8"
short_description: Manage Api Diagnostic instance.
description:
    - Create, update and delete instance of Api Diagnostic.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - API identifier. Must be unique in the current API Management service instance.
        required: True
    diagnostic_id:
        description:
            - Diagnostic identifier. Must be unique in the current API Management service instance.
        required: True
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    enabled:
        description:
            - Indicates whether a diagnostic should receive data or not.
        required: True
    state:
      description:
        - Assert the state of the Api Diagnostic.
        - Use 'present' to create or update an Api Diagnostic and 'absent' to delete it.
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
  - name: Create (or update) Api Diagnostic
    azure_rm_apimanagementapidiagnostic:
      resource_group: rg1
      name: apimService1
      api_id: 57d1f7558aa04f15146d9d8a
      diagnostic_id: default
      if_match: NOT FOUND
      enabled: NOT FOUND
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


class AzureRMApiDiagnostic(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Diagnostic resource"""

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
            api_id=dict(
                type='str',
                required=True
            ),
            diagnostic_id=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            enabled=dict(
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
        self.api_id = None
        self.diagnostic_id = None
        self.if_match = None
        self.enabled = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiDiagnostic, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_apidiagnostic()

        if not old_response:
            self.log("Api Diagnostic instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Diagnostic instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Diagnostic instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apidiagnostic()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Diagnostic instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apidiagnostic()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apidiagnostic():
                time.sleep(20)
        else:
            self.log("Api Diagnostic instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_apidiagnostic(self):
        '''
        Creates or updates Api Diagnostic with the specified configuration.

        :return: deserialized Api Diagnostic instance state dictionary
        '''
        self.log("Creating / Updating the Api Diagnostic instance {0}".format(self.diagnostic_id))

        try:
            response = self.mgmt_client.api_diagnostic.create_or_update(resource_group_name=self.resource_group,
                                                                        service_name=self.name,
                                                                        api_id=self.api_id,
                                                                        diagnostic_id=self.diagnostic_id,
                                                                        enabled=self.enabled)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Diagnostic instance.')
            self.fail("Error creating the Api Diagnostic instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apidiagnostic(self):
        '''
        Deletes specified Api Diagnostic instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Diagnostic instance {0}".format(self.diagnostic_id))
        try:
            response = self.mgmt_client.api_diagnostic.delete(resource_group_name=self.resource_group,
                                                              service_name=self.name,
                                                              api_id=self.api_id,
                                                              diagnostic_id=self.diagnostic_id,
                                                              if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Api Diagnostic instance.')
            self.fail("Error deleting the Api Diagnostic instance: {0}".format(str(e)))

        return True

    def get_apidiagnostic(self):
        '''
        Gets the properties of the specified Api Diagnostic.

        :return: deserialized Api Diagnostic instance state dictionary
        '''
        self.log("Checking if the Api Diagnostic instance {0} is present".format(self.diagnostic_id))
        found = False
        try:
            response = self.mgmt_client.api_diagnostic.get(resource_group_name=self.resource_group,
                                                           service_name=self.name,
                                                           api_id=self.api_id,
                                                           diagnostic_id=self.diagnostic_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Diagnostic instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Diagnostic instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
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
    AzureRMApiDiagnostic()


if __name__ == '__main__':
    main()
