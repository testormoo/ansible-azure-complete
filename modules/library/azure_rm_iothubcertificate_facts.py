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
module: azure_rm_iothubcertificate_facts
version_added: "2.8"
short_description: Get Azure Certificate facts.
description:
    - Get facts of Azure Certificate.

options:
    resource_group:
        description:
            - The name of the resource group that contains the IoT hub.
        required: True
    resource_name:
        description:
            - The name of the IoT hub.
        required: True
    name:
        description:
            - The name of the certificate

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Certificate
    azure_rm_iothubcertificate_facts:
      resource_group: resource_group_name
      resource_name: resource_name
      name: certificate_name

  - name: List instances of Certificate
    azure_rm_iothubcertificate_facts:
      resource_group: resource_group_name
      resource_name: resource_name
'''

RETURN = '''
certificates:
    description: A list of dictionaries containing facts for Certificate.
    returned: always
    type: complex
    contains:
        properties:
            description:
                -
            returned: always
            type: complex
            sample: properties
            contains:
                subject:
                    description:
                        - "The certificate's subject name."
                    returned: always
                    type: str
                    sample: CN=testdevice1
                expiry:
                    description:
                        - "The certificate's expiration date and time."
                    returned: always
                    type: datetime
                    sample: "Sat, 31 Dec 2039 23:59:59 GMT"
                thumbprint:
                    description:
                        - "The certificate's thumbprint."
                    returned: always
                    type: str
                    sample: 97388663832D0393C9246CAB4FBA2C8677185A25
                created:
                    description:
                        - "The certificate's create date and time."
                    returned: always
                    type: datetime
                    sample: "Thu, 12 Oct 2017 19:23:50 GMT"
                updated:
                    description:
                        - "The certificate's last update date and time."
                    returned: always
                    type: datetime
                    sample: "Thu, 12 Oct 2017 19:23:50 GMT"
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/91d12660-3dec-467a-be2a-213b5544ddc0/resourceGroups/myResourceGroup/providers/Microsoft.Devices/IotHubs/andbuc-hub/certif
                    icates/cert"
        name:
            description:
                - The name of the certificate.
            returned: always
            type: str
            sample: cert
        etag:
            description:
                - The entity tag.
            returned: always
            type: str
            sample: AAAAAAExpNs=
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.iothub import IotHubClient
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
            resource_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.resource_name = None
        self.name = None
        super(AzureRMCertificateFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(IotHubClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['certificates'] = self.get()
        else:
            self.results['certificates'] = self.list_by_iot_hub()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.certificates.get(resource_group_name=self.resource_group,
                                                         resource_name=self.resource_name,
                                                         certificate_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Certificate.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_iot_hub(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.certificates.list_by_iot_hub(resource_group_name=self.resource_group,
                                                                     resource_name=self.resource_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Certificate.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'properties': {
                'subject': d.get('properties', {}).get('subject', None),
                'expiry': d.get('properties', {}).get('expiry', None),
                'thumbprint': d.get('properties', {}).get('thumbprint', None),
                'created': d.get('properties', {}).get('created', None),
                'updated': d.get('properties', {}).get('updated', None)
            },
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMCertificateFacts()


if __name__ == '__main__':
    main()
