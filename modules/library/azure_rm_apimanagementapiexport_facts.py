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
module: azure_rm_apimanagementapiexport_facts
version_added: "2.8"
short_description: Get Azure Api Export facts.
description:
    - Get facts of Azure Api Export.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."
        required: True
    format:
        description:
            - Format in which to I(export) the Api Details to the Storage Blob with Sas Key valid for 5 minutes.
        required: True
    export:
        description:
            - Query parameter required to export the API details.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Api Export
    azure_rm_apimanagementapiexport_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      format: format
      export: export
'''

RETURN = '''
api_export:
    description: A list of dictionaries containing facts for Api Export.
    returned: always
    type: complex
    contains:
        link:
            description:
                - Link to the Storage Blob containing the result of the export operation. The Blob Uri is only valid for 5 minutes.
            returned: always
            type: str
            sample: "https://apimgmtstaobxxxxxxx.blob.core.windows.net/api-export/Echo
                     API.json?sv=2015-07-08&sr=b&sig=xxxxxxxxxx%3D&se=2017-09-08T21:54:08Z&sp=r"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiExportFacts(AzureRMModuleBase):
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
            api_id=dict(
                type='str',
                required=True
            ),
            format=dict(
                type='str',
                required=True
            ),
            export=dict(
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
        self.api_id = None
        self.format = None
        self.export = None
        super(AzureRMApiExportFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['api_export'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_export.get(resource_group_name=self.resource_group,
                                                       service_name=self.name,
                                                       api_id=self.api_id,
                                                       format=self.format,
                                                       export=self.export)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ApiExport.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'link': d.get('link', None)
        }
        return d


def main():
    AzureRMApiExportFacts()


if __name__ == '__main__':
    main()
