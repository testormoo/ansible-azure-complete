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
module: azure_rm_consumptionreservationsdetail_facts
version_added: "2.8"
short_description: Get Azure Reservations Detail facts.
description:
    - Get facts of Azure Reservations Detail.

options:
    reservation_order_id:
        description:
            - Order Id of the reservation
        required: True
    reservation_id:
        description:
            - Id of the reservation
    filter:
        description:
            - "Filter reservation details by date range. The properties/UsageDate for start date and end date. The filter supports 'le' and  'ge' "
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Reservations Detail
    azure_rm_consumptionreservationsdetail_facts:
      reservation_order_id: reservation_order_id
      reservation_id: reservation_id
      filter: filter

  - name: List instances of Reservations Detail
    azure_rm_consumptionreservationsdetail_facts:
      reservation_order_id: reservation_order_id
      filter: filter
'''

RETURN = '''
reservations_details:
    description: A list of dictionaries containing facts for Reservations Detail.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.consumption import ConsumptionManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMReservationsDetailsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            reservation_order_id=dict(
                type='str',
                required=True
            ),
            reservation_id=dict(
                type='str'
            ),
            filter=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.reservation_order_id = None
        self.reservation_id = None
        self.filter = None
        super(AzureRMReservationsDetailsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.reservation_id is not None:
            self.results['reservations_details'] = self.list_by_reservation_order_and_reservation()
        else:
            self.results['reservations_details'] = self.list_by_reservation_order()
        return self.results

    def list_by_reservation_order_and_reservation(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reservations_details.list_by_reservation_order_and_reservation(reservation_order_id=self.reservation_order_id,
                                                                                                       reservation_id=self.reservation_id,
                                                                                                       filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ReservationsDetails.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_reservation_order(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reservations_details.list_by_reservation_order(reservation_order_id=self.reservation_order_id,
                                                                                       filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ReservationsDetails.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMReservationsDetailsFacts()


if __name__ == '__main__':
    main()
