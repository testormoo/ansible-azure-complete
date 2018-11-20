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
module: azure_rm_deploymentmanagerservice
version_added: "2.8"
short_description: Manage Service instance.
description:
    - Create, update and delete instance of Service.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    service_topology_name:
        description:
            - The name of the service topology .
        required: True
    name:
        description:
            - The name of the service resource.
        required: True
    service_info:
        description:
            - The service object
        required: True
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                    - Required when C(state) is I(present).
            target_location:
                description:
                    - The Azure location to which the resources in the service belong to or should be deployed to.
                    - Required when C(state) is I(present).
            target_subscription_id:
                description:
                    - The subscription to which the resources in the service belong to or should be deployed to.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Service.
        - Use 'present' to create or update an Service and 'absent' to delete it.
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
  - name: Create (or update) Service
    azure_rm_deploymentmanagerservice:
      resource_group: myResourceGroup
      service_topology_name: myTopology
      name: myService
      service_info:
        location: centralus
        target_location: centralus
        target_subscription_id: 600c95c5-3ee5-44fe-b190-ca38a19adcd7
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


class AzureRMServices(AzureRMModuleBase):
    """Configuration class for an Azure RM Service resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            service_info=dict(
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
        self.name = None
        self.service_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServices, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.service_info["location"] = kwargs[key]
                elif key == "target_location":
                    self.service_info["target_location"] = kwargs[key]
                elif key == "target_subscription_id":
                    self.service_info["target_subscription_id"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureDeploymentManager,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_service()

        if not old_response:
            self.log("Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_service()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_service()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_service():
                time.sleep(20)
        else:
            self.log("Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_service(self):
        '''
        Creates or updates Service with the specified configuration.

        :return: deserialized Service instance state dictionary
        '''
        self.log("Creating / Updating the Service instance {0}".format(self.name))

        try:
            response = self.mgmt_client.services.create_or_update(resource_group_name=self.resource_group,
                                                                  service_topology_name=self.service_topology_name,
                                                                  service_name=self.name,
                                                                  service_info=self.service_info)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Service instance.')
            self.fail("Error creating the Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_service(self):
        '''
        Deletes specified Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Service instance {0}".format(self.name))
        try:
            response = self.mgmt_client.services.delete(resource_group_name=self.resource_group,
                                                        service_topology_name=self.service_topology_name,
                                                        service_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Service instance.')
            self.fail("Error deleting the Service instance: {0}".format(str(e)))

        return True

    def get_service(self):
        '''
        Gets the properties of the specified Service.

        :return: deserialized Service instance state dictionary
        '''
        self.log("Checking if the Service instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.services.get(resource_group_name=self.resource_group,
                                                     service_topology_name=self.service_topology_name,
                                                     service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Service instance.')
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
    AzureRMServices()


if __name__ == '__main__':
    main()
