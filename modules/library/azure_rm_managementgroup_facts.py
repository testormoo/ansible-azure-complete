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
module: azure_rm_managementgroup_facts
version_added: "2.8"
short_description: Get Azure Management Group facts.
description:
    - Get facts of Azure Management Group.

options:
    group_id:
        description:
            - Management Group ID.
        required: True
    expand:
        description:
            - The $expand=children query string parameter allows clients to request inclusion of children in the response payload.
    recurse:
        description:
            - "The $recurse=true query string parameter allows clients to request inclusion of entire hierarchy in the response payload. Note that
               $I(expand)=children must be passed up if $recurse is set to true."
    filter:
        description:
            - "A filter which allows the exclusion of subscriptions from results (i.e. '$filter=children.childType ne Subscription')"
    cache_control:
        description:
            - "Indicates that the request shouldn't utilize any caches."

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Management Group
    azure_rm_managementgroup_facts:
      group_id: group_id
      expand: expand
      recurse: recurse
      filter: filter
      cache_control: cache_control
'''

RETURN = '''
management_groups:
    description: A list of dictionaries containing facts for Management Group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "The fully qualified ID for the management group.  For example,
                   /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000"
            returned: always
            type: str
            sample: /providers/Microsoft.Management/managementGroups/20000000-0001-0000-0000-000000000000
        name:
            description:
                - The name of the management group. For example, 00000000-0000-0000-0000-000000000000
            returned: always
            type: str
            sample: 20000000-0001-0000-0000-000000000000
        details:
            description:
                -
            returned: always
            type: complex
            sample: details
            contains:
                version:
                    description:
                        - The version number of the object.
                    returned: always
                    type: float
                    sample: 1
                parent:
                    description:
                        -
                    returned: always
                    type: complex
                    sample: parent
                    contains:
                        id:
                            description:
                                - "The fully qualified ID for the parent management group.  For example,
                                   /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000"
                            returned: always
                            type: str
                            sample: /providers/Microsoft.Management/managementGroups/RootGroup
                        name:
                            description:
                                - The name of the parent management group
                            returned: always
                            type: str
                            sample: RootGroup
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.managementgroups import ManagementGroupsAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagementGroupFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            group_id=dict(
                type='str',
                required=True
            ),
            expand=dict(
                type='str'
            ),
            recurse=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
            cache_control=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.group_id = None
        self.expand = None
        self.recurse = None
        self.filter = None
        self.cache_control = None
        super(AzureRMManagementGroupFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ManagementGroupsAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['management_groups'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.management_groups.get(group_id=self.group_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Management Group.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'details': {
                'version': d.get('details', {}).get('version', None),
                'parent': {
                    'id': d.get('details', {}).get('parent', {}).get('id', None),
                    'name': d.get('details', {}).get('parent', {}).get('name', None)
                }
            }
        }
        return d


def main():
    AzureRMManagementGroupFacts()


if __name__ == '__main__':
    main()
