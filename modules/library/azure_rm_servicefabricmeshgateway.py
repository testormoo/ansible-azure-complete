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
module: azure_rm_servicefabricmeshgateway
version_added: "2.8"
short_description: Manage Gateway instance.
description:
    - Create, update and delete instance of Gateway.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    name:
        description:
            - The identity of the gateway.
        required: True
    gateway_resource_description:
        description:
            - Description for creating a Gateway resource.
        required: True
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                    - Required when C(state) is I(present).
            description:
                description:
                    - User readable description of the gateway.
            source_network:
                description:
                    - Network the gateway should listen on for requests.
                    - Required when C(state) is I(present).
                suboptions:
                    name:
                        description:
                            - Name of the network
                    endpoint_refs:
                        description:
                            - A list of endpoints that are exposed on this network.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Name of the endpoint.
            destination_network:
                description:
                    - Network that the Application is using.
                    - Required when C(state) is I(present).
                suboptions:
                    name:
                        description:
                            - Name of the network
                    endpoint_refs:
                        description:
                            - A list of endpoints that are exposed on this network.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Name of the endpoint.
            tcp:
                description:
                    - Configuration for tcp connectivity for this gateway.
                type: list
                suboptions:
                    name:
                        description:
                            - tcp gateway config name.
                            - Required when C(state) is I(present).
                    port:
                        description:
                            - Specifies the port at which the service endpoint below needs to be exposed.
                            - Required when C(state) is I(present).
                    destination:
                        description:
                            - Describes destination endpoint for routing traffic.
                            - Required when C(state) is I(present).
                        suboptions:
                            application_name:
                                description:
                                    - Name of the service fabric Mesh application.
                                    - Required when C(state) is I(present).
                            service_name:
                                description:
                                    - service that contains the endpoint.
                                    - Required when C(state) is I(present).
                            endpoint_name:
                                description:
                                    - name of the endpoint in the service.
                                    - Required when C(state) is I(present).
            http:
                description:
                    - Configuration for http connectivity for this gateway.
                type: list
                suboptions:
                    name:
                        description:
                            - http gateway config name.
                            - Required when C(state) is I(present).
                    port:
                        description:
                            - Specifies the port at which the service endpoint below needs to be exposed.
                            - Required when C(state) is I(present).
                    hosts:
                        description:
                            - description for routing.
                            - Required when C(state) is I(present).
                        type: list
                        suboptions:
                            name:
                                description:
                                    - http hostname config name.
                                    - Required when C(state) is I(present).
                            routes:
                                description:
                                    - "Route information to use for routing. Routes are processed in the order they are specified. Specify routes that are
                                       more specific before routes that can hamdle general cases."
                                    - Required when C(state) is I(present).
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - http route name.
                                            - Required when C(state) is I(present).
                                    match:
                                        description:
                                            - Describes a rule for http route matching.
                                            - Required when C(state) is I(present).
                                        suboptions:
                                            path:
                                                description:
                                                    - Path to match for routing.
                                                    - Required when C(state) is I(present).
                                            headers:
                                                description:
                                                    - headers and their values to match in request.
                                                type: list
                                    destination:
                                        description:
                                            - Describes destination endpoint for routing traffic.
                                            - Required when C(state) is I(present).
                                        suboptions:
                                            application_name:
                                                description:
                                                    - Name of the service fabric Mesh application.
                                                    - Required when C(state) is I(present).
                                            service_name:
                                                description:
                                                    - service that contains the endpoint.
                                                    - Required when C(state) is I(present).
                                            endpoint_name:
                                                description:
                                                    - name of the endpoint in the service.
                                                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Gateway.
        - Use 'present' to create or update an Gateway and 'absent' to delete it.
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
  - name: Create (or update) Gateway
    azure_rm_servicefabricmeshgateway:
      resource_group: sbz_demo
      name: sampleGateway
      gateway_resource_description:
        location: EastUS
        description: Service Fabric Mesh sample gateway.
        source_network:
          name: Open
        destination_network:
          name: helloWorldNetwork
        tcp:
          - name: web
            port: 80
            destination:
              application_name: helloWorldApp
              service_name: helloWorldService
              endpoint_name: helloWorldListener
        http:
          - name: contosoWebsite
            port: 8081
            hosts:
              - name: contoso.com
                routes:
                  - name: index
                    match:
                      path: {
  "value": "/index",
  "rewrite": "/",
  "type": "prefix"
}
                    destination:
                      application_name: httpHelloWorldApp
                      service_name: indexService
                      endpoint_name: indexHttpEndpoint
'''

RETURN = '''
id:
    description:
        - "Fully qualified identifier for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/gateways/sampleGateway
status:
    description:
        - "Status of the resource. Possible values include: 'Unknown', 'Ready', 'Upgrading', 'Creating', 'Deleting', 'Failed'"
    returned: always
    type: str
    sample: Ready
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.servicefabricmesh import ServiceFabricMeshManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGateway(AzureRMModuleBase):
    """Configuration class for an Azure RM Gateway resource"""

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
            gateway_resource_description=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.gateway_resource_description = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGateway, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.gateway_resource_description["location"] = kwargs[key]
                elif key == "description":
                    self.gateway_resource_description["description"] = kwargs[key]
                elif key == "source_network":
                    self.gateway_resource_description["source_network"] = kwargs[key]
                elif key == "destination_network":
                    self.gateway_resource_description["destination_network"] = kwargs[key]
                elif key == "tcp":
                    self.gateway_resource_description["tcp"] = kwargs[key]
                elif key == "http":
                    self.gateway_resource_description["http"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_gateway()

        if not old_response:
            self.log("Gateway instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Gateway instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Gateway instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_gateway()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Gateway instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_gateway()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_gateway():
                time.sleep(20)
        else:
            self.log("Gateway instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_gateway(self):
        '''
        Creates or updates Gateway with the specified configuration.

        :return: deserialized Gateway instance state dictionary
        '''
        self.log("Creating / Updating the Gateway instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.gateway.create(resource_group_name=self.resource_group,
                                                           gateway_resource_name=self.name,
                                                           gateway_resource_description=self.gateway_resource_description)
            else:
                response = self.mgmt_client.gateway.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Gateway instance.')
            self.fail("Error creating the Gateway instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_gateway(self):
        '''
        Deletes specified Gateway instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Gateway instance {0}".format(self.name))
        try:
            response = self.mgmt_client.gateway.delete(resource_group_name=self.resource_group,
                                                       gateway_resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Gateway instance.')
            self.fail("Error deleting the Gateway instance: {0}".format(str(e)))

        return True

    def get_gateway(self):
        '''
        Gets the properties of the specified Gateway.

        :return: deserialized Gateway instance state dictionary
        '''
        self.log("Checking if the Gateway instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.gateway.get(resource_group_name=self.resource_group,
                                                    gateway_resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Gateway instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Gateway instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
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
    AzureRMGateway()


if __name__ == '__main__':
    main()
