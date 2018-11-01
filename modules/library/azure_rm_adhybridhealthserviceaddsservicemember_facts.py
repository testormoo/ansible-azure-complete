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
module: azure_rm_adhybridhealthserviceaddsservicemember_facts
version_added: "2.8"
short_description: Get Azure Adds Service Member facts.
description:
    - Get facts of Azure Adds Service Member.

options:
    service_name:
        description:
            - The name of the service.
        required: True
    service_member_id:
        description:
            - The server Id.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Adds Service Member
    azure_rm_adhybridhealthserviceaddsservicemember_facts:
      service_name: service_name
      service_member_id: service_member_id
'''

RETURN = '''
adds_service_members:
    description: A list of dictionaries containing facts for Adds Service Member.
    returned: always
    type: complex
    contains:
        dimensions:
            description:
                - The server specific configuration related dimensions.
            returned: always
            type: str
            sample: "[\n  {\n    'key': 'key1',\n    'value': 'value1'\n  }\n]"
        disabled:
            description:
                - Indicates if the server is disabled or not.
            returned: always
            type: str
            sample: False
        properties:
            description:
                - Server specific properties.
            returned: always
            type: str
            sample: "[\n  {\n    'key': 'key1',\n    'value': 'value1'\n  }\n]"
        role:
            description:
                - The service role that is being monitored in the server.
            returned: always
            type: str
            sample: AdfsServer_30
        status:
            description:
                - The health status of the server.
            returned: always
            type: str
            sample: Healthy
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.adhybridhealthservice import ADHybridHealthService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAddsServiceMembersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            service_name=dict(
                type='str',
                required=True
            ),
            service_member_id=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.service_name = None
        self.service_member_id = None
        super(AzureRMAddsServiceMembersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ADHybridHealthService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['adds_service_members'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.adds_service_members.get(service_name=self.service_name,
                                                                 service_member_id=self.service_member_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AddsServiceMembers.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'dimensions': d.get('dimensions', None),
            'disabled': d.get('disabled', None),
            'properties': d.get('properties', None),
            'role': d.get('role', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMAddsServiceMembersFacts()


if __name__ == '__main__':
    main()
