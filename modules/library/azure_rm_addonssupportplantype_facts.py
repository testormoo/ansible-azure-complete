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
module: azure_rm_addonssupportplantype_facts
version_added: "2.8"
short_description: Get Azure Support Plan Type facts.
description:
    - Get facts of Azure Support Plan Type.

options:
    provider_name:
        description:
            - "The support plan type. For now the only valid type is 'canonical'."
        required: True
    name:
        description:
            - The Canonical support plan type.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Support Plan Type
    azure_rm_addonssupportplantype_facts:
      provider_name: provider_name
      name: plan_type_name
'''

RETURN = '''
support_plan_types:
    description: A list of dictionaries containing facts for Support Plan Type.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "The id of the ARM resource, e.g.
                   '/subscriptions/{id}/providers/Microsoft.Addons/supportProvider/{supportProviderName}/supportPlanTypes/{planTypeName}'."
            returned: always
            type: str
            sample: subscriptions/d18d258f-bdba-4de1-8b51-e79d6c181d5e/providers/Microsoft.Addons/supportProviders/canonical/supportPlanTypes/Standard
        name:
            description:
                - "The name of the Canonical support plan, i.e. 'essential', 'standard' or 'advanced'."
            returned: always
            type: str
            sample: Standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.addons import AzureAddonsResourceProvider
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSupportPlanTypeFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            provider_name=dict(
                type='str',
                required=True
            ),
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
        self.provider_name = None
        self.name = None
        super(AzureRMSupportPlanTypeFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureAddonsResourceProvider,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['support_plan_types'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.support_plan_types.get(provider_name=self.provider_name,
                                                               plan_type_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Support Plan Type.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMSupportPlanTypeFacts()


if __name__ == '__main__':
    main()
