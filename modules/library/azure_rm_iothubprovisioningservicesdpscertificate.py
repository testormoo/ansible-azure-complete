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
module: azure_rm_iothubprovisioningservicesdpscertificate
version_added: "2.8"
short_description: Manage Dps Certificate instance.
description:
    - Create, update and delete instance of Dps Certificate.

options:
    resource_group:
        description:
            - Resource group identifier.
        required: True
    provisioning_service_name:
        description:
            - The name of the provisioning service.
        required: True
    name:
        description:
            - The name of the I(certificate) create or update.
        required: True
    if_match:
        description:
            - ETag of the I(certificate). This is required to update an existing I(certificate), and ignored while creating a brand new I(certificate).
    certificate:
        description:
            - Base-64 representation of the X509 leaf certificate .cer file or just .pem file content.
    state:
      description:
        - Assert the state of the Dps Certificate.
        - Use 'present' to create or update an Dps Certificate and 'absent' to delete it.
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
  - name: Create (or update) Dps Certificate
    azure_rm_iothubprovisioningservicesdpscertificate:
      resource_group: myResourceGroup
      provisioning_service_name: myFirstProvisioningService
      name: cert
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
    from azure.mgmt.iothubprovisioningservices import IotDpsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDpsCertificate(AzureRMModuleBase):
    """Configuration class for an Azure RM Dps Certificate resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            provisioning_service_name=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.provisioning_service_name = None
        self.name = None
        self.if_match = None
        self.certificate = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDpsCertificate, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(IotDpsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_dpscertificate()

        if not old_response:
            self.log("Dps Certificate instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Dps Certificate instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dps Certificate instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dpscertificate()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dps Certificate instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dpscertificate()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_dpscertificate():
                time.sleep(20)
        else:
            self.log("Dps Certificate instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_dpscertificate(self):
        '''
        Creates or updates Dps Certificate with the specified configuration.

        :return: deserialized Dps Certificate instance state dictionary
        '''
        self.log("Creating / Updating the Dps Certificate instance {0}".format(self.certificatenonce))

        try:
            response = self.mgmt_client.dps_certificate.create_or_update(resource_group_name=self.resource_group,
                                                                         provisioning_service_name=self.provisioning_service_name,
                                                                         certificate_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Dps Certificate instance.')
            self.fail("Error creating the Dps Certificate instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_dpscertificate(self):
        '''
        Deletes specified Dps Certificate instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Dps Certificate instance {0}".format(self.certificatenonce))
        try:
            response = self.mgmt_client.dps_certificate.delete(resource_group_name=self.resource_group,
                                                               if_match=self.if_match,
                                                               provisioning_service_name=self.provisioning_service_name,
                                                               certificate_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Dps Certificate instance.')
            self.fail("Error deleting the Dps Certificate instance: {0}".format(str(e)))

        return True

    def get_dpscertificate(self):
        '''
        Gets the properties of the specified Dps Certificate.

        :return: deserialized Dps Certificate instance state dictionary
        '''
        self.log("Checking if the Dps Certificate instance {0} is present".format(self.certificatenonce))
        found = False
        try:
            response = self.mgmt_client.dps_certificate.get(certificate_name=self.name,
                                                            resource_group_name=self.resource_group,
                                                            provisioning_service_name=self.provisioning_service_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Dps Certificate instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Dps Certificate instance.')
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


def main():
    """Main execution"""
    AzureRMDpsCertificate()


if __name__ == '__main__':
    main()
