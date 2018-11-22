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
module: azure_rm_eventgridtopictype_facts
version_added: "2.8"
short_description: Get Azure Topic Type facts.
description:
    - Get facts of Azure Topic Type.

options:
    name:
        description:
            - Name of the topic type
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Topic Type
    azure_rm_eventgridtopictype_facts:
      name: topic_type_name
'''

RETURN = '''
topic_types:
    description: A list of dictionaries containing facts for Topic Type.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified identifier of the resource
            returned: always
            type: str
            sample: providers/Microsoft.EventGrid/topicTypes/Microsoft.Storage.StorageAccounts
        name:
            description:
                - Name of the resource
            returned: always
            type: str
            sample: Microsoft.Storage.StorageAccounts
        provider:
            description:
                - Namespace of the provider of the topic type.
            returned: always
            type: str
            sample: Microsoft.Storage
        description:
            description:
                - Description of the topic type.
            returned: always
            type: str
            sample: Microsoft Storage service events.
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventgrid import EventGridManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTopicTypeFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.name = None
        super(AzureRMTopicTypeFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['topic_types'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.topic_types.get(topic_type_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Topic Type.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'provider': d.get('provider', None),
            'description': d.get('description', None)
        }
        return d


def main():
    AzureRMTopicTypeFacts()


if __name__ == '__main__':
    main()
