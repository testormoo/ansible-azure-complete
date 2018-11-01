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
module: azure_rm_streamingjobsinput_facts
version_added: "2.8"
short_description: Get Azure Input facts.
description:
    - Get facts of Azure Input.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    job_name:
        description:
            - The name of the streaming job.
        required: True
    input_name:
        description:
            - The name of the input.
    select:
        description:
            - "The $select OData query parameter. This is a comma-separated list of structural properties to include in the response, or '*' to include all
               properties. By default, all properties are returned except diagnostics. Currently only accepts '*' as a valid value."

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Input
    azure_rm_streamingjobsinput_facts:
      resource_group: resource_group_name
      job_name: job_name
      input_name: input_name

  - name: List instances of Input
    azure_rm_streamingjobsinput_facts:
      select: select
      resource_group: resource_group_name
      job_name: job_name
'''

RETURN = '''
inputs:
    description: A list of dictionaries containing facts for Input.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: "/subscriptions/56b5e0a9-b645-407d-99b0-c64f86013e3d/resourceGroups/sjrg8440/providers/Microsoft.StreamAnalytics/streamingjobs/sj9597/inp
                    uts/input7225"
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: input7225
        properties:
            description:
                - The properties that are associated with an input. Required on PUT (CreateOrReplace) requests.
            returned: always
            type: complex
            sample: properties
            contains:
                serialization:
                    description:
                        - "Describes how data from an input is serialized or how data is serialized when written to an output. Required on PUT
                           (CreateOrReplace) requests."
                    returned: always
                    type: complex
                    sample: serialization
                    contains:
                        type:
                            description:
                                - Constant filled by server.
                            returned: always
                            type: str
                            sample: Csv
                type:
                    description:
                        - Constant filled by server.
                    returned: always
                    type: str
                    sample: Reference
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.streamingjobs import StreamAnalyticsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMInputsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            job_name=dict(
                type='str',
                required=True
            ),
            input_name=dict(
                type='str'
            ),
            select=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.job_name = None
        self.input_name = None
        self.select = None
        super(AzureRMInputsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StreamAnalyticsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.input_name is not None:
            self.results['inputs'] = self.get()
        else:
            self.results['inputs'] = self.list_by_streaming_job()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.inputs.get(resource_group_name=self.resource_group,
                                                   job_name=self.job_name,
                                                   input_name=self.input_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Inputs.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_streaming_job(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.inputs.list_by_streaming_job(resource_group_name=self.resource_group,
                                                                     job_name=self.job_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Inputs.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'properties': {
                'serialization': {
                    'type': d.get('properties', {}).get('serialization', {}).get('type', None)
                },
                'type': d.get('properties', {}).get('type', None)
            }
        }
        return d


def main():
    AzureRMInputsFacts()


if __name__ == '__main__':
    main()
