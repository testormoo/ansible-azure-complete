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
module: azure_rm_datafactorypipelinerun_facts
version_added: "2.8"
short_description: Get Azure Pipeline Run facts.
description:
    - Get facts of Azure Pipeline Run.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    name:
        description:
            - The factory name.
        required: True
    run_id:
        description:
            - The pipeline run identifier.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Pipeline Run
    azure_rm_datafactorypipelinerun_facts:
      resource_group: resource_group_name
      name: factory_name
      run_id: run_id
'''

RETURN = '''
pipeline_runs:
    description: A list of dictionaries containing facts for Pipeline Run.
    returned: always
    type: complex
    contains:
        parameters:
            description:
                - The full or partial list of parameter name, value pair used in the pipeline run.
            returned: always
            type: complex
            sample: "{\n  'OutputBlobNameList': '[\'exampleoutput.csv\']'\n}"
        status:
            description:
                - The status of a pipeline run.
            returned: always
            type: str
            sample: Succeeded
        message:
            description:
                - The message from a pipeline run.
            returned: always
            type: str
            sample: message
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPipelineRunFacts(AzureRMModuleBase):
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
            run_id=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.run_id = None
        super(AzureRMPipelineRunFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['pipeline_runs'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.pipeline_runs.get(resource_group_name=self.resource_group,
                                                          factory_name=self.name,
                                                          run_id=self.run_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Pipeline Run.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'parameters': d.get('parameters', None),
            'status': d.get('status', None),
            'message': d.get('message', None)
        }
        return d


def main():
    AzureRMPipelineRunFacts()


if __name__ == '__main__':
    main()
