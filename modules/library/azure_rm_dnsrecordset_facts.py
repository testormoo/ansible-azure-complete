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
module: azure_rm_dnsrecordset_facts
version_added: "2.8"
short_description: Get Azure Record Set facts.
description:
    - Get facts of Azure Record Set.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    zone_name:
        description:
            - The name of the DNS zone (without a terminating dot).
        required: True
    record_type:
        description:
            - The type of record sets to enumerate.
    top:
        description:
            - The maximum number of record sets to return. If not specified, returns up to 100 record sets.
    recordsetnamesuffix:
        description:
            - "The suffix label of the record set name that has to be used to filter the record set enumerations. If this parameter is specified,
               Enumeration will return only records that end with .<recordSetNameSuffix>"
    name:
        description:
            - The name of the record set, relative to the name of the zone.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Record Set
    azure_rm_dnsrecordset_facts:
      resource_group: resource_group_name
      zone_name: zone_name
      record_type: record_type
      top: top
      recordsetnamesuffix: recordsetnamesuffix

  - name: Get instance of Record Set
    azure_rm_dnsrecordset_facts:
      resource_group: resource_group_name
      zone_name: zone_name
      name: relative_record_set_name
      record_type: record_type

  - name: List instances of Record Set
    azure_rm_dnsrecordset_facts:
      resource_group: resource_group_name
      zone_name: zone_name
      top: top
      recordsetnamesuffix: recordsetnamesuffix
'''

RETURN = '''
record_sets:
    description: A list of dictionaries containing facts for Record Set.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The ID of the record set.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/dnsZones/zone1/A/record1
        name:
            description:
                - The name of the record set.
            returned: always
            type: str
            sample: record1
        etag:
            description:
                - The etag of the record set.
            returned: always
            type: str
            sample: 00000000-0000-0000-0000-000000000000
        metadata:
            description:
                - The metadata attached to the record set.
            returned: always
            type: complex
            sample: "{\n  'key1': 'value1'\n}"
        fqdn:
            description:
                - Fully qualified domain name of the record set.
            returned: always
            type: str
            sample: record1.zone1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.dns import DnsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRecordSetsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            zone_name=dict(
                type='str',
                required=True
            ),
            record_type=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            recordsetnamesuffix=dict(
                type='str'
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
        self.zone_name = None
        self.record_type = None
        self.top = None
        self.recordsetnamesuffix = None
        self.name = None
        super(AzureRMRecordSetsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DnsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.record_type is not None:
            self.results['record_sets'] = self.list_by_type()
        elif (self.name is not None and
                self.record_type is not None):
            self.results['record_sets'] = self.get()
        else:
            self.results['record_sets'] = self.list_by_dns_zone()
        return self.results

    def list_by_type(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.record_sets.list_by_type(resource_group_name=self.resource_group,
                                                                 zone_name=self.zone_name,
                                                                 record_type=self.record_type)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RecordSets.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.record_sets.get(resource_group_name=self.resource_group,
                                                        zone_name=self.zone_name,
                                                        relative_record_set_name=self.name,
                                                        record_type=self.record_type)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RecordSets.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_dns_zone(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.record_sets.list_by_dns_zone(resource_group_name=self.resource_group,
                                                                     zone_name=self.zone_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RecordSets.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None),
            'metadata': d.get('metadata', None),
            'fqdn': d.get('fqdn', None)
        }
        return d


def main():
    AzureRMRecordSetsFacts()


if __name__ == '__main__':
    main()
