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
module: azure_rm_iothubcertificate
version_added: "2.8"
short_description: Manage Certificate instance.
description:
    - Create, update and delete instance of Certificate.

options:
    resource_group:
        description:
            - The name of the resource group that contains the IoT hub.
        required: True
    resource_name:
        description:
            - The name of the IoT hub.
        required: True
    certificate_name:
        description:
            - The name of the I(certificate)
        required: True
    if_match:
        description:
            - ETag of the I(certificate). Do not specify for creating a brand new I(certificate). Required to update an existing I(certificate).
    certificate:
        description:
            - base-64 representation of the X509 leaf certificate .cer file or just .pem file content.
    state:
      description:
        - Assert the state of the Certificate.
        - Use 'present' to create or update an Certificate and 'absent' to delete it.
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
  - name: Create (or update) Certificate
    azure_rm_iothubcertificate:
      resource_group: myResourceGroup
      resource_name: iothub
      certificate_name: cert
      if_match: NOT FOUND
      certificate: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: "/subscriptions/91d12660-3dec-467a-be2a-213b5544ddc0/resourceGroups/myResourceGroup/providers/Microsoft.Devices/ProvisioningServives/myFirstProvi
            sioningService/certificates/cert"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.iothub import IotHubClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMCertificates(AzureRMModuleBase):
    """Configuration class for an Azure RM Certificate resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            certificate_name=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            certificate=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.resource_name = None
        self.certificate_name = None
        self.if_match = None
        self.certificate = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCertificates, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(IotHubClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_certificate()

        if not old_response:
            self.log("Certificate instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Certificate instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Certificate instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Certificate instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_certificate()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Certificate instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_certificate()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_certificate():
                time.sleep(20)
        else:
            self.log("Certificate instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_certificate(self):
        '''
        Creates or updates Certificate with the specified configuration.

        :return: deserialized Certificate instance state dictionary
        '''
        self.log("Creating / Updating the Certificate instance {0}".format(self.certificate_name))

        try:
            response = self.mgmt_client.certificates.create_or_update(resource_group_name=self.resource_group,
                                                                      resource_name=self.resource_name,
                                                                      certificate_name=self.certificate_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Certificate instance.')
            self.fail("Error creating the Certificate instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_certificate(self):
        '''
        Deletes specified Certificate instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Certificate instance {0}".format(self.certificate_name))
        try:
            response = self.mgmt_client.certificates.delete(resource_group_name=self.resource_group,
                                                            resource_name=self.resource_name,
                                                            certificate_name=self.certificate_name,
                                                            if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Certificate instance.')
            self.fail("Error deleting the Certificate instance: {0}".format(str(e)))

        return True

    def get_certificate(self):
        '''
        Gets the properties of the specified Certificate.

        :return: deserialized Certificate instance state dictionary
        '''
        self.log("Checking if the Certificate instance {0} is present".format(self.certificate_name))
        found = False
        try:
            response = self.mgmt_client.certificates.get(resource_group_name=self.resource_group,
                                                         resource_name=self.resource_name,
                                                         certificate_name=self.certificate_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Certificate instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Certificate instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMCertificates()


if __name__ == '__main__':
    main()
