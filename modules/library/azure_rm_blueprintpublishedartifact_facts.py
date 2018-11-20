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
module: azure_rm_blueprintpublishedartifact_facts
version_added: "2.8"
short_description: Get Azure Published Artifact facts.
description:
    - Get facts of Azure Published Artifact.

options:
    management_group_name:
        description:
            - ManagementGroup where blueprint stores.
        required: True
    blueprint_name:
        description:
            - name of the blueprint.
        required: True
    version_id:
        description:
            - version of the published blueprint.
        required: True
    name:
        description:
            - name of the artifact.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Published Artifact
    azure_rm_blueprintpublishedartifact_facts:
      management_group_name: management_group_name
      blueprint_name: blueprint_name
      version_id: version_id
      name: artifact_name
'''

RETURN = '''
published_artifacts:
    description: A list of dictionaries containing facts for Published Artifact.
    returned: always
    type: complex
    contains:
        id:
            description:
                - String Id used to locate any resource on Azure.
            returned: always
            type: str
            sample: "/providers/Microsoft.Management/managementGroups/ContosoOnlineGroup/providers/Microsoft.Blueprint/blueprints/simpleBlueprint/versions/V2
                    /artifacts/storageTemplate"
        name:
            description:
                - Name of this resource.
            returned: always
            type: str
            sample: storageTemplate
        kind:
            description:
                - Constant filled by server.
            returned: always
            type: str
            sample: template
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.blueprint import BlueprintManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPublishedArtifactsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            management_group_name=dict(
                type='str',
                required=True
            ),
            blueprint_name=dict(
                type='str',
                required=True
            ),
            version_id=dict(
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
        self.blueprint_name = None
        self.version_id = None
        self.name = None
        super(AzureRMPublishedArtifactsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(BlueprintManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['published_artifacts'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.published_artifacts.get(management_group_name=self.management_group_name,
                                                                blueprint_name=self.blueprint_name,
                                                                version_id=self.version_id,
                                                                artifact_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for PublishedArtifacts.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'kind': d.get('kind', None)
        }
        return d


def main():
    AzureRMPublishedArtifactsFacts()


if __name__ == '__main__':
    main()
