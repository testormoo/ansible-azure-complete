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
module: azure_rm_webresourcehealthmetadata_facts
version_added: "2.8"
short_description: Get Azure Resource Health Metadata facts.
description:
    - Get facts of Azure Resource Health Metadata.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Name of web app.
    slot:
        description:
            - Name of web app slot. If not specified then will default to production slot.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Resource Health Metadata
    azure_rm_webresourcehealthmetadata_facts:
      resource_group: resource_group_name
      name: name
      slot: slot

  - name: List instances of Resource Health Metadata
    azure_rm_webresourcehealthmetadata_facts:
      resource_group: resource_group_name
      name: name

  - name: List instances of Resource Health Metadata
    azure_rm_webresourcehealthmetadata_facts:
      resource_group: resource_group_name
'''

RETURN = '''
resource_health_metadata:
    description: A list of dictionaries containing facts for Resource Health Metadata.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.web import WebSiteManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMResourceHealthMetadataFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            slot=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.slot = None
        super(AzureRMResourceHealthMetadataFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(WebSiteManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.name is not None and
                self.slot is not None):
            self.results['resource_health_metadata'] = self.list_by_site_slot()
        elif self.name is not None:
            self.results['resource_health_metadata'] = self.list_by_site()
        else:
            self.results['resource_health_metadata'] = self.list_by_resource_group()
        return self.results

    def list_by_site_slot(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.resource_health_metadata.list_by_site_slot(resource_group_name=self.resource_group,
                                                                                   name=self.name,
                                                                                   slot=self.slot)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ResourceHealthMetadata.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_site(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.resource_health_metadata.list_by_site(resource_group_name=self.resource_group,
                                                                              name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ResourceHealthMetadata.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.resource_health_metadata.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ResourceHealthMetadata.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMResourceHealthMetadataFacts()


if __name__ == '__main__':
    main()
