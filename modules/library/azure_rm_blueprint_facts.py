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
module: azure_rm_blueprint_facts
version_added: "2.8"
short_description: Get Azure Blueprint facts.
description:
    - Get facts of Azure Blueprint.

options:
    management_group_name:
        description:
            - ManagementGroup where blueprint stores.
        required: True
    name:
        description:
            - name of the blueprint.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Blueprint
    azure_rm_blueprint_facts:
      management_group_name: management_group_name
      name: blueprint_name
'''

RETURN = '''
blueprints:
    description: A list of dictionaries containing facts for Blueprint.
    returned: always
    type: complex
    contains:
        id:
            description:
                - String Id used to locate any resource on Azure.
            returned: always
            type: str
            sample: /providers/Microsoft.Management/managementGroups/ContosoOnlineGroup/providers/Microsoft.Blueprint/blueprints/simpleBlueprint
        name:
            description:
                - Name of this resource.
            returned: always
            type: str
            sample: simpleBlueprint
        description:
            description:
                - Multi-line explain this resource.
            returned: always
            type: str
            sample: "blueprint contains all artifact kinds {'template', 'rbac', 'policy'}"
        status:
            description:
                - Status of the Blueprint. This field is readonly.
            returned: always
            type: complex
            sample: status
            contains:
        parameters:
            description:
                - Parameters required by this Blueprint definition.
            returned: always
            type: complex
            sample: "{\n  'storageAccountType': {\n    'type': 'string',\n    'metadata': {\n      'displayName': 'storage account type.'\n    }\n  },\n
                     'costCenter': {\n    'type': 'string',\n    'metadata': {\n      'displayName': 'force cost center tag for all resources under given
                     subscription.'\n    }\n  },\n  'owners': {\n    'type': 'array',\n    'metadata': {\n      'displayName': 'assign owners to
                     subscription along with blueprint assignment.'\n    }\n  }\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.blueprint import BlueprintManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBlueprintsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            management_group_name=dict(
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
        self.management_group_name = None
        self.name = None
        super(AzureRMBlueprintsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(BlueprintManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['blueprints'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.blueprints.get(management_group_name=self.management_group_name,
                                                       blueprint_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Blueprints.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None),
            'status': {
            },
            'parameters': d.get('parameters', None)
        }
        return d


def main():
    AzureRMBlueprintsFacts()


if __name__ == '__main__':
    main()
