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
module: azure_rm_servicefabricmeshapplication
version_added: "2.8"
short_description: Manage Application instance.
description:
    - Create, update and delete instance of Application.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    application_resource_name:
        description:
            - The identity of the application.
        required: True
    application_resource_description:
        description:
            - Description for creating a Application resource.
        required: True
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                required: True
            description:
                description:
                    - User readable description of the application.
            services:
                description:
                    - "Describes the services in the application. This property is used to create or modify services of the application. On get only the
                       name of the service is returned. The service I(description) can be obtained by querying for the service resource."
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the resource
                    os_type:
                        description:
                            - The operation system required by the code in service.
                        required: True
                        choices:
                            - 'linux'
                            - 'windows'
                    code_packages:
                        description:
                            - "Describes the set of code packages that forms the service. A code package describes the container and the properties for
                               running it. All the code packages are started together on the same host and share the same context (network, process etc.)."
                        required: True
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The name of the code package.
                                required: True
                            image:
                                description:
                                    - The Container image to use.
                                required: True
                            image_registry_credential:
                                description:
                                    - I(image) registry credential.
                                suboptions:
                                    server:
                                        description:
                                            - Docker image registry server, without protocol such as `http` and `https`.
                                        required: True
                                    username:
                                        description:
                                            - The username for the private registry.
                                        required: True
                                    password:
                                        description:
                                            - "The password for the private registry. The password is required for create or update operations, however it
                                               is not returned in the get or list operations."
                            entrypoint:
                                description:
                                    - Override for the default entry point in the container.
                            commands:
                                description:
                                    - Command array to execute within the container in exec form.
                                type: list
                            environment_variables:
                                description:
                                    - The environment variables to set in this container
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - The name of the environment variable.
                                    value:
                                        description:
                                            - The value of the environment variable.
                            settings:
                                description:
                                    - "The settings to set in this container. The setting file path can be fetched from environment variable
                                       'Fabric_SettingPath'. The path for Windows container is 'C:\\secrets'. The path for Linux container is
                                       '/var/secrets'."
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - The name of the setting.
                                    value:
                                        description:
                                            - The value of the setting.
                            labels:
                                description:
                                    - The labels to set in this container.
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - The name of the container label.
                                        required: True
                                    value:
                                        description:
                                            - The value of the container label.
                                        required: True
                            endpoints:
                                description:
                                    - The endpoints exposed by this container.
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - The name of the endpoint.
                                        required: True
                                    port:
                                        description:
                                            - Port used by the container.
                            resources:
                                description:
                                    - The resources required by this container.
                                required: True
                                suboptions:
                                    requests:
                                        description:
                                            - Describes the requested resources for a given container.
                                        required: True
                                        suboptions:
                                            memory_in_gb:
                                                description:
                                                    - The memory request in GB for this container.
                                                required: True
                                            cpu:
                                                description:
                                                    - Requested number of CPU cores. At present, only full cores are supported.
                                                required: True
                                    limits:
                                        description:
                                            - Describes the maximum limits on the resources for a given container.
                                        suboptions:
                                            memory_in_gb:
                                                description:
                                                    - The memory limit in GB.
                                            cpu:
                                                description:
                                                    - CPU limits in cores. At present, only full cores are supported.
                            volume_refs:
                                description:
                                    - "I(volumes) to be attached to the container. The lifetime of these I(volumes) is independent of the application's
                                       lifetime."
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - Name of the volume being referenced.
                                        required: True
                                    read_only:
                                        description:
                                            - "The flag indicating whether the volume is read only. Default is 'false'."
                                    destination_path:
                                        description:
                                            - The path within the container at which the volume should be mounted. Only valid path characters are allowed.
                                        required: True
                            volumes:
                                description:
                                    - "Volumes to be attached to the container. The lifetime of these volumes is scoped to the application's lifetime."
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - Name of the volume being referenced.
                                        required: True
                                    read_only:
                                        description:
                                            - "The flag indicating whether the volume is read only. Default is 'false'."
                                    destination_path:
                                        description:
                                            - The path within the container at which the volume should be mounted. Only valid path characters are allowed.
                                        required: True
                                    creation_parameters:
                                        description:
                                            - Describes parameters for creating application-scoped volumes.
                                        required: True
                                        suboptions:
                                            description:
                                                description:
                                                    - User readable description of the volume.
                                            kind:
                                                description:
                                                    - Constant filled by server.
                                                required: True
                            diagnostics:
                                description:
                                    - Reference to sinks in DiagnosticsDescription.
                                suboptions:
                                    enabled:
                                        description:
                                            - Status of whether or not sinks are enabled.
                                    sink_refs:
                                        description:
                                            - List of sinks to be used if I(enabled). References the list of sinks in DiagnosticsDescription.
                                        type: list
                            reliable_collections_refs:
                                description:
                                    - "A list of ReliableCollection I(resources) used by this particular code package. Please refer to
                                       ReliablecollectionsRef for more details."
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - "Name of ReliableCollection resource. Right now it's not used and you can use any string."
                                        required: True
                                    do_not_persist_state:
                                        description:
                                            - "False (the default) if ReliableCollections state is persisted to disk as usual. True if you do not want to
                                               persist state, in which case replication is still enabled and you can use ReliableCollections as distributed
                                               cache."
                    network_refs:
                        description:
                            - The names of the private networks that this service needs to be part of.
                        type: list
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
                    diagnostics:
                        description:
                            - Reference to sinks in DiagnosticsDescription.
                        suboptions:
                            enabled:
                                description:
                                    - Status of whether or not sinks are enabled.
                            sink_refs:
                                description:
                                    - List of sinks to be used if I(enabled). References the list of sinks in DiagnosticsDescription.
                                type: list
                    description:
                        description:
                            - User readable description of the service.
                    replica_count:
                        description:
                            - The number of replicas of the service to create. Defaults to 1 if not specified.
                    auto_scaling_policies:
                        description:
                            - Auto scaling policies
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The name of the auto scaling policy.
                                required: True
                            trigger:
                                description:
                                    - Determines when auto scaling operation will be invoked.
                                required: True
                                suboptions:
                                    kind:
                                        description:
                                            - Constant filled by server.
                                        required: True
                            mechanism:
                                description:
                                    - The mechanism that is used to scale when auto scaling operation is invoked.
                                required: True
                                suboptions:
                                    kind:
                                        description:
                                            - Constant filled by server.
                                        required: True
            diagnostics:
                description:
                    - Describes the diagnostics definition and usage for an application resource.
                suboptions:
                    sinks:
                        description:
                            - List of supported sinks that can be referenced.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Name of the sink. This value is referenced by DiagnosticsReferenceDescription
                            description:
                                description:
                                    - A description of the sink.
                            kind:
                                description:
                                    - Constant filled by server.
                                required: True
                    enabled:
                        description:
                            - Status of whether or not I(sinks) are enabled.
                    default_sink_refs:
                        description:
                            - The I(sinks) to be used if diagnostics is I(enabled). Sink choices can be overridden at the service and code package level.
                        type: list
            debug_params:
                description:
                    - Internal - used by Visual Studio to setup the debugging session on the local development environment.
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
    azure_rm_servicefabricmeshapplication:
      resource_group: sbz_demo
      application_resource_name: sampleApplication
      application_resource_description:
        location: EastUS
