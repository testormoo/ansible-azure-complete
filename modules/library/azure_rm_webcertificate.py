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
module: azure_rm_webcertificate
version_added: "2.8"
short_description: Manage Certificate instance.
description:
    - Create, update and delete instance of Certificate.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Name of the certificate.
        required: True
    kind:
        description:
            - Kind of resource.
    location:
        description:
            - Resource Location.
            - Required when C(state) is I(present).
    host_names:
        description:
            - Host names the certificate applies to.
        type: list
    pfx_blob:
        description:
            - Pfx blob.
    password:
        description:
            - Certificate password.
    key_vault_id:
        description:
            - Key Vault Csm resource Id.
    key_vault_secret_name:
        description:
            - Key Vault secret name.
    server_farm_id:
        description:
            - "Resource ID of the associated App Service plan, formatted as:
               '/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}'."
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
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Certificate
    azure_rm_webcertificate:
      resource_group: testrg123
      name: testc6282
      location: East US
      host_names:
        - [
  "ServerCert"
]
      password: SWsSsd__233$Sdsds#%Sd!
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: /subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testrg123/providers/Microsoft.Web/certificates/testc6282
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

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


class AzureRMCertificates(AzureRMModuleBase):
    """Configuration class for an Azure RM Certificate resource"""

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
            kind=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            host_names=dict(
                type='list'
            ),
            pfx_blob=dict(
                type='str'
            ),
            password=dict(
                type='str',
                no_log=True
            ),
            key_vault_id=dict(
                type='str'
            ),
            key_vault_secret_name=dict(
                type='str'
            ),
            server_farm_id=dict(
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
        self.certificate_envelope = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCertificates, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "kind":
                    self.certificate_envelope["kind"] = kwargs[key]
                elif key == "location":
                    self.certificate_envelope["location"] = kwargs[key]
                elif key == "host_names":
                    self.certificate_envelope["host_names"] = kwargs[key]
                elif key == "pfx_blob":
                    self.certificate_envelope["pfx_blob"] = kwargs[key]
                elif key == "password":
                    self.certificate_envelope["password"] = kwargs[key]
                elif key == "key_vault_id":
                    self.certificate_envelope["key_vault_id"] = kwargs[key]
                elif key == "key_vault_secret_name":
                    self.certificate_envelope["key_vault_secret_name"] = kwargs[key]
                elif key == "server_farm_id":
                    self.certificate_envelope["server_farm_id"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(WebSiteManagementClient,
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
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Certificate instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_certificate()

            self.results['changed'] = True
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
        self.log("Creating / Updating the Certificate instance {0}".format(self.name))

        try:
            response = self.mgmt_client.certificates.create_or_update(resource_group_name=self.resource_group,
                                                                      name=self.name,
                                                                      certificate_envelope=self.certificate_envelope)
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
        self.log("Deleting the Certificate instance {0}".format(self.name))
        try:
            response = self.mgmt_client.certificates.delete(resource_group_name=self.resource_group,
                                                            name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Certificate instance.')
            self.fail("Error deleting the Certificate instance: {0}".format(str(e)))

        return True

    def get_certificate(self):
        '''
        Gets the properties of the specified Certificate.

        :return: deserialized Certificate instance state dictionary
        '''
        self.log("Checking if the Certificate instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.certificates.get(resource_group_name=self.resource_group,
                                                         name=self.name)
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
    AzureRMCertificates()


if __name__ == '__main__':
    main()
