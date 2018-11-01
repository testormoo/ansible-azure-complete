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
module: azure_rm_addonssupportplantype
version_added: "2.8"
short_description: Manage Support Plan Type instance.
description:
    - Create, update and delete instance of Support Plan Type.

options:
    provider_name:
        description:
            - "The support plan type. For now the only valid type is 'canonical'."
        required: True
    plan_type_name:
        description:
            - The Canonical support plan type.
        required: True
        choices:
            - 'essential'
            - 'standard'
            - 'advanced'
    state:
      description:
        - Assert the state of the Support Plan Type.
        - Use 'present' to create or update an Support Plan Type and 'absent' to delete it.
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
  - name: Create (or update) Support Plan Type
    azure_rm_addonssupportplantype:
      provider_name: Canonical
      plan_type_name: Standard
'''

RETURN = '''
id:
    description:
        - "The id of the ARM resource, e.g.
           '/subscriptions/{id}/providers/Microsoft.Addons/supportProvider/{supportProviderName}/supportPlanTypes/{planTypeName}'."
    returned: always
    type: str
    sample: subscriptions/d18d258f-bdba-4de1-8b51-e79d6c181d5e/providers/Microsoft.Addons/supportProviders/canonical/supportPlanTypes/Standard
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.addons import AzureAddonsResourceProvider
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSupportPlanTypes(AzureRMModuleBase):
    """Configuration class for an Azure RM Support Plan Type resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            provider_name=dict(
                type='str',
                required=True
            ),
            plan_type_name=dict(
                type='str',
                choices=['essential',
                         'standard',
                         'advanced'],
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.provider_name = None
        self.plan_type_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSupportPlanTypes, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureAddonsResourceProvider,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_supportplantype()

        if not old_response:
            self.log("Support Plan Type instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Support Plan Type instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Support Plan Type instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Support Plan Type instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_supportplantype()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Support Plan Type instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_supportplantype()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_supportplantype():
                time.sleep(20)
        else:
            self.log("Support Plan Type instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_supportplantype(self):
        '''
        Creates or updates Support Plan Type with the specified configuration.

        :return: deserialized Support Plan Type instance state dictionary
        '''
        self.log("Creating / Updating the Support Plan Type instance {0}".format(self.plan_type_name))

        try:
            response = self.mgmt_client.support_plan_types.create_or_update(provider_name=self.provider_name,
                                                                            plan_type_name=self.plan_type_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Support Plan Type instance.')
            self.fail("Error creating the Support Plan Type instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_supportplantype(self):
        '''
        Deletes specified Support Plan Type instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Support Plan Type instance {0}".format(self.plan_type_name))
        try:
            response = self.mgmt_client.support_plan_types.delete(provider_name=self.provider_name,
                                                                  plan_type_name=self.plan_type_name)
        except CloudError as e:
            self.log('Error attempting to delete the Support Plan Type instance.')
            self.fail("Error deleting the Support Plan Type instance: {0}".format(str(e)))

        return True

    def get_supportplantype(self):
        '''
        Gets the properties of the specified Support Plan Type.

        :return: deserialized Support Plan Type instance state dictionary
        '''
        self.log("Checking if the Support Plan Type instance {0} is present".format(self.plan_type_name))
        found = False
        try:
            response = self.mgmt_client.support_plan_types.get(provider_name=self.provider_name,
                                                               plan_type_name=self.plan_type_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Support Plan Type instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Support Plan Type instance.')
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
    AzureRMSupportPlanTypes()


if __name__ == '__main__':
    main()
