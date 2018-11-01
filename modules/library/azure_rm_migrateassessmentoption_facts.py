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
module: azure_rm_migrateassessmentoption_facts
version_added: "2.8"
short_description: Get Azure Assessment Option facts.
description:
    - Get facts of Azure Assessment Option.

options:
    location_name:
        description:
            - Azure region in which the project is created.
        required: True
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Assessment Option
    azure_rm_migrateassessmentoption_facts:
      location_name: location_name
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
assessment_options:
    description: A list of dictionaries containing facts for Assessment Option.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAssessmentOptionsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            location_name=dict(
                type='str',
                required=True
            ),
            self.config.accept_language=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.location_name = None
        self.self.config.accept_language = None
        super(AzureRMAssessmentOptionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['assessment_options'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assessment_options.get(location_name=self.location_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AssessmentOptions.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMAssessmentOptionsFacts()


if __name__ == '__main__':
    main()
