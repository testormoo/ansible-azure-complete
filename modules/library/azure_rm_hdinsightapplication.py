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
module: azure_rm_hdinsightapplication
version_added: "2.8"
short_description: Manage Azure Application instance.
description:
    - Create, update and delete instance of Azure Application.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    cluster_name:
        description:
            - The name of the cluster.
        required: True
    name:
        description:
            - The constant value for the application name.
        required: True
    compute_profile:
        description:
            - The list of roles in the cluster.
        suboptions:
            roles:
                description:
                    - The list of roles in the cluster.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the role.
                    min_instance_count:
                        description:
                            - The minimum instance count of the cluster.
                    target_instance_count:
                        description:
                            - The instance count of the cluster.
                    hardware_profile:
                        description:
                            - The hardware profile.
                        suboptions:
                            vm_size:
                                description:
                                    - The size of the VM
                    os_profile:
                        description:
                            - The operating system profile.
                        suboptions:
                            linux_operating_system_profile:
                                description:
                                    - The Linux OS profile.
                    virtual_network_profile:
                        description:
                            - The virtual network profile.
                        suboptions:
                            id:
                                description:
                                    - The ID of the virtual network.
                            subnet:
                                description:
                                    - The name of the subnet.
                    data_disks_groups:
                        description:
                            - The data disks groups for the role.
                        type: list
                        suboptions:
                            disks_per_node:
                                description:
                                    - The number of disks per node.
                    script_actions:
                        description:
                            - The list of script actions on the role.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The name of the script action.
                                    - Required when C(state) is I(present).
                            uri:
                                description:
                                    - The URI to the script.
                                    - Required when C(state) is I(present).
                            parameters:
                                description:
                                    - The parameters for the script provided.
                                    - Required when C(state) is I(present).
    install_script_actions:
        description:
            - The list of install script actions.
        type: list
        suboptions:
            name:
                description:
                    - The name of the script action.
                    - Required when C(state) is I(present).
            uri:
                description:
                    - The URI to the script.
                    - Required when C(state) is I(present).
            parameters:
                description:
                    - The parameters for the script
            roles:
                description:
                    - The list of roles where script will be executed.
                    - Required when C(state) is I(present).
                type: list
    uninstall_script_actions:
        description:
            - The list of uninstall script actions.
        type: list
        suboptions:
            name:
                description:
                    - The name of the script action.
                    - Required when C(state) is I(present).
            uri:
                description:
                    - The URI to the script.
                    - Required when C(state) is I(present).
            parameters:
                description:
                    - The parameters for the script
            roles:
                description:
                    - The list of roles where script will be executed.
                    - Required when C(state) is I(present).
                type: list
    https_endpoints:
        description:
            - The list of application HTTPS endpoints.
        type: list
        suboptions:
            additional_properties:
                description:
                    - Unmatched properties from the message are deserialized this collection
            access_modes:
                description:
                    - The list of access modes for the application.
                type: list
            location:
                description:
                    - The location of the endpoint.
            destination_port:
                description:
                    - The destination port to connect to.
            public_port:
                description:
                    - The public port to connect to.
    ssh_endpoints:
        description:
            - The list of application SSH endpoints.
        type: list
        suboptions:
            location:
                description:
                    - The location of the endpoint.
            destination_port:
                description:
                    - The destination port to connect to.
            public_port:
                description:
                    - The public port to connect to.
    application_type:
        description:
            - The application type.
    errors:
        description:
            - The list of errors.
        type: list
        suboptions:
            code:
                description:
                    - The error code.
            message:
                description:
                    - The error message.
    additional_properties:
        description:
            - The additional properties for application.
    state:
      description:
        - Assert the state of the Application.
        - Use 'present' to create or update an Application and 'absent' to delete it.
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
  - name: Create (or update) Application
    azure_rm_hdinsightapplication:
      resource_group: rg1
      cluster_name: cluster1
      name: hue
      compute_profile:
        roles:
          - name: edgenode
            target_instance_count: 1
            hardware_profile:
              vm_size: Standard_D12_v2
      install_script_actions:
        - name: app-install-app1
          uri: https://.../install.sh
          parameters: -version latest -port 20000
          roles:
            - [
  "edgenode"
]
      https_endpoints:
        - access_modes:
            - [
  "WebPage"
]
          destination_port: 20000
      application_type: CustomApplication
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource.
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
    from azure.mgmt.hdinsight import HDInsightManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApplication(AzureRMModuleBase):
    """Configuration class for an Azure RM Application resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            compute_profile=dict(
                type='dict',
                options=dict(
                    roles=dict(
                        type='list',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            min_instance_count=dict(
                                type='int'
                            ),
                            target_instance_count=dict(
                                type='int'
                            ),
                            hardware_profile=dict(
                                type='dict',
                                options=dict(
                                    vm_size=dict(
                                        type='str'
                                    )
                                )
                            ),
                            os_profile=dict(
                                type='dict',
                                options=dict(
                                    linux_operating_system_profile=dict(
                                        type='dict'
                                    )
                                )
                            ),
                            virtual_network_profile=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    subnet=dict(
                                        type='str'
                                    )
                                )
                            ),
                            data_disks_groups=dict(
                                type='list',
                                options=dict(
                                    disks_per_node=dict(
                                        type='int'
                                    )
                                )
                            ),
                            script_actions=dict(
                                type='list',
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    uri=dict(
                                        type='str'
                                    ),
                                    parameters=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            install_script_actions=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    uri=dict(
                        type='str'
                    ),
                    parameters=dict(
                        type='str'
                    ),
                    roles=dict(
                        type='list'
                    )
                )
            ),
            uninstall_script_actions=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    uri=dict(
                        type='str'
                    ),
                    parameters=dict(
                        type='str'
                    ),
                    roles=dict(
                        type='list'
                    )
                )
            ),
            https_endpoints=dict(
                type='list',
                options=dict(
                    additional_properties=dict(
                        type='dict'
                    ),
                    access_modes=dict(
                        type='list'
                    ),
                    location=dict(
                        type='str'
                    ),
                    destination_port=dict(
                        type='int'
                    ),
                    public_port=dict(
                        type='int'
                    )
                )
            ),
            ssh_endpoints=dict(
                type='list',
                options=dict(
                    location=dict(
                        type='str'
                    ),
                    destination_port=dict(
                        type='int'
                    ),
                    public_port=dict(
                        type='int'
                    )
                )
            ),
            application_type=dict(
                type='str'
            ),
            errors=dict(
                type='list',
                options=dict(
                    code=dict(
                        type='str'
                    ),
                    message=dict(
                        type='str'
                    )
                )
            ),
            additional_properties=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.cluster_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApplication, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['compute_profile', 'roles', 'virtual_network_profile', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_expand(self.parameters, ['compute_profile'])
        dict_expand(self.parameters, ['install_script_actions'])
        dict_expand(self.parameters, ['uninstall_script_actions'])
        dict_expand(self.parameters, ['https_endpoints'])
        dict_expand(self.parameters, ['ssh_endpoints'])
        dict_expand(self.parameters, ['application_type'])
        dict_expand(self.parameters, ['errors'])
        dict_expand(self.parameters, ['additional_properties'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(HDInsightManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_application()

        if not old_response:
            self.log("Application instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Application instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Application instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_application()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Application instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_application()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Application instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_application(self):
        '''
        Creates or updates Application with the specified configuration.

        :return: deserialized Application instance state dictionary
        '''
        self.log("Creating / Updating the Application instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.applications.create(resource_group_name=self.resource_group,
                                                                cluster_name=self.cluster_name,
                                                                application_name=self.name,
                                                                parameters=self.parameters)
            else:
                response = self.mgmt_client.applications.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Application instance.')
            self.fail("Error creating the Application instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_application(self):
        '''
        Deletes specified Application instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Application instance {0}".format(self.name))
        try:
            response = self.mgmt_client.applications.delete(resource_group_name=self.resource_group,
                                                            cluster_name=self.cluster_name,
                                                            application_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Application instance.')
            self.fail("Error deleting the Application instance: {0}".format(str(e)))

        return True

    def get_application(self):
        '''
        Gets the properties of the specified Application.

        :return: deserialized Application instance state dictionary
        '''
        self.log("Checking if the Application instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.applications.get(resource_group_name=self.resource_group,
                                                         cluster_name=self.cluster_name,
                                                         application_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Application instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Application instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMApplication()


if __name__ == '__main__':
    main()
