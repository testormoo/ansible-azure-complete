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
module: azure_rm_managementpartnerpartner_facts
version_added: "2.8"
short_description: Get Azure Partner facts.
description:
    - Get facts of Azure Partner.

options:
    partner_id:
        description:
            - Id of the Partner
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Partner
    azure_rm_managementpartnerpartner_facts:
      partner_id: partner_id
'''

RETURN = '''
partner:
    description: A list of dictionaries containing facts for Partner.
    returned: always
    type: complex
    contains:
        etag:
            description:
                - Type of the partner
            returned: always
            type: int
            sample: 3
        id:
            description:
                - Identifier of the partner
            returned: always
            type: str
            sample: /providers/microsoft.managementpartner/partners/123456
        name:
            description:
                - Name of the partner
            returned: always
            type: str
            sample: 123456
        version:
            description:
                - This is the version.
            returned: always
            type: str
            sample: 3
        state:
            description:
                - "This is the partner state. Possible values include: 'Active', 'Deleted'"
            returned: always
            type: str
            sample: Active
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.managementpartner import ACEProvisioningManagementPartnerAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPartnerFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            partner_id=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.partner_id = None
        super(AzureRMPartnerFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ACEProvisioningManagementPartnerAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['partner'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.partner.get(partner_id=self.partner_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Partner.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'etag': d.get('etag', None),
            'id': d.get('id', None),
            'name': d.get('name', None),
            'version': d.get('version', None),
            'state': d.get('state', None)
        }
        return d


def main():
    AzureRMPartnerFacts()


if __name__ == '__main__':
    main()
