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
module: azure_rm_iothubprovisioningservicesiotdpsresource_facts
version_added: "2.8"
short_description: Get Azure Iot Dps Resource facts.
description:
    - Get facts of Azure Iot Dps Resource.

options:
    provisioning_service_name:
        description:
            - Name of the provisioning service to retrieve.
    resource_group:
        description:
            - Resource group name.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Iot Dps Resource
    azure_rm_iothubprovisioningservicesiotdpsresource_facts:
      provisioning_service_name: provisioning_service_name
      resource_group: resource_group_name

  - name: List instances of Iot Dps Resource
    azure_rm_iothubprovisioningservicesiotdpsresource_facts:
      resource_group: resource_group_name

  - name: List instances of Iot Dps Resource
    azure_rm_iothubprovisioningservicesiotdpsresource_facts:
'''

RETURN = '''
iot_dps_resource:
    description: A list of dictionaries containing facts for Iot Dps Resource.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/91d12660-3dec-467a-be2a-213b5544ddc0/resourceGroups/myResourceGroup/providers/Microsoft.Devices/ProvisioningServices/myFi
                    rstProvisioningService"
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: myFirstProvisioningService
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: {}
        etag:
            description:
                - The Etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal ETag convention.
            returned: always
            type: str
            sample: AAAAAAAADGk=
        properties:
            description:
                - Service specific properties for a provisioning service
            returned: always
            type: complex
            sample: properties
            contains:
                state:
                    description:
                        - "Current state of the provisioning service. Possible values include: 'Activating', 'Active', 'Deleting', 'Deleted',
                           'ActivationFailed', 'DeletionFailed', 'Transitioning', 'Suspending', 'Suspended', 'Resuming', 'FailingOver', 'FailoverFailed'"
                    returned: always
                    type: str
                    sample: Active
        sku:
            description:
                - Sku info for a provisioning Service.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "Sku name. Possible values include: 'S1'"
                    returned: always
                    type: str
                    sample: S1
                tier:
                    description:
                        - Pricing tier name of the provisioning service.
                    returned: always
                    type: str
                    sample: Standard
                capacity:
                    description:
                        - The number of units to provision
                    returned: always
                    type: int
                    sample: 1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.iothubprovisioningservices import IotDpsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIotDpsResourceFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            provisioning_service_name=dict(
                type='str'
            ),
            resource_group=dict(
                type='str'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.provisioning_service_name = None
        self.resource_group = None
        self.tags = None
        super(AzureRMIotDpsResourceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(IotDpsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.provisioning_service_name is not None and
                self.resource_group is not None):
            self.results['iot_dps_resource'] = self.get()
        elif self.resource_group is not None:
            self.results['iot_dps_resource'] = self.list_by_resource_group()
        else:
            self.results['iot_dps_resource'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iot_dps_resource.get(provisioning_service_name=self.provisioning_service_name,
                                                             resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iot Dps Resource.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iot_dps_resource.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iot Dps Resource.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iot_dps_resource.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iot Dps Resource.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'etag': d.get('etag', None),
            'properties': {
                'state': d.get('properties', {}).get('state', None)
            },
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            }
        }
        return d


def main():
    AzureRMIotDpsResourceFacts()


if __name__ == '__main__':
    main()
