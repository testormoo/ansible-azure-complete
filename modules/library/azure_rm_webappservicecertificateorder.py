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
module: azure_rm_webappservicecertificateorder
version_added: "2.8"
short_description: Manage Azure App Service Certificate Order instance.
description:
    - Create, update and delete instance of Azure App Service Certificate Order.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    certificate_order_name:
        description:
            - Name of the certificate order.
        required: True
    kind:
        description:
            - Kind of resource.
    location:
        description:
            - Resource Location.
            - Required when C(state) is I(present).
    certificates:
        description:
            - State of the Key Vault secret.
    distinguished_name:
        description:
            - Certificate distinguished name.
    validity_in_years:
        description:
            - Duration in years (must be between 1 and 3).
    key_size:
        description:
            - Certificate key size.
    product_type:
        description:
            - Certificate product type.
        choices:
            - 'standard_domain_validated_ssl'
            - 'standard_domain_validated_wild_card_ssl'
    auto_renew:
        description:
            - <code>true</code> if the certificate should be automatically renewed when it expires; otherwise, <code>false</code>.
    csr:
        description:
            - Last CSR that was created for this order.
    state:
      description:
        - Assert the state of the App Service Certificate Order.
        - Use 'present' to create or update an App Service Certificate Order and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) App Service Certificate Order
    azure_rm_webappservicecertificateorder:
      resource_group: NOT FOUND
      certificate_order_name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: id
status:
    description:
        - "Current order status. Possible values include: 'Pendingissuance', 'Issued', 'Revoked', 'Canceled', 'Denied', 'Pendingrevocation', 'PendingRekey',
           'Unused', 'Expired', 'NotSubmitted'"
    returned: always
    type: str
    sample: status
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.web import WebSiteManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAppServiceCertificateOrder(AzureRMModuleBase):
    """Configuration class for an Azure RM App Service Certificate Order resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            certificate_order_name=dict(
                type='str',
                required=True
            ),
            kind=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            certificates=dict(
                type='dict'
            ),
            distinguished_name=dict(
                type='str'
            ),
            validity_in_years=dict(
                type='int'
            ),
            key_size=dict(
                type='int'
            ),
            product_type=dict(
                type='str',
                choices=['standard_domain_validated_ssl',
                         'standard_domain_validated_wild_card_ssl']
            ),
            auto_renew=dict(
                type='str'
            ),
            csr=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.certificate_order_name = None
        self.name = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAppServiceCertificateOrder, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                   supports_check_mode=True,
                                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.certificate_distinguished_name[key] = kwargs[key]

        dict_camelize(self.certificate_distinguished_name, ['product_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(WebSiteManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_appservicecertificateorder()

        if not old_response:
            self.log("App Service Certificate Order instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("App Service Certificate Order instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.certificate_distinguished_name, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the App Service Certificate Order instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_appservicecertificateorder()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("App Service Certificate Order instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_appservicecertificateorder()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("App Service Certificate Order instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': response.get('status', None)
                })
        return self.results

    def create_update_appservicecertificateorder(self):
        '''
        Creates or updates App Service Certificate Order with the specified configuration.

        :return: deserialized App Service Certificate Order instance state dictionary
        '''
        self.log("Creating / Updating the App Service Certificate Order instance {0}".format(self.certificate_order_name))

        try:
            response = self.mgmt_client.app_service_certificate_orders.create_or_update(resource_group_name=self.resource_group,
                                                                                        certificate_order_name=self.certificate_order_name,
                                                                                        certificate_distinguished_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the App Service Certificate Order instance.')
            self.fail("Error creating the App Service Certificate Order instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_appservicecertificateorder(self):
        '''
        Deletes specified App Service Certificate Order instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the App Service Certificate Order instance {0}".format(self.certificate_order_name))
        try:
            response = self.mgmt_client.app_service_certificate_orders.delete(resource_group_name=self.resource_group,
                                                                              certificate_order_name=self.certificate_order_name)
        except CloudError as e:
            self.log('Error attempting to delete the App Service Certificate Order instance.')
            self.fail("Error deleting the App Service Certificate Order instance: {0}".format(str(e)))

        return True

    def get_appservicecertificateorder(self):
        '''
        Gets the properties of the specified App Service Certificate Order.

        :return: deserialized App Service Certificate Order instance state dictionary
        '''
        self.log("Checking if the App Service Certificate Order instance {0} is present".format(self.certificate_order_name))
        found = False
        try:
            response = self.mgmt_client.app_service_certificate_orders.get(resource_group_name=self.resource_group,
                                                                           certificate_order_name=self.certificate_order_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("App Service Certificate Order instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the App Service Certificate Order instance.')
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


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def main():
    """Main execution"""
    AzureRMAppServiceCertificateOrder()


if __name__ == '__main__':
    main()
