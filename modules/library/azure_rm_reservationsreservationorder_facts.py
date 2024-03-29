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
module: azure_rm_reservationsreservationorder_facts
version_added: "2.8"
short_description: Get Azure Reservation Order facts.
description:
    - Get facts of Azure Reservation Order.

options:
    reservation_order_id:
        description:
            - Order Id of the reservation
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Reservation Order
    azure_rm_reservationsreservationorder_facts:
      reservation_order_id: reservation_order_id
'''

RETURN = '''
reservation_order:
    description: A list of dictionaries containing facts for Reservation Order.
    returned: always
    type: complex
    contains:
        etag:
            description:
                -
            returned: always
            type: int
            sample: 7
        id:
            description:
                - Identifier of the reservation
            returned: always
            type: str
            sample: /providers/microsoft.capacity/reservationOrders/1f14354c-dc12-4c8d-8090-6f295a3a34aa
        name:
            description:
                - Name of the reservation
            returned: always
            type: str
            sample: 1f14354c-dc12-4c8d-8090-6f295a3a34aa
        term:
            description:
                - "Possible values include: 'P1Y', 'P3Y'"
            returned: always
            type: str
            sample: P1Y
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.reservations import AzureReservationAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMReservationOrderFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            reservation_order_id=dict(
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
        super(AzureRMReservationOrderFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureReservationAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['reservation_order'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reservation_order.get(reservation_order_id=self.reservation_order_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Reservation Order.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'etag': d.get('etag', None),
            'id': d.get('id', None),
            'name': d.get('name', None),
            'term': d.get('term', None)
        }
        return d


def main():
    AzureRMReservationOrderFacts()


if __name__ == '__main__':
    main()
