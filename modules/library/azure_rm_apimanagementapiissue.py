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
module: azure_rm_apimanagementapiissue
version_added: "2.8"
short_description: Manage Azure Api Issue instance.
description:
    - Create, update and delete instance of Azure Api Issue.

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
    issue_id:
        description:
            - Issue identifier. Must be unique in the current API Management service instance.
        required: True
    title:
        description:
            - The issue title.
            - Required when C(state) is I(present).
    description:
        description:
            - Text describing the issue.
            - Required when C(state) is I(present).
    created_date:
        description:
            - Date and time when the issue was created.
    state:
        description:
            - Status of the issue.
        choices:
            - 'proposed'
            - 'open'
            - 'removed'
            - 'resolved'
            - 'closed'
    user_id:
        description:
            - A resource identifier for the user created the issue.
            - Required when C(state) is I(present).
    api_id:
        description:
            - A resource identifier for the API the issue was created for.
    if_match:
        description:
            - "ETag of the Issue Entity. ETag should match the current entity I(state) from the header response of the GET request or it should be * for
               unconditional update."
    state:
      description:
        - Assert the state of the Api Issue.
        - Use 'present' to create or update an Api Issue and 'absent' to delete it.
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
  - name: Create (or update) Api Issue
    azure_rm_apimanagementapiissue:
      resource_group: rg1
      name: apimService1
      api_id: 57d1f7558aa04f15146d9d8a
      issue_id: 57d2ef278aa04f0ad01d6cdc
      title: New API issue
      description: New API issue description
      created_date: 2018-02-01T22:21:20.467Z
      state: open
      user_id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/users/1
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/57d1f7558aa04f15146d9d8a/issues/57d2ef278aa0
            4f0ad01d6cdc"
state:
    description:
        - "Status of the issue. Possible values include: 'proposed', 'open', 'removed', 'resolved', 'closed'"
    returned: always
    type: str
    sample: open
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMApiIssue(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Issue resource"""

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
            issue_id=dict(
                type='str',
                required=True
            ),
            title=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            created_date=dict(
                type='datetime'
            ),
            state=dict(
                type='str',
                choices=['proposed',
                         'open',
                         'removed',
                         'resolved',
                         'closed']
            ),
            user_id=dict(
                type='str'
            ),
            api_id=dict(
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
        self.name = None
        self.api_id = None
        self.issue_id = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiIssue, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_apiissue()

        if not old_response:
            self.log("Api Issue instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Issue instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Issue instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apiissue()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Issue instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apiissue()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Api Issue instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None)
                })
        return self.results

    def create_update_apiissue(self):
        '''
        Creates or updates Api Issue with the specified configuration.

        :return: deserialized Api Issue instance state dictionary
        '''
        self.log("Creating / Updating the Api Issue instance {0}".format(self.issue_id))

        try:
            response = self.mgmt_client.api_issue.create_or_update(resource_group_name=self.resource_group,
                                                                   service_name=self.name,
                                                                   api_id=self.api_id,
                                                                   issue_id=self.issue_id,
                                                                   parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Issue instance.')
            self.fail("Error creating the Api Issue instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apiissue(self):
        '''
        Deletes specified Api Issue instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Issue instance {0}".format(self.issue_id))
        try:
            response = self.mgmt_client.api_issue.delete(resource_group_name=self.resource_group,
                                                         service_name=self.name,
                                                         api_id=self.api_id,
                                                         issue_id=self.issue_id,
                                                         if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Api Issue instance.')
            self.fail("Error deleting the Api Issue instance: {0}".format(str(e)))

        return True

    def get_apiissue(self):
        '''
        Gets the properties of the specified Api Issue.

        :return: deserialized Api Issue instance state dictionary
        '''
        self.log("Checking if the Api Issue instance {0} is present".format(self.issue_id))
        found = False
        try:
            response = self.mgmt_client.api_issue.get(resource_group_name=self.resource_group,
                                                      service_name=self.name,
                                                      api_id=self.api_id,
                                                      issue_id=self.issue_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Issue instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Issue instance.')
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
    AzureRMApiIssue()


if __name__ == '__main__':
    main()
