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
module: azure_rm_datamigrationfile_facts
version_added: "2.8"
short_description: Get Azure File facts.
description:
    - Get facts of Azure File.

options:
    group_name:
        description:
            - Name of the resource group
        required: True
    service_name:
        description:
            - Name of the service
        required: True
    project_name:
        description:
            - Name of the project
        required: True
    file_name:
        description:
            - Name of the File
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of File
    azure_rm_datamigrationfile_facts:
      group_name: group_name
      service_name: service_name
      project_name: project_name
      file_name: file_name
'''

RETURN = '''
files:
    description: A list of dictionaries containing facts for File.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/fc04246f-04c5-437e-ac5e-206a19e7193f/resourceGroups/DmsSdkRg/providers/Microsoft.DataMigration/services/DmsSdkService/pro
                    jects/DmsSdkProject/files/x114d023d8"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: x114d023d8
        properties:
            description:
                - Custom file properties
            returned: always
            type: complex
            sample: properties
            contains:
                extension:
                    description:
                        - Optional File extension. If submitted it should not have a leading period and must match the extension from filePath.
                    returned: always
                    type: str
                    sample: sql
                size:
                    description:
                        - File size.
                    returned: always
                    type: int
                    sample: 51835
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datamigration import DataMigrationServiceClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMFilesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            group_name=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            project_name=dict(
                type='str',
                required=True
            ),
            file_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.group_name = None
        self.service_name = None
        self.project_name = None
        self.file_name = None
        super(AzureRMFilesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataMigrationServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['files'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.files.get(group_name=self.group_name,
                                                  service_name=self.service_name,
                                                  project_name=self.project_name,
                                                  file_name=self.file_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Files.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'properties': {
                'extension': d.get('properties', {}).get('extension', None),
                'size': d.get('properties', {}).get('size', None)
            }
        }
        return d


def main():
    AzureRMFilesFacts()


if __name__ == '__main__':
    main()
