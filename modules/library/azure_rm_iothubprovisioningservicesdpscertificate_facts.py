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
module: azure_rm_iothubprovisioningservicesdpscertificate_facts
version_added: "2.8"
short_description: Get Azure Dps Certificate facts.
description:
    - Get facts of Azure Dps Certificate.

options:
    certificate_name:
        description:
            - Name of the certificate to retrieve.
        required: True
    resource_group:
        description:
            - Resource group identifier.
        required: True
    name:
        description:
            - Name of the provisioning service the certificate is associated with.
        required: True
    if_match:
        description:
            - ETag of the certificate.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Dps Certificate
    azure_rm_iothubprovisioningservicesdpscertificate_facts:
      certificate_name: certificate_name
      resource_group: resource_group_name
      name: provisioning_service_name
      if_match: if_match
'''

RETURN = '''
dps_certificate:
    description: A list of dictionaries containing facts for Dps Certificate.
    returned: always
    type: complex
    contains:
        properties:
            description:
                - properties of a certificate
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
                        - "The certificate's creation date and time."
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
    from azure.mgmt.iothubprovisioningservices import IotDpsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDpsCertificateFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            certificate_name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.certificate_name = None
        self.resource_group = None
        self.name = None
        self.if_match = None
        super(AzureRMDpsCertificateFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(IotDpsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['dps_certificate'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dps_certificate.get(certificate_name=self.certificate_name,
                                                            resource_group_name=self.resource_group,
                                                            provisioning_service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DpsCertificate.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
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
    AzureRMDpsCertificateFacts()


if __name__ == '__main__':
    main()
