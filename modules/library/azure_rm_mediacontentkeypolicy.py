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
module: azure_rm_mediacontentkeypolicy
version_added: "2.8"
short_description: Manage Azure Content Key Policy instance.
description:
    - Create, update and delete instance of Azure Content Key Policy.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    name:
        description:
            - The Content Key Policy name.
        required: True
    description:
        description:
            - A description for the Policy.
    name:
        description:
            - The Policy Option I(description).
    configuration:
        description:
            - The key delivery configuration.
            - Required when C(state) is I(present).
        suboptions:
            odatatype:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    restriction:
        description:
            - The requirements that must be met to deliver keys with this I(configuration)
            - Required when C(state) is I(present).
        suboptions:
            odatatype:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Content Key Policy.
        - Use 'present' to create or update an Content Key Policy and 'absent' to delete it.
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
  - name: Create (or update) Content Key Policy
    azure_rm_mediacontentkeypolicy:
      resource_group: contoso
      account_name: contosomedia
      name: PolicyWithPlayReadyOptionAndOpenRestriction
      description: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso/providers/Microsoft.Media/mediaservices/contosomedia/contentKeyPolici
            es/PolicyWithClearKeyOptionAndTokenRestriction"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMContentKeyPolicy(AzureRMModuleBase):
    """Configuration class for an Azure RM Content Key Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            configuration=dict(
                type='dict',
                options=dict(
                    odatatype=dict(
                        type='str'
                    )
                )
            ),
            restriction=dict(
                type='dict',
                options=dict(
                    odatatype=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.name = None
        self.description = None
        self.options = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMContentKeyPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.options[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_contentkeypolicy()

        if not old_response:
            self.log("Content Key Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Content Key Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.options, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Content Key Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_contentkeypolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Content Key Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_contentkeypolicy()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Content Key Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_contentkeypolicy(self):
        '''
        Creates or updates Content Key Policy with the specified configuration.

        :return: deserialized Content Key Policy instance state dictionary
        '''
        self.log("Creating / Updating the Content Key Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.content_key_policies.create_or_update(resource_group_name=self.resource_group,
                                                                              account_name=self.account_name,
                                                                              content_key_policy_name=self.name,
                                                                              options=self.options)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Content Key Policy instance.')
            self.fail("Error creating the Content Key Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_contentkeypolicy(self):
        '''
        Deletes specified Content Key Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Content Key Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.content_key_policies.delete(resource_group_name=self.resource_group,
                                                                    account_name=self.account_name,
                                                                    content_key_policy_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Content Key Policy instance.')
            self.fail("Error deleting the Content Key Policy instance: {0}".format(str(e)))

        return True

    def get_contentkeypolicy(self):
        '''
        Gets the properties of the specified Content Key Policy.

        :return: deserialized Content Key Policy instance state dictionary
        '''
        self.log("Checking if the Content Key Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.content_key_policies.get(resource_group_name=self.resource_group,
                                                                 account_name=self.account_name,
                                                                 content_key_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Content Key Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Content Key Policy instance.')
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


def main():
    """Main execution"""
    AzureRMContentKeyPolicy()


if __name__ == '__main__':
    main()