'''

RETURN = '''
id:
    description:
        - "Fully qualified identifier for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/applications/sampleApplication
status:
    description:
        - "Status of the application. Possible values include: 'Unknown', 'Ready', 'Upgrading', 'Creating', 'Deleting', 'Failed'"
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


class AzureRMApplication(AzureRMModuleBase):
    """Configuration class for an Azure RM Application resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            application_resource_name=dict(
                type='str',
                required=True
            ),
            application_resource_description=dict(
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
        self.application_resource_name = None
        self.application_resource_description = dict()

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
                if key == "location":
                    self.application_resource_description["location"] = kwargs[key]
                elif key == "description":
                    self.application_resource_description["description"] = kwargs[key]
                elif key == "services":
                    ev = kwargs[key]
                    if 'os_type' in ev:
                        if ev['os_type'] == 'linux':
                            ev['os_type'] = 'Linux'
                        elif ev['os_type'] == 'windows':
                            ev['os_type'] = 'Windows'
                    self.application_resource_description["services"] = ev
                elif key == "diagnostics":
                    self.application_resource_description["diagnostics"] = kwargs[key]
                elif key == "debug_params":
                    self.application_resource_description["debug_params"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
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

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_application(self):
        '''
        Creates or updates Application with the specified configuration.

        :return: deserialized Application instance state dictionary
        '''
        self.log("Creating / Updating the Application instance {0}".format(self.application_resource_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.application.create(resource_group_name=self.resource_group,
                                                               application_resource_name=self.application_resource_name,
                                                               application_resource_description=self.application_resource_description)
            else:
                response = self.mgmt_client.application.update()
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
        self.log("Deleting the Application instance {0}".format(self.application_resource_name))
        try:
            response = self.mgmt_client.application.delete(resource_group_name=self.resource_group,
                                                           application_resource_name=self.application_resource_name)
        except CloudError as e:
            self.log('Error attempting to delete the Application instance.')
            self.fail("Error deleting the Application instance: {0}".format(str(e)))

        return True

    def get_application(self):
        '''
        Gets the properties of the specified Application.

        :return: deserialized Application instance state dictionary
        '''
        self.log("Checking if the Application instance {0} is present".format(self.application_resource_name))
        found = False
        try:
            response = self.mgmt_client.application.get(resource_group_name=self.resource_group,
                                                        application_resource_name=self.application_resource_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Application instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Application instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMApplication()


if __name__ == '__main__':
    main()
