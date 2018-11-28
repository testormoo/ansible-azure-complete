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
short_description: Manage Azure Application instance.
description:
    - Create, update and delete instance of Azure Application.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    name:
        description:
            - The identity of the application.
        required: True
    location:
        description:
            - The geo-location where the resource lives
            - Required when C(state) is I(present).
    description:
        description:
            - User readable description of the application.
    services:
        description:
            - "Describes the services in the application. This property is used to create or modify services of the application. On get only the name of the
               service is returned. The service I(description) can be obtained by querying for the service resource."
        type: list
        suboptions:
            name:
                description:
                    - The name of the resource
            os_type:
                description:
                    - The operation system required by the code in service.
                    - Required when C(state) is I(present).
                choices:
                    - 'linux'
                    - 'windows'
            code_packages:
                description:
                    - "Describes the set of code packages that forms the service. A code package describes the container and the properties for running it.
                       All the code packages are started together on the same host and share the same context (network, process etc.)."
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the code package.
                            - Required when C(state) is I(present).
                    image:
                        description:
                            - The Container image to use.
                            - Required when C(state) is I(present).
                    image_registry_credential:
                        description:
                            - I(image) registry credential.
                        suboptions:
                            server:
                                description:
                                    - Docker image registry server, without protocol such as `http` and `https`.
                                    - Required when C(state) is I(present).
                            username:
                                description:
                                    - The username for the private registry.
                                    - Required when C(state) is I(present).
                            password:
                                description:
                                    - "The password for the private registry. The password is required for create or update operations, however it is not
                                       returned in the get or list operations."
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
                            - "The settings to set in this container. The setting file path can be fetched from environment variable 'Fabric_SettingPath'.
                               The path for Windows container is 'C:\\secrets'. The path for Linux container is '/var/secrets'."
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
                                    - Required when C(state) is I(present).
                            value:
                                description:
                                    - The value of the container label.
                                    - Required when C(state) is I(present).
                    endpoints:
                        description:
                            - The endpoints exposed by this container.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The name of the endpoint.
                                    - Required when C(state) is I(present).
                            port:
                                description:
                                    - Port used by the container.
                    resources:
                        description:
                            - The resources required by this container.
                            - Required when C(state) is I(present).
                        suboptions:
                            requests:
                                description:
                                    - Describes the requested resources for a given container.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    memory_in_gb:
                                        description:
                                            - The memory request in GB for this container.
                                            - Required when C(state) is I(present).
                                    cpu:
                                        description:
                                            - Requested number of CPU cores. At present, only full cores are supported.
                                            - Required when C(state) is I(present).
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
                            - "I(volumes) to be attached to the container. The lifetime of these I(volumes) is independent of the application's lifetime."
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Name of the volume being referenced.
                                    - Required when C(state) is I(present).
                            read_only:
                                description:
                                    - "The flag indicating whether the volume is read only. Default is 'false'."
                            destination_path:
                                description:
                                    - The path within the container at which the volume should be mounted. Only valid path characters are allowed.
                                    - Required when C(state) is I(present).
                    volumes:
                        description:
                            - "Volumes to be attached to the container. The lifetime of these volumes is scoped to the application's lifetime."
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Name of the volume being referenced.
                                    - Required when C(state) is I(present).
                            read_only:
                                description:
                                    - "The flag indicating whether the volume is read only. Default is 'false'."
                            destination_path:
                                description:
                                    - The path within the container at which the volume should be mounted. Only valid path characters are allowed.
                                    - Required when C(state) is I(present).
                            creation_parameters:
                                description:
                                    - Describes parameters for creating application-scoped volumes.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    description:
                                        description:
                                            - User readable description of the volume.
                                    kind:
                                        description:
                                            - Constant filled by server.
                                            - Required when C(state) is I(present).
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
                            - "A list of ReliableCollection I(resources) used by this particular code package. Please refer to ReliablecollectionsRef for
                               more details."
                        type: list
                        suboptions:
                            name:
                                description:
                                    - "Name of ReliableCollection resource. Right now it's not used and you can use any string."
                                    - Required when C(state) is I(present).
                            do_not_persist_state:
                                description:
                                    - "False (the default) if ReliableCollections state is persisted to disk as usual. True if you do not want to persist
                                       state, in which case replication is still enabled and you can use ReliableCollections as distributed cache."
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
                            - Required when C(state) is I(present).
                    trigger:
                        description:
                            - Determines when auto scaling operation will be invoked.
                            - Required when C(state) is I(present).
                        suboptions:
                            kind:
                                description:
                                    - Constant filled by server.
                                    - Required when C(state) is I(present).
                    mechanism:
                        description:
                            - The mechanism that is used to scale when auto scaling operation is invoked.
                            - Required when C(state) is I(present).
                        suboptions:
                            kind:
                                description:
                                    - Constant filled by server.
                                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
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
      name: sampleApplication
      location: EastUS
      description: Service Fabric Mesh sample application.
      services:
        - name: helloWorldService
          os_type: Linux
          code_packages:
            - name: helloWorldCode
              image: seabreeze/sbz-helloworld:1.0-alpine
              endpoints:
                - name: helloWorldListener
                  port: 80
              resources:
                requests:
                  memory_in_gb: 1
                  cpu: 1
          network_refs:
            - name: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/networks/sampleNetwork
              endpoint_refs:
                - name: helloWorldListener
          description: SeaBreeze Hello World Service.
          replica_count: 1
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            services=dict(
                type='list'
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    os_type=dict(
                        type='str',
                        choices=['linux',
                                 'windows']
                    ),
                    code_packages=dict(
                        type='list'
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            image=dict(
                                type='str'
                            ),
                            image_registry_credential=dict(
                                type='dict'
                                options=dict(
                                    server=dict(
                                        type='str'
                                    ),
                                    username=dict(
                                        type='str'
                                    ),
                                    password=dict(
                                        type='str',
                                        no_log=True
                                    )
                                )
                            ),
                            entrypoint=dict(
                                type='str'
                            ),
                            commands=dict(
                                type='list'
                            ),
                            environment_variables=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    value=dict(
                                        type='str'
                                    )
                                )
                            ),
                            settings=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    value=dict(
                                        type='str'
                                    )
                                )
                            ),
                            labels=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    value=dict(
                                        type='str'
                                    )
                                )
                            ),
                            endpoints=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    port=dict(
                                        type='int'
                                    )
                                )
                            ),
                            resources=dict(
                                type='dict'
                                options=dict(
                                    requests=dict(
                                        type='dict'
                                        options=dict(
                                            memory_in_gb=dict(
                                                type='float'
                                            ),
                                            cpu=dict(
                                                type='float'
                                            )
                                        )
                                    ),
                                    limits=dict(
                                        type='dict'
                                        options=dict(
                                            memory_in_gb=dict(
                                                type='float'
                                            ),
                                            cpu=dict(
                                                type='float'
                                            )
                                        )
                                    )
                                )
                            ),
                            volume_refs=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    read_only=dict(
                                        type='str'
                                    ),
                                    destination_path=dict(
                                        type='str'
                                    )
                                )
                            ),
                            volumes=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    read_only=dict(
                                        type='str'
                                    ),
                                    destination_path=dict(
                                        type='str'
                                    ),
                                    creation_parameters=dict(
                                        type='dict'
                                        options=dict(
                                            description=dict(
                                                type='str'
                                            ),
                                            kind=dict(
                                                type='str'
                                            )
                                        )
                                    )
                                )
                            ),
                            diagnostics=dict(
                                type='dict'
                                options=dict(
                                    enabled=dict(
                                        type='str'
                                    ),
                                    sink_refs=dict(
                                        type='list'
                                    )
                                )
                            ),
                            reliable_collections_refs=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    do_not_persist_state=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    network_refs=dict(
                        type='list'
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            endpoint_refs=dict(
                                type='list'
                                options=dict(
                                    name=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    diagnostics=dict(
                        type='dict'
                        options=dict(
                            enabled=dict(
                                type='str'
                            ),
                            sink_refs=dict(
                                type='list'
                            )
                        )
                    ),
                    description=dict(
                        type='str'
                    ),
                    replica_count=dict(
                        type='int'
                    ),
                    auto_scaling_policies=dict(
                        type='list'
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            trigger=dict(
                                type='dict'
                                options=dict(
                                    kind=dict(
                                        type='str'
                                    )
                                )
                            ),
                            mechanism=dict(
                                type='dict'
                                options=dict(
                                    kind=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            diagnostics=dict(
                type='dict'
                options=dict(
                    sinks=dict(
                        type='list'
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            description=dict(
                                type='str'
                            ),
                            kind=dict(
                                type='str'
                            )
                        )
                    ),
                    enabled=dict(
                        type='str'
                    ),
                    default_sink_refs=dict(
                        type='list'
                    )
                )
            ),
            debug_params=dict(
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
                self.application_resource_description[key] = kwargs[key]

        dict_camelize(self.application_resource_description, ['services', 'os_type'], True)

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
                if (not default_compare(self.application_resource_description, old_response, '', self.results)):
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
                'id': response.get('id', None),
                'status': response.get('status', None)
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
                response = self.mgmt_client.application.create(resource_group_name=self.resource_group,
                                                               application_resource_name=self.name,
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
        self.log("Deleting the Application instance {0}".format(self.name))
        try:
            response = self.mgmt_client.application.delete(resource_group_name=self.resource_group,
                                                           application_resource_name=self.name)
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
            response = self.mgmt_client.application.get(resource_group_name=self.resource_group,
                                                        application_resource_name=self.name)
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMApplication()


if __name__ == '__main__':
    main()
