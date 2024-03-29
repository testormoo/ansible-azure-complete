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
short_description: Manage Azure Service Unit instance.
description:
    - Create, update and delete instance of Azure Service Unit.

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
    name:
        description:
            - The name of the service unit resource.
        required: True
    location:
        description:
            - The geo-location where the resource lives
            - Required when C(state) is I(present).
    target_resource_group:
        description:
            - The Azure Resource Group to which the resources in the service unit belong to or should be deployed to.
            - Required when C(state) is I(present).
    deployment_mode:
        description:
            - Describes the type of ARM deployment to be performed on the resource.
            - Required when C(state) is I(present).
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
      name: myServiceUnit
      location: centralus
      target_resource_group: myDeploymentResourceGroup
      deployment_mode: Incremental
      artifacts:
        template_artifact_source_relative_path: templates/myTopologyUnit.template.json
        parameters_artifact_source_relative_path: parameter/myTopologyUnit.parameters.json
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMServiceUnit(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            target_resource_group=dict(
                type='str'
            ),
            deployment_mode=dict(
                type='str',
                choices=['incremental',
                         'complete']
            ),
            artifacts=dict(
                type='dict',
                options=dict(
                    template_uri=dict(
                        type='str'
                    ),
                    parameters_uri=dict(
                        type='str'
                    ),
                    template_artifact_source_relative_path=dict(
                        type='str'
                    ),
                    parameters_artifact_source_relative_path=dict(
                        type='str'
                    )
                )
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
        self.name = None
        self.service_unit_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServiceUnit, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.service_unit_info[key] = kwargs[key]

        dict_camelize(self.service_unit_info, ['deployment_mode'], True)

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
                if (not default_compare(self.service_unit_info, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Service Unit instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_serviceunit()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Service Unit instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_serviceunit()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Service Unit instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_serviceunit(self):
        '''
        Creates or updates Service Unit with the specified configuration.

        :return: deserialized Service Unit instance state dictionary
        '''
        self.log("Creating / Updating the Service Unit instance {0}".format(self.name))

        try:
            response = self.mgmt_client.service_units.create_or_update(resource_group_name=self.resource_group,
                                                                       service_topology_name=self.service_topology_name,
                                                                       service_name=self.service_name,
                                                                       service_unit_name=self.name,
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
        self.log("Deleting the Service Unit instance {0}".format(self.name))
        try:
            response = self.mgmt_client.service_units.delete(resource_group_name=self.resource_group,
                                                             service_topology_name=self.service_topology_name,
                                                             service_name=self.service_name,
                                                             service_unit_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Service Unit instance.')
            self.fail("Error deleting the Service Unit instance: {0}".format(str(e)))

        return True

    def get_serviceunit(self):
        '''
        Gets the properties of the specified Service Unit.

        :return: deserialized Service Unit instance state dictionary
        '''
        self.log("Checking if the Service Unit instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.service_units.get(resource_group_name=self.resource_group,
                                                          service_topology_name=self.service_topology_name,
                                                          service_name=self.service_name,
                                                          service_unit_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Service Unit instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Service Unit instance.')
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
            else:
                key = list(old[0])[0]
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
    AzureRMServiceUnit()


if __name__ == '__main__':
    main()
