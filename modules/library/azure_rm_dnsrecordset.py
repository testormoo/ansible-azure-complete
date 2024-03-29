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
module: azure_rm_dnsrecordset
version_added: "2.8"
short_description: Manage Azure Record Set instance.
description:
    - Create, update and delete instance of Azure Record Set.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    zone_name:
        description:
            - The name of the DNS zone (without C(a) terminating dot).
        required: True
    name:
        description:
            - The name of the record set, relative to the name of the zone.
        required: True
    record_type:
        description:
            - "The type of DNS record in this record set. Record sets of type C(soa) can be updated but not created (they are created when the DNS zone is
               created)."
        required: True
        choices:
            - 'a'
            - 'aaaa'
            - 'caa'
            - 'cname'
            - 'mx'
            - 'ns'
            - 'ptr'
            - 'soa'
            - 'srv'
            - 'txt'
    metadata:
        description:
            - The metadata attached to the record set.
    ttl:
        description:
            - The TTL (time-to-live) of the records in the record set.
    target_resource:
        description:
            - C(a) reference to an azure resource from where the dns resource value is taken.
        suboptions:
            id:
                description:
                    - Resource Id.
    arecords:
        description:
            - The list of C(a) records in the record set.
        type: list
        suboptions:
            ipv4_address:
                description:
                    - The IPv4 address of this A record.
    aaaa_records:
        description:
            - The list of C(aaaa) records in the record set.
        type: list
        suboptions:
            ipv6_address:
                description:
                    - The IPv6 address of this AAAA record.
    mx_records:
        description:
            - The list of C(mx) records in the record set.
        type: list
        suboptions:
            preference:
                description:
                    - The preference value for this MX record.
            exchange:
                description:
                    - The domain name of the mail host for this MX record.
    ns_records:
        description:
            - The list of C(ns) records in the record set.
        type: list
        suboptions:
            nsdname:
                description:
                    - The name server name for this NS record.
    ptr_records:
        description:
            - The list of C(ptr) records in the record set.
        type: list
        suboptions:
            ptrdname:
                description:
                    - The PTR target domain name for this PTR record.
    srv_records:
        description:
            - The list of C(srv) records in the record set.
        type: list
        suboptions:
            priority:
                description:
                    - The priority value for this SRV record.
            weight:
                description:
                    - The weight value for this SRV record.
            port:
                description:
                    - The port value for this SRV record.
            target:
                description:
                    - The target domain name for this SRV record.
    txt_records:
        description:
            - The list of C(txt) records in the record set.
        type: list
        suboptions:
            value:
                description:
                    - The text value of this TXT record.
                type: list
    cname_record:
        description:
            - The C(cname) record in the  record set.
        suboptions:
            cname:
                description:
                    - The canonical name for this CNAME record.
    soa_record:
        description:
            - The C(soa) record in the record set.
        suboptions:
            host:
                description:
                    - The domain name of the authoritative name server for this SOA record.
            email:
                description:
                    - The email contact for this SOA record.
            serial_number:
                description:
                    - The serial number for this SOA record.
            refresh_time:
                description:
                    - The refresh value for this SOA record.
            retry_time:
                description:
                    - The retry time for this SOA record.
            expire_time:
                description:
                    - The expire time for this SOA record.
            minimum_ttl:
                description:
                    - The minimum value for this SOA record. By convention this is used to determine the negative caching duration.
    caa_records:
        description:
            - The list of C(caa) records in the record set.
        type: list
        suboptions:
            flags:
                description:
                    - The flags for this CAA record as an integer between 0 and 255.
            tag:
                description:
                    - The tag for this CAA record.
            value:
                description:
                    - The value for this CAA record.
    if_match:
        description:
            - "The etag of the record set. Omit this value to always overwrite the current record set. Specify the last-seen etag value to prevent
               accidentally overwritting any concurrent changes."
    if_none_match:
        description:
            - "Set to '*' to allow C(a) new record set to be created, but to prevent updating an existing record set. Other values will be ignored."
    state:
      description:
        - Assert the state of the Record Set.
        - Use 'present' to create or update an Record Set and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Record Set
    azure_rm_dnsrecordset:
      resource_group: rg1
      zone_name: zone1
      name: record1
      record_type: A
      metadata: {
  "key1": "value1"
}
      ttl: 3600
      arecords:
        - ipv4_address: 127.0.0.1
      if_match: NOT FOUND
      if_none_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The ID of the record set.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/dnsZones/zone1/A/record1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.dns import DnsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRecordSet(AzureRMModuleBase):
    """Configuration class for an Azure RM Record Set resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            zone_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            record_type=dict(
                type='str',
                choices=['a',
                         'aaaa',
                         'caa',
                         'cname',
                         'mx',
                         'ns',
                         'ptr',
                         'soa',
                         'srv',
                         'txt'],
                required=True
            ),
            metadata=dict(
                type='dict'
            ),
            ttl=dict(
                type='int'
            ),
            target_resource=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            arecords=dict(
                type='list',
                options=dict(
                    ipv4_address=dict(
                        type='str'
                    )
                )
            ),
            aaaa_records=dict(
                type='list',
                options=dict(
                    ipv6_address=dict(
                        type='str'
                    )
                )
            ),
            mx_records=dict(
                type='list',
                options=dict(
                    preference=dict(
                        type='int'
                    ),
                    exchange=dict(
                        type='str'
                    )
                )
            ),
            ns_records=dict(
                type='list',
                options=dict(
                    nsdname=dict(
                        type='str'
                    )
                )
            ),
            ptr_records=dict(
                type='list',
                options=dict(
                    ptrdname=dict(
                        type='str'
                    )
                )
            ),
            srv_records=dict(
                type='list',
                options=dict(
                    priority=dict(
                        type='int'
                    ),
                    weight=dict(
                        type='int'
                    ),
                    port=dict(
                        type='int'
                    ),
                    target=dict(
                        type='str'
                    )
                )
            ),
            txt_records=dict(
                type='list',
                options=dict(
                    value=dict(
                        type='list'
                    )
                )
            ),
            cname_record=dict(
                type='dict',
                options=dict(
                    cname=dict(
                        type='str'
                    )
                )
            ),
            soa_record=dict(
                type='dict',
                options=dict(
                    host=dict(
                        type='str'
                    ),
                    email=dict(
                        type='str'
                    ),
                    serial_number=dict(
                        type='int'
                    ),
                    refresh_time=dict(
                        type='int'
                    ),
                    retry_time=dict(
                        type='int'
                    ),
                    expire_time=dict(
                        type='int'
                    ),
                    minimum_ttl=dict(
                        type='int'
                    )
                )
            ),
            caa_records=dict(
                type='list',
                options=dict(
                    flags=dict(
                        type='int'
                    ),
                    tag=dict(
                        type='str'
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            if_match=dict(
                type='str'
            ),
            if_none_match=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.zone_name = None
        self.name = None
        self.record_type = None
        self.parameters = dict()
        self.if_match = None
        self.if_none_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRecordSet, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['target_resource', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DnsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_recordset()

        if not old_response:
            self.log("Record Set instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Record Set instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Record Set instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_recordset()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Record Set instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_recordset()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Record Set instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_recordset(self):
        '''
        Creates or updates Record Set with the specified configuration.

        :return: deserialized Record Set instance state dictionary
        '''
        self.log("Creating / Updating the Record Set instance {0}".format(self.record_type))

        try:
            response = self.mgmt_client.record_sets.create_or_update(resource_group_name=self.resource_group,
                                                                     zone_name=self.zone_name,
                                                                     relative_record_set_name=self.name,
                                                                     record_type=self.record_type,
                                                                     parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Record Set instance.')
            self.fail("Error creating the Record Set instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_recordset(self):
        '''
        Deletes specified Record Set instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Record Set instance {0}".format(self.record_type))
        try:
            response = self.mgmt_client.record_sets.delete(resource_group_name=self.resource_group,
                                                           zone_name=self.zone_name,
                                                           relative_record_set_name=self.name,
                                                           record_type=self.record_type)
        except CloudError as e:
            self.log('Error attempting to delete the Record Set instance.')
            self.fail("Error deleting the Record Set instance: {0}".format(str(e)))

        return True

    def get_recordset(self):
        '''
        Gets the properties of the specified Record Set.

        :return: deserialized Record Set instance state dictionary
        '''
        self.log("Checking if the Record Set instance {0} is present".format(self.record_type))
        found = False
        try:
            response = self.mgmt_client.record_sets.get(resource_group_name=self.resource_group,
                                                        zone_name=self.zone_name,
                                                        relative_record_set_name=self.name,
                                                        record_type=self.record_type)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Record Set instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Record Set instance.')
        if found is True:
            return response.as_dict()

        return False


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            else:
                key = list(old[0])[0]
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMRecordSet()


if __name__ == '__main__':
    main()
