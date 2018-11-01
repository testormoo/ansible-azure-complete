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
module: azure_rm_msiuserassignedidentity_facts
version_added: "2.8"
short_description: Get Azure User Assigned Identity facts.
description:
    - Get facts of Azure User Assigned Identity.

options:
    resource_group:
        description:
            - The name of the Resource Group to which the identity belongs.
    resource_name:
        description:
            - The name of the identity resource.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of User Assigned Identity
    azure_rm_msiuserassignedidentity_facts:
      resource_group: resource_group_name
      resource_name: resource_name

  - name: List instances of User Assigned Identity
    azure_rm_msiuserassignedidentity_facts:
      resource_group: resource_group_name

  - name: List instances of User Assigned Identity
    azure_rm_msiuserassignedidentity_facts:
'''

RETURN = '''
user_assigned_identities:
    description: A list of dictionaries containing facts for User Assigned Identity.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The id of the created identity.
            returned: always
            type: str
            sample: /subscriptions/subid/resourcegroups/rgName/providers/Microsoft.ManagedIdentity/userAssignedIdentities/identityName
        name:
            description:
                - The name of the created identity.
            returned: always
            type: str
            sample: identityName
        location:
            description:
                - The Azure region where the identity lives.
            returned: always
            type: str
            sample: cus
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'key1': 'value1',\n  'key2': 'value2'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.msi import ManagedServiceIdentityClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMUserAssignedIdentitiesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            resource_name=dict(
                type='str'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.resource_name = None
        self.tags = None
        super(AzureRMUserAssignedIdentitiesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ManagedServiceIdentityClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.resource_name is not None):
            self.results['user_assigned_identities'] = self.get()
        elif self.resource_group is not None:
            self.results['user_assigned_identities'] = self.list_by_resource_group()
        else:
            self.results['user_assigned_identities'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.user_assigned_identities.get(resource_group_name=self.resource_group,
                                                                     resource_name=self.resource_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UserAssignedIdentities.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.user_assigned_identities.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UserAssignedIdentities.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.user_assigned_identities.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UserAssignedIdentities.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMUserAssignedIdentitiesFacts()


if __name__ == '__main__':
    main()
