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
module: azure_rm_advisorsuppression
version_added: "2.8"
short_description: Manage Suppression instance.
description:
    - Create, update and delete instance of Suppression.

options:
    resource_uri:
        description:
            - The fully qualified Azure Resource Manager identifier of the resource to which the recommendation applies.
        required: True
    recommendation_id:
        description:
            - The recommendation ID.
        required: True
    name:
        description:
            - The name of the suppression.
        required: True
    suppression_id:
        description:
            - The GUID of the suppression.
    ttl:
        description:
            - The duration for which the suppression is valid.
    state:
      description:
        - Assert the state of the Suppression.
        - Use 'present' to create or update an Suppression and 'absent' to delete it.
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
  - name: Create (or update) Suppression
    azure_rm_advisorsuppression:
      resource_uri: resourceUri
      recommendation_id: recommendationId
      name: suppressionName1
      suppression_id: NOT FOUND
      ttl: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource ID.
    returned: always
    type: str
    sample: /resourceUri/providers/Microsoft.Advisor/recommendations/recommendationId/suppressions/suppressionName1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.advisor import AdvisorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSuppressions(AzureRMModuleBase):
    """Configuration class for an Azure RM Suppression resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_uri=dict(
                type='str',
                required=True
            ),
            recommendation_id=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            suppression_id=dict(
                type='str'
            ),
            ttl=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_uri = None
        self.recommendation_id = None
        self.name = None
        self.suppression_id = None
        self.ttl = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSuppressions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AdvisorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_suppression()

        if not old_response:
            self.log("Suppression instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Suppression instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Suppression instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Suppression instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_suppression()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Suppression instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_suppression()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_suppression():
                time.sleep(20)
        else:
            self.log("Suppression instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_suppression(self):
        '''
        Creates or updates Suppression with the specified configuration.

        :return: deserialized Suppression instance state dictionary
        '''
        self.log("Creating / Updating the Suppression instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.suppressions.create(resource_uri=self.resource_uri,
                                                                recommendation_id=self.recommendation_id,
                                                                name=self.name)
            else:
                response = self.mgmt_client.suppressions.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Suppression instance.')
            self.fail("Error creating the Suppression instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_suppression(self):
        '''
        Deletes specified Suppression instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Suppression instance {0}".format(self.name))
        try:
            response = self.mgmt_client.suppressions.delete(resource_uri=self.resource_uri,
                                                            recommendation_id=self.recommendation_id,
                                                            name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Suppression instance.')
            self.fail("Error deleting the Suppression instance: {0}".format(str(e)))

        return True

    def get_suppression(self):
        '''
        Gets the properties of the specified Suppression.

        :return: deserialized Suppression instance state dictionary
        '''
        self.log("Checking if the Suppression instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.suppressions.get(resource_uri=self.resource_uri,
                                                         recommendation_id=self.recommendation_id,
                                                         name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Suppression instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Suppression instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMSuppressions()


if __name__ == '__main__':
    main()
