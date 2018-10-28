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
module: azure_rm_hdinsightclusterapplication
version_added: "2.8"
short_description: Manage Application instance.
description:
    - Create, update and delete instance of Application.

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
                                suboptions:
                                    username:
                                        description:
                                            - The username.
                                    password:
                                        description:
                                            - The password.
                                    ssh_profile:
                                        description:
                                            - The SSH profile.
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
                                required: True
                            uri:
                                description:
                                    - The URI to the script.
                                required: True
                            parameters:
                                description:
                                    - The parameters for the script provided.
                                required: True
    install_script_actions:
        description:
            - The list of install script actions.
        type: list
        suboptions:
            name:
                description:
                    - The name of the script action.
                required: True
            uri:
                description:
                    - The URI to the script.
                required: True
            parameters:
                description:
                    - The parameters for the script
            roles:
                description:
                    - The list of roles where script will be executed.
                required: True
                type: list
    uninstall_script_actions:
        description:
            - The list of uninstall script actions.
        type: list
        suboptions:
            name:
                description:
                    - The name of the script action.
                required: True
            uri:
                description:
                    - The URI to the script.
                required: True
            parameters:
                description:
                    - The parameters for the script
            roles:
                description:
                    - The list of roles where script will be executed.
                required: True
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
    azure_rm_hdinsightclusterapplication:
      resource_group: rg1
      cluster_name: cluster1
      name: hue
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

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from azure.mgmt.cluster import HDInsightManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApplications(AzureRMModuleBase):
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
                type='dict'
            ),
            install_script_actions=dict(
                type='list'
            ),
            uninstall_script_actions=dict(
                type='list'
            ),
            https_endpoints=dict(
                type='list'
            ),
            ssh_endpoints=dict(
                type='list'
            ),
            application_type=dict(
                type='str'
            ),
            errors=dict(
                type='list'
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

        super(AzureRMApplications, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "compute_profile":
                    self.parameters["compute_profile"] = kwargs[key]
                elif key == "install_script_actions":
                    self.parameters["install_script_actions"] = kwargs[key]
                elif key == "uninstall_script_actions":
                    self.parameters["uninstall_script_actions"] = kwargs[key]
                elif key == "https_endpoints":
                    self.parameters["https_endpoints"] = kwargs[key]
                elif key == "ssh_endpoints":
                    self.parameters["ssh_endpoints"] = kwargs[key]
                elif key == "application_type":
                    self.parameters["application_type"] = kwargs[key]
                elif key == "errors":
                    self.parameters["errors"] = kwargs[key]
                elif key == "additional_properties":
                    self.parameters["additional_properties"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Application instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Application instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_application()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Application instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_application()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_application():
                time.sleep(20)
        else:
            self.log("Application instance unchanged")
            self.results['changed'] = False
            response = old_response

        self.results.update(self.format_item(response))
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
            if isinstance(response, LROPoller):
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

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'id': d['id']
        }
        return d


def main():
    """Main execution"""
    AzureRMApplications()


if __name__ == '__main__':
    main()
