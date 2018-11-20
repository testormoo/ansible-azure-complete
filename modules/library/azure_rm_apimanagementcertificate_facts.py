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
module: azure_rm_apimanagementcertificate_facts
version_added: "2.8"
short_description: Get Azure Certificate facts.
description:
    - Get facts of Azure Certificate.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    filter:
        description:
            - | Field          | Supported operators    | Supported functions                         |
            - |----------------|------------------------|---------------------------------------------|
            - | id             | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | subject        | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | thumbprint     | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | expirationDate | ge, le, eq, ne, gt, lt | N/A                                         |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    certificate_id:
        description:
            - Identifier of the certificate entity. Must be unique in the current API Management service instance.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Certificate
    azure_rm_apimanagementcertificate_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Certificate
    azure_rm_apimanagementcertificate_facts:
      resource_group: resource_group_name
      name: service_name
      certificate_id: certificate_id
'''

RETURN = '''
certificate:
    description: A list of dictionaries containing facts for Certificate.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/certificates/templateCert1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: templateCert1
        subject:
            description:
                - Subject attribute of the certificate.
            returned: always
            type: str
            sample: CN=mutual-authcert
        thumbprint:
            description:
                - Thumbprint of the certificate.
            returned: always
            type: str
            sample: EBA**********************8594A6
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMCertificateFacts(AzureRMModuleBase):
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
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            ),
            certificate_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.filter = None
        self.top = None
        self.skip = None
        self.certificate_id = None
        super(AzureRMCertificateFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['certificate'] = self.list_by_service()
        elif self.certificate_id is not None:
            self.results['certificate'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.certificate.list_by_service(resource_group_name=self.resource_group,
                                                                    service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Certificate.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.certificate.get(resource_group_name=self.resource_group,
                                                        service_name=self.name,
                                                        certificate_id=self.certificate_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Certificate.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'subject': d.get('subject', None),
            'thumbprint': d.get('thumbprint', None)
        }
        return d


def main():
    AzureRMCertificateFacts()


if __name__ == '__main__':
    main()
