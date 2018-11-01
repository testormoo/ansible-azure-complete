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
module: azure_rm_apimanagementbackend
version_added: "2.8"
short_description: Manage Backend instance.
description:
    - Create, update and delete instance of Backend.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    backendid:
        description:
            - Identifier of the Backend entity. Must be unique in the current API Management service instance.
        required: True
    title:
        description:
            - Backend Title.
    description:
        description:
            - Backend Description.
    resource_id:
        description:
            - Management Uri of the Resource in External System. This I(url) can be the Arm Resource Id of Logic Apps, Function Apps or Api Apps.
    service_fabric_cluster:
        description:
            - Backend Service Fabric Cluster Properties
        suboptions:
            client_certificatethumbprint:
                description:
                    - The client certificate thumbprint for the management endpoint.
                required: True
            max_partition_resolution_retries:
                description:
                    - Maximum number of retries while attempting resolve the parition.
            management_endpoints:
                description:
                    - The cluster management endpoint.
                required: True
                type: list
            server_certificate_thumbprints:
                description:
                    - Thumbprints of certificates cluster management service uses for tls communication
                type: list
            server_x509_names:
                description:
                    - Server X509 Certificate Names Collection
                type: list
                suboptions:
                    name:
                        description:
                            - Common Name of the Certificate.
                    issuer_certificate_thumbprint:
                        description:
                            - Thumbprint for the Issuer of the Certificate.
    credentials:
        description:
            - Backend Credentials Contract Properties
        suboptions:
            certificate:
                description:
                    - List of Client Certificate Thumbprint.
                type: list
            query:
                description:
                    - Query Parameter description.
            header:
                description:
                    - Header Parameter description.
            authorization:
                description:
                    - Authorization I(header) authentication
                suboptions:
                    scheme:
                        description:
                            - Authentication Scheme name.
                        required: True
                    parameter:
                        description:
                            - Authentication Parameter value.
                        required: True
    proxy:
        description:
            - Backend Proxy Contract Properties
        suboptions:
            url:
                description:
                    - WebProxy Server AbsoluteUri property which includes the entire URI stored in the Uri instance, including all fragments and query strings.
                required: True
            username:
                description:
                    - Username to connect to the WebProxy server
            password:
                description:
                    - Password to connect to the WebProxy Server
    tls:
        description:
            - Backend TLS Properties
        suboptions:
            validate_certificate_chain:
                description:
                    - Flag indicating whether SSL certificate chain validation should be done when using self-signed certificates for this backend host.
            validate_certificate_name:
                description:
                    - Flag indicating whether SSL certificate name validation should be done when using self-signed certificates for this backend host.
    url:
        description:
            - Runtime Url of the Backend.
        required: True
    protocol:
        description:
            - Backend communication protocol.
        required: True
        choices:
            - 'http'
            - 'soap'
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Backend.
        - Use 'present' to create or update an Backend and 'absent' to delete it.
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
  - name: Create (or update) Backend
    azure_rm_apimanagementbackend:
      resource_group: rg1
      service_name: apimService1
      backendid: sfbackend
      if_match: NOT FOUND
'''

RETURN = '''
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


class AzureRMBackend(AzureRMModuleBase):
    """Configuration class for an Azure RM Backend resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            backendid=dict(
                type='str',
                required=True
            ),
            title=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            resource_id=dict(
                type='str'
            ),
            service_fabric_cluster=dict(
                type='dict'
            ),
            credentials=dict(
                type='dict'
            ),
            proxy=dict(
                type='dict'
            ),
            tls=dict(
                type='dict'
            ),
            url=dict(
                type='str',
                required=True
            ),
            protocol=dict(
                type='str',
                choices=['http',
                         'soap'],
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.service_name = None
        self.backendid = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBackend, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "title":
                    self.parameters["title"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "resource_id":
                    self.parameters["resource_id"] = kwargs[key]
                elif key == "service_fabric_cluster":
                    self.parameters.setdefault("properties", {})["service_fabric_cluster"] = kwargs[key]
                elif key == "credentials":
                    self.parameters["credentials"] = kwargs[key]
                elif key == "proxy":
                    self.parameters["proxy"] = kwargs[key]
                elif key == "tls":
                    self.parameters["tls"] = kwargs[key]
                elif key == "url":
                    self.parameters["url"] = kwargs[key]
                elif key == "protocol":
                    self.parameters["protocol"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_backend()

        if not old_response:
            self.log("Backend instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Backend instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Backend instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Backend instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_backend()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Backend instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_backend()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_backend():
                time.sleep(20)
        else:
            self.log("Backend instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_backend(self):
        '''
        Creates or updates Backend with the specified configuration.

        :return: deserialized Backend instance state dictionary
        '''
        self.log("Creating / Updating the Backend instance {0}".format(self.backendid))

        try:
            response = self.mgmt_client.backend.create_or_update(resource_group_name=self.resource_group,
                                                                 service_name=self.service_name,
                                                                 backendid=self.backendid,
                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Backend instance.')
            self.fail("Error creating the Backend instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_backend(self):
        '''
        Deletes specified Backend instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Backend instance {0}".format(self.backendid))
        try:
            response = self.mgmt_client.backend.delete(resource_group_name=self.resource_group,
                                                       service_name=self.service_name,
                                                       backendid=self.backendid,
                                                       if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Backend instance.')
            self.fail("Error deleting the Backend instance: {0}".format(str(e)))

        return True

    def get_backend(self):
        '''
        Gets the properties of the specified Backend.

        :return: deserialized Backend instance state dictionary
        '''
        self.log("Checking if the Backend instance {0} is present".format(self.backendid))
        found = False
        try:
            response = self.mgmt_client.backend.get(resource_group_name=self.resource_group,
                                                    service_name=self.service_name,
                                                    backendid=self.backendid)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Backend instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Backend instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMBackend()


if __name__ == '__main__':
    main()
