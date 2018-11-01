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
module: azure_rm_managementpartnerpartner
version_added: "2.8"
short_description: Manage Partner instance.
description:
    - Create, update and delete instance of Partner.

options:
    partner_id:
        description:
            - Id of the Partner
        required: True
    state:
      description:
        - Assert the state of the Partner.
        - Use 'present' to create or update an Partner and 'absent' to delete it.
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
  - name: Create (or update) Partner
    azure_rm_managementpartnerpartner:
      partner_id: 123456
'''

RETURN = '''
id:
    description:
        - Identifier of the partner
    returned: always
    type: str
    sample: /providers/microsoft.managementpartner/partners/123456
version:
    description:
        - This is the version.
    returned: always
    type: str
    sample: 3
state:
    description:
        - "This is the partner state. Possible values include: 'Active', 'Deleted'"
    returned: always
    type: str
    sample: Active
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.managementpartner import ACEProvisioningManagementPartnerAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPartner(AzureRMModuleBase):
    """Configuration class for an Azure RM Partner resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            partner_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.partner_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPartner, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ACEProvisioningManagementPartnerAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_partner()

        if not old_response:
            self.log("Partner instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Partner instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Partner instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Partner instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_partner()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Partner instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_partner()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_partner():
                time.sleep(20)
        else:
            self.log("Partner instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_partner(self):
        '''
        Creates or updates Partner with the specified configuration.

        :return: deserialized Partner instance state dictionary
        '''
        self.log("Creating / Updating the Partner instance {0}".format(self.partner_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.partner.create(partner_id=self.partner_id)
            else:
                response = self.mgmt_client.partner.update(partner_id=self.partner_id)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Partner instance.')
            self.fail("Error creating the Partner instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_partner(self):
        '''
        Deletes specified Partner instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Partner instance {0}".format(self.partner_id))
        try:
            response = self.mgmt_client.partner.delete(partner_id=self.partner_id)
        except CloudError as e:
            self.log('Error attempting to delete the Partner instance.')
            self.fail("Error deleting the Partner instance: {0}".format(str(e)))

        return True

    def get_partner(self):
        '''
        Gets the properties of the specified Partner.

        :return: deserialized Partner instance state dictionary
        '''
        self.log("Checking if the Partner instance {0} is present".format(self.partner_id))
        found = False
        try:
            response = self.mgmt_client.partner.get(partner_id=self.partner_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Partner instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Partner instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'version': d.get('version', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMPartner()


if __name__ == '__main__':
    main()
