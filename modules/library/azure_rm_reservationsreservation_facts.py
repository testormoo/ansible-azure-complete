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
module: azure_rm_reservationsreservation_facts
version_added: "2.8"
short_description: Get Azure Reservation facts.
description:
    - Get facts of Azure Reservation.

options:
    reservation_id:
        description:
            - Id of the Reservation Item
        required: True
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
  - name: Get instance of Reservation
    azure_rm_reservationsreservation_facts:
      reservation_id: reservation_id
      reservation_order_id: reservation_order_id
'''

RETURN = '''
reservation:
    description: A list of dictionaries containing facts for Reservation.
    returned: always
    type: complex
    contains:
        location:
            description:
                - The Azure Region where the reserved resource lives.
            returned: always
            type: str
            sample: eastus
        etag:
            description:
                -
            returned: always
            type: int
            sample: 2
        id:
            description:
                - Identifier of the reservation
            returned: always
            type: str
            sample: /providers/microsoft.capacity/reservationOrders/276e7ae4-84d0-4da6-ab4b-d6b94f3557da/reservations/6ef59113-3482-40da-8d79-787f823e34bc
        name:
            description:
                - Name of the reservation
            returned: always
            type: str
            sample: 276e7ae4-84d0-4da6-ab4b-d6b94f3557da/6ef59113-3482-40da-8d79-787f823e34bc
        sku:
            description:
                -
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        -
                    returned: always
                    type: str
                    sample: Standard_DS1_v2
        properties:
            description:
                -
            returned: always
            type: complex
            sample: properties
            contains:
                quantity:
                    description:
                        - Quantity of the SKUs that are part of the Reservation.
                    returned: always
                    type: int
                    sample: 3
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.reservations import AzureReservationAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMReservationFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            reservation_id=dict(
                type='str',
                required=True
            ),
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
        self.reservation_id = None
        self.reservation_order_id = None
        super(AzureRMReservationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureReservationAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['reservation'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reservation.get(reservation_id=self.reservation_id,
                                                        reservation_order_id=self.reservation_order_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Reservation.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'location': d.get('location', None),
            'etag': d.get('etag', None),
            'id': d.get('id', None),
            'name': d.get('name', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            },
            'properties': {
                'quantity': d.get('properties', {}).get('quantity', None)
            }
        }
        return d


def main():
    AzureRMReservationFacts()


if __name__ == '__main__':
    main()
