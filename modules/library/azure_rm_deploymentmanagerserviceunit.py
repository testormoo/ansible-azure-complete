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
module: azure_rm_deploymentmanagerserviceunit
version_added: "2.8"
short_description: Manage Service Unit instance.
description:
    - Create, update and delete instance of Service Unit.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    service_topology_name:
        description:
            - The name of the service topology .
        required: True
    service_name:
        description:
            - The name of the service resource.
        required: True
    service_unit_name:
        description:
            - The name of the service unit resource.
        required: True
    service_unit_info:
        description:
            - The service unit resource object.
        required: True
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                required: True
            target_resource_group:
                description:
                    - The Azure Resource Group to which the resources in the service unit belong to or should be deployed to.
                required: True
            deployment_mode:
                description:
                    - Describes the type of ARM deployment to be performed on the resource.
                required: True
                choices:
                    - 'incremental'
                    - 'complete'
            artifacts:
                description:
                    - The artifacts for the service unit.
                suboptions:
                    template_uri:
                        description:
                            - The full URI of the ARM template file with the SAS token.
                    parameters_uri:
                        description:
                            - The full URI of the ARM parameters file with the SAS token.
                    template_artifact_source_relative_path:
                        description:
                            - The path to the ARM template file relative to the artifact source.
                    parameters_artifact_source_relative_path:
                        description:
                            - The path to the ARM parameters file relative to the artifact source.
    state:
      description:
        - Assert the state of the Service Unit.
        - Use 'present' to create or update an Service Unit and 'absent' to delete it.
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
  - name: Create (or update) Service Unit
    azure_rm_deploymentmanagerserviceunit:
      resource_group: myResourceGroup
      service_topology_name: myTopology
      service_name: myService
      service_unit_name: myServiceUnit
      service_unit_info:
        location: centralus
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
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
    from azure.mgmt.deploymentmanager import AzureDeploymentManager
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMServiceUnits(AzureRMModuleBase):
    """Configuration class for an Azure RM Service Unit resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_topology_name=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            service_unit_name=dict(
                type='str',
                required=True
            ),
            service_unit_info=dict(
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
        self.service_topology_name = None
        self.service_name = None
        self.service_unit_name = None
        self.service_unit_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServiceUnits, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.service_unit_info["location"] = kwargs[key]
                elif key == "target_resource_group":
                    self.service_unit_info["target_resource_group"] = kwargs[key]
                elif key == "deployment_mode":
                    self.service_unit_info["deployment_mode"] = _snake_to_camel(kwargs[key], True)
                elif key == "artifacts":
                    self.service_unit_info["artifacts"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureDeploymentManager,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_serviceunit()

        if not old_response:
            self.log("Service Unit instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Service Unit instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Service Unit instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Service Unit instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_serviceunit()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Service Unit instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_serviceunit()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_serviceunit():
                time.sleep(20)
        else:
            self.log("Service Unit instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_serviceunit(self):
        '''
        Creates or updates Service Unit with the specified configuration.

        :return: deserialized Service Unit instance state dictionary
        '''
        self.log("Creating / Updating the Service Unit instance {0}".format(self.service_unit_name))

        try:
            response = self.mgmt_client.service_units.create_or_update(resource_group_name=self.resource_group,
                                                                       service_topology_name=self.service_topology_name,
                                                                       service_name=self.service_name,
                                                                       service_unit_name=self.service_unit_name,
                                                                       service_unit_info=self.service_unit_info)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Service Unit instance.')
            self.fail("Error creating the Service Unit instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serviceunit(self):
        '''
        Deletes specified Service Unit instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Service Unit instance {0}".format(self.service_unit_name))
        try:
            response = self.mgmt_client.service_units.delete(resource_group_name=self.resource_group,
                                                             service_topology_name=self.service_topology_name,
                                                             service_name=self.service_name,
                                                             service_unit_name=self.service_unit_name)
        except CloudError as e:
            self.log('Error attempting to delete the Service Unit instance.')
            self.fail("Error deleting the Service Unit instance: {0}".format(str(e)))

        return True

    def get_serviceunit(self):
        '''
        Gets the properties of the specified Service Unit.

        :return: deserialized Service Unit instance state dictionary
        '''
        self.log("Checking if the Service Unit instance {0} is present".format(self.service_unit_name))
        found = False
        try:
            response = self.mgmt_client.service_units.get(resource_group_name=self.resource_group,
                                                          service_topology_name=self.service_topology_name,
                                                          service_name=self.service_name,
                                                          service_unit_name=self.service_unit_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Service Unit instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Service Unit instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMServiceUnits()


if __name__ == '__main__':
    main()
