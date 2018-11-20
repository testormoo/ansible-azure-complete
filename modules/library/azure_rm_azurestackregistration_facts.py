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
module: azure_rm_azurestackregistration_facts
version_added: "2.8"
short_description: Get Azure Registration facts.
description:
    - Get facts of Azure Registration.

options:
    resource_group:
        description:
            - Name of the resource group.
        required: True
    name:
        description:
            - Name of the Azure Stack registration.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Registration
    azure_rm_azurestackregistration_facts:
      resource_group: resource_group
      name: registration_name
'''

RETURN = '''
registrations:
    description: A list of dictionaries containing facts for Registration.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ID of the resource.
            returned: always
            type: str
            sample: /subscriptions/dd8597b4-8739-4467-8b10-f8679f62bfbf/resourceGroups/azurestack/providers/Microsoft.AzureStack/registrations/testregistration
        name:
            description:
                - Name of the resource.
            returned: always
            type: str
            sample: azurestack
        location:
            description:
                - Location of the resource.
            returned: always
            type: str
            sample: global
        tags:
            description:
                - Custom tags for the resource.
            returned: always
            type: complex
            sample: tags
        etag:
            description:
                - The entity tag used for optimistic concurency when modifying the resource.
            returned: always
            type: str
            sample: 0d00527e-0000-0000-0000-5a81ebdf0000
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.azurestack import AzureStackManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRegistrationsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
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
        self.name = None
        self.tags = None
        super(AzureRMRegistrationsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureStackManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['registrations'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.registrations.get(resource_group=self.resource_group,
                                                          registration_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Registrations.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMRegistrationsFacts()


if __name__ == '__main__':
    main()
