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
module: azure_rm_apimanagementservice
version_added: "2.8"
short_description: Manage Api Management Service instance.
description:
    - Create, update and delete instance of Api Management Service.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    notification_sender_email:
        description:
            - Email address from which the notification will be sent.
    hostname_configurations:
        description:
            - Custom hostname configuration of the API Management service.
        type: list
        suboptions:
            type:
                description:
                    - I(host_name) type.
                    - Required when C(state) is I(present).
                choices:
                    - 'proxy'
                    - 'portal'
                    - 'management'
                    - 'scm'
            host_name:
                description:
                    - Hostname to configure on the Api C(management) service.
                    - Required when C(state) is I(present).
            key_vault_id:
                description:
                    - "Url to the KeyVault Secret containing the Ssl I(certificate). If absolute Url containing version is provided, auto-update of ssl
                       I(certificate) will not work. This requires Api C(management) service to be configured with MSI. The secret should be of I(type)
                       *application/x-pkcs12*"
            encoded_certificate:
                description:
                    - Base64 Encoded I(certificate).
            certificate_password:
                description:
                    - I(certificate) Password.
            default_ssl_binding:
                description:
                    - "Specify true to setup the I(certificate) associated with this I(host_name) as the Default SSL I(certificate). If a client does not
                       send the SNI header, then this will be the I(certificate) that will be challenged. The property is useful if a service has multiple
                       custom I(host_name) enabled and it needs to decide on the default ssl I(certificate). The setting only applied to C(proxy)
                       I(host_name) I(type)."
            negotiate_client_certificate:
                description:
                    - Specify true to always negotiate client I(certificate) on the I(host_name). Default Value is false.
            certificate:
                description:
                    - Certificate information.
                suboptions:
                    expiry:
                        description:
                            - "Expiration date of the certificate. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO
                               8601 standard."
                            - Required when C(state) is I(present).
                    thumbprint:
                        description:
                            - Thumbprint of the certificate.
                            - Required when C(state) is I(present).
                    subject:
                        description:
                            - Subject of the certificate.
                            - Required when C(state) is I(present).
    virtual_network_configuration:
        description:
            - Virtual network configuration of the API Management service.
        suboptions:
            subnet_resource_id:
                description:
                    - The full resource ID of a subnet in a virtual network to deploy the API Management service in.
    additional_locations:
        description:
            - Additional datacenter locations of the API Management service.
        type: list
        suboptions:
            location:
                description:
                    - The location name of the additional region among Azure Data center regions.
                    - Required when C(state) is I(present).
            sku:
                description:
                    - SKU properties of the API Management service.
                    - Required when C(state) is I(present).
                suboptions:
                    name:
                        description:
                            - Name of the Sku.
                            - Required when C(state) is I(present).
                        choices:
                            - 'developer'
                            - 'standard'
                            - 'premium'
                            - 'basic'
                    capacity:
                        description:
                            - Capacity of the SKU (number of deployed units of the SKU). The default value is 1.
            virtual_network_configuration:
                description:
                    - Virtual network configuration for the location.
                suboptions:
                    subnet_resource_id:
                        description:
                            - The full resource ID of a subnet in a virtual network to deploy the API Management service in.
    custom_properties:
        description:
            - "Custom properties of the API Management service. Setting `Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TripleDes168` will
               disable the cipher TLS_RSA_WITH_3DES_EDE_CBC_SHA for all TLS(1.0, 1.1 and 1.2). Setting
               `Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls11` can be used to disable just TLS 1.1 and setting
               `Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls10` can be used to disable TLS 1.0 on an API Management service."
    certificates:
        description:
            - List of Certificates that need to be installed in the API Management service. Max supported certificates that can be installed is 10.
        type: list
        suboptions:
            encoded_certificate:
                description:
                    - Base64 Encoded I(certificate).
            certificate_password:
                description:
                    - I(certificate) Password.
            store_name:
                description:
                    - "The System.Security.Cryptography.x509certificates.Storename I(certificate) store location. Only C(root) and C(certificate_authority)
                       are valid locations."
                    - Required when C(state) is I(present).
                choices:
                    - 'certificate_authority'
                    - 'root'
            certificate:
                description:
                    - Certificate information.
                suboptions:
                    expiry:
                        description:
                            - "Expiration date of the certificate. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO
                               8601 standard."
                            - Required when C(state) is I(present).
                    thumbprint:
                        description:
                            - Thumbprint of the certificate.
                            - Required when C(state) is I(present).
                    subject:
                        description:
                            - Subject of the certificate.
                            - Required when C(state) is I(present).
    virtual_network_type:
        description:
            - "The type of VPN in which API Managemet service needs to be configured in. C(none) (Default Value) means the API Management service is not
               part of any Virtual Network, C(external) means the API Management deployment is set up inside a Virtual Network having an Internet Facing
               Endpoint, and C(internal) means that API Management deployment is setup inside a Virtual Network having an Intranet Facing Endpoint only."
        choices:
            - 'none'
            - 'external'
            - 'internal'
    publisher_email:
        description:
            - Publisher email.
            - Required when C(state) is I(present).
    publisher_name:
        description:
            - Publisher name.
            - Required when C(state) is I(present).
    sku:
        description:
            - SKU properties of the API Management service.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - Name of the Sku.
                    - Required when C(state) is I(present).
                choices:
                    - 'developer'
                    - 'standard'
                    - 'premium'
                    - 'basic'
            capacity:
                description:
                    - Capacity of the SKU (number of deployed units of the SKU). The default value is 1.
    identity:
        description:
            - Managed service identity of the Api Management service.
        suboptions:
            type:
                description:
                    - "The identity type. Currently the only supported type is 'SystemAssigned'."
                    - Required when C(state) is I(present).
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
      description:
        - Assert the state of the Api Management Service.
        - Use 'present' to create or update an Api Management Service and 'absent' to delete it.
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
  - name: Create (or update) Api Management Service
    azure_rm_apimanagementservice:
      resource_group: rg1
      name: apimService1
      publisher_email: admin@live.com
      publisher_name: contoso
      sku:
        name: Premium
        capacity: 1
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApiManagementService(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Management Service resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            notification_sender_email=dict(
                type='str'
            ),
            hostname_configurations=dict(
                type='list'
            ),
            virtual_network_configuration=dict(
                type='dict'
            ),
            additional_locations=dict(
                type='list'
            ),
            custom_properties=dict(
                type='dict'
            ),
            certificates=dict(
                type='list'
            ),
            virtual_network_type=dict(
                type='str',
                choices=['none',
                         'external',
                         'internal']
            ),
            publisher_email=dict(
                type='str'
            ),
            publisher_name=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            identity=dict(
                type='dict'
            ),
            location=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiManagementService, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "notification_sender_email":
                    self.parameters["notification_sender_email"] = kwargs[key]
                elif key == "hostname_configurations":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'proxy':
                            ev['type'] = 'Proxy'
                        elif ev['type'] == 'portal':
                            ev['type'] = 'Portal'
                        elif ev['type'] == 'management':
                            ev['type'] = 'Management'
                        elif ev['type'] == 'scm':
                            ev['type'] = 'Scm'
                    self.parameters["hostname_configurations"] = ev
                elif key == "virtual_network_configuration":
                    self.parameters["virtual_network_configuration"] = kwargs[key]
                elif key == "additional_locations":
                    self.parameters["additional_locations"] = kwargs[key]
                elif key == "custom_properties":
                    self.parameters["custom_properties"] = kwargs[key]
                elif key == "certificates":
                    ev = kwargs[key]
                    if 'store_name' in ev:
                        if ev['store_name'] == 'certificate_authority':
                            ev['store_name'] = 'CertificateAuthority'
                        elif ev['store_name'] == 'root':
                            ev['store_name'] = 'Root'
                    self.parameters["certificates"] = ev
                elif key == "virtual_network_type":
                    self.parameters["virtual_network_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "publisher_email":
                    self.parameters["publisher_email"] = kwargs[key]
                elif key == "publisher_name":
                    self.parameters["publisher_name"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'developer':
                            ev['name'] = 'Developer'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                        elif ev['name'] == 'premium':
                            ev['name'] = 'Premium'
                        elif ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                    self.parameters["sku"] = ev
                elif key == "identity":
                    self.parameters["identity"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_apimanagementservice()

        if not old_response:
            self.log("Api Management Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Management Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Management Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apimanagementservice()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Management Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apimanagementservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apimanagementservice():
                time.sleep(20)
        else:
            self.log("Api Management Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_apimanagementservice(self):
        '''
        Creates or updates Api Management Service with the specified configuration.

        :return: deserialized Api Management Service instance state dictionary
        '''
        self.log("Creating / Updating the Api Management Service instance {0}".format(self.name))

        try:
            response = self.mgmt_client.api_management_service.create_or_update(resource_group_name=self.resource_group,
                                                                                service_name=self.name,
                                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Management Service instance.')
            self.fail("Error creating the Api Management Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apimanagementservice(self):
        '''
        Deletes specified Api Management Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Management Service instance {0}".format(self.name))
        try:
            response = self.mgmt_client.api_management_service.delete(resource_group_name=self.resource_group,
                                                                      service_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Api Management Service instance.')
            self.fail("Error deleting the Api Management Service instance: {0}".format(str(e)))

        return True

    def get_apimanagementservice(self):
        '''
        Gets the properties of the specified Api Management Service.

        :return: deserialized Api Management Service instance state dictionary
        '''
        self.log("Checking if the Api Management Service instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.api_management_service.get(resource_group_name=self.resource_group,
                                                                   service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Management Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Management Service instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMApiManagementService()


if __name__ == '__main__':
    main()
