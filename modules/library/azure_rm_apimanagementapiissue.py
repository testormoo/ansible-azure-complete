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
short_description: Manage Api Issue instance.
description:
    - Create, update and delete instance of Api Issue.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
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
        required: True
    description:
        description:
            - Text describing the issue.
        required: True
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
        required: True
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
      service_name: apimService1
      api_id: 57d1f7558aa04f15146d9d8a
      issue_id: 57d2ef278aa04f0ad01d6cdc
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
            service_name=dict(
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
                type='str',
                required=True
            ),
            description=dict(
                type='str',
                required=True
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
                type='str',
                required=True
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
        self.service_name = None
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

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "title":
                    self.parameters["title"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "created_date":
                    self.parameters["created_date"] = kwargs[key]
                elif key == "state":
                    self.parameters["state"] = kwargs[key]
                elif key == "user_id":
                    self.parameters["user_id"] = kwargs[key]
                elif key == "api_id":
                    self.parameters["api_id"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Api Issue instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Issue instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apiissue()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Issue instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apiissue()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apiissue():
                time.sleep(20)
        else:
            self.log("Api Issue instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_apiissue(self):
        '''
        Creates or updates Api Issue with the specified configuration.

        :return: deserialized Api Issue instance state dictionary
        '''
        self.log("Creating / Updating the Api Issue instance {0}".format(self.issue_id))

        try:
            response = self.mgmt_client.api_issue.create_or_update(resource_group_name=self.resource_group,
                                                                   service_name=self.service_name,
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
                                                         service_name=self.service_name,
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
                                                      service_name=self.service_name,
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

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMApiIssue()


if __name__ == '__main__':
    main()
