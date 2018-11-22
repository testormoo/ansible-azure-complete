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
short_description: Manage Azure Backend instance.
description:
    - Create, update and delete instance of Azure Backend.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
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
                    - Required when C(state) is I(present).
            max_partition_resolution_retries:
                description:
                    - Maximum number of retries while attempting resolve the parition.
            management_endpoints:
                description:
                    - The cluster management endpoint.
                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
                    parameter:
                        description:
                            - Authentication Parameter value.
                            - Required when C(state) is I(present).
    proxy:
        description:
            - Backend Proxy Contract Properties
        suboptions:
            url:
                description:
                    - WebProxy Server AbsoluteUri property which includes the entire URI stored in the Uri instance, including all fragments and query strings.
                    - Required when C(state) is I(present).
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
            - Required when C(state) is I(present).
    protocol:
        description:
            - Backend communication protocol.
            - Required when C(state) is I(present).
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
      name: apimService1
      backendid: sfbackend
      description: Service Fabric Test App 1
      service_fabric_cluster:
        client_certificatethumbprint: EBA029198AA3E76EF0D70482626E5BCF148594A6
        max_partition_resolution_retries: 5
        management_endpoints:
          - [
  "https://somecluster.com"
]
        server_x509_names:
          - name: ServerCommonName1
            issuer_certificate_thumbprint: IssuerCertificateThumbprint1
      url: fabric:/mytestapp/mytestservice
      protocol: http
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
            name=dict(
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
                type='str'
            ),
            protocol=dict(
                type='str',
                choices=['http',
                         'soap']
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
        self.name = None
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

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_expand(self.parameters, ['service_fabric_cluster'])

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Backend instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_backend()

            self.results['changed'] = True
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
            self.results.update(self.format_response(response))
        return self.results

    def create_update_backend(self):
        '''
        Creates or updates Backend with the specified configuration.

        :return: deserialized Backend instance state dictionary
        '''
        self.log("Creating / Updating the Backend instance {0}".format(self.backendid))

        try:
            response = self.mgmt_client.backend.create_or_update(resource_group_name=self.resource_group,
                                                                 service_name=self.name,
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
                                                       service_name=self.name,
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
                                                    service_name=self.name,
                                                    backendid=self.backendid)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Backend instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Backend instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
        }
        return d


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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMBackend()


if __name__ == '__main__':
    main()
