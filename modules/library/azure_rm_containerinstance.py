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
module: azure_rm_containerinstance
version_added: "2.8"
short_description: Manage Azure Container Group instance.
description:
    - Create, update and delete instance of Azure Container Group.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the container group.
        required: True
    location:
        description:
            - The resource location.
            - Required when C(state) is I(present).
    containers:
        description:
            - The containers within the container group.
        type: list
        suboptions:
            name:
                description:
                    - The user-provided name of the container instance.
                    - Required when C(state) is I(present).
            image:
                description:
                    - The name of the image used to create the container instance.
                    - Required when C(state) is I(present).
            command:
                description:
                    - The commands to execute within the container instance in exec form.
                type: list
            ports:
                description:
                    - The exposed ports on the container instance.
                type: list
                suboptions:
                    protocol:
                        description:
                            - The protocol associated with the I(port).
                        choices:
                            - 'tcp'
                            - 'udp'
                    port:
                        description:
                            - The port number exposed within the container group.
                            - Required when C(state) is I(present).
            environment_variables:
                description:
                    - The environment variables to set in the container instance.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the environment variable.
                            - Required when C(state) is I(present).
                    value:
                        description:
                            - The value of the environment variable.
                            - Required when C(state) is I(present).
            resources:
                description:
                    - The resource requirements of the container instance.
                    - Required when C(state) is I(present).
                suboptions:
                    requests:
                        description:
                            - The resource requests of this container instance.
                            - Required when C(state) is I(present).
                        suboptions:
                            memory_in_gb:
                                description:
                                    - The memory request in GB of this container instance.
                                    - Required when C(state) is I(present).
                            cpu:
                                description:
                                    - The CPU request of this container instance.
                                    - Required when C(state) is I(present).
                    limits:
                        description:
                            - The resource limits of this container instance.
                        suboptions:
                            memory_in_gb:
                                description:
                                    - The memory limit in GB of this container instance.
                            cpu:
                                description:
                                    - The CPU limit of this container instance.
            volume_mounts:
                description:
                    - The volume mounts available to the container instance.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the volume mount.
                            - Required when C(state) is I(present).
                    mount_path:
                        description:
                            - "The path within the container where the volume should be mounted. Must not contain colon (:)."
                            - Required when C(state) is I(present).
                    read_only:
                        description:
                            - The flag indicating whether the volume mount is read-only.
    image_registry_credentials:
        description:
            - The image registry credentials by which the container group is created from.
        type: list
        suboptions:
            server:
                description:
                    - "The Docker image registry server without a protocol such as 'http' and 'https'."
                    - Required when C(state) is I(present).
            username:
                description:
                    - The username for the private registry.
                    - Required when C(state) is I(present).
            password:
                description:
                    - The password for the private registry.
    restart_policy:
        description:
            - Restart policy for all I(containers) within the container group.
            - - `C(always)` C(always) restart
            - - `C(on_failure)` Restart on failure
            - - `C(never)` C(never) restart
            - .
        choices:
            - 'always'
            - 'on_failure'
            - 'never'
    ip_address:
        description:
            - The IP address type of the container group.
        suboptions:
            ports:
                description:
                    - The list of ports exposed on the container group.
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    protocol:
                        description:
                            - The protocol associated with the I(port).
                        choices:
                            - 'tcp'
                            - 'udp'
                    port:
                        description:
                            - The port number.
                            - Required when C(state) is I(present).
            type:
                description:
                    - Specifies if the I(ip) is exposed to the public internet.
                    - Required when C(state) is I(present).
            ip:
                description:
                    - The IP exposed to the public internet.
    os_type:
        description:
            - The operating system type required by the I(containers) in the container group.
        choices:
            - 'windows'
            - 'linux'
    volumes:
        description:
            - The list of volumes that can be mounted by I(containers) in this container group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the volume.
                    - Required when C(state) is I(present).
            azure_file:
                description:
                    - The name of the Azure File volume.
                suboptions:
                    share_name:
                        description:
                            - The name of the Azure File share to be mounted as a volume.
                            - Required when C(state) is I(present).
                    read_only:
                        description:
                            - The flag indicating whether the Azure File shared mounted as a volume is read-only.
                    storage_account_name:
                        description:
                            - The name of the storage account that contains the Azure File share.
                            - Required when C(state) is I(present).
                    storage_account_key:
                        description:
                            - The storage account access key used to access the Azure File share.
            empty_dir:
                description:
                    - The empty directory volume.
    state:
      description:
        - Assert the state of the Container Group.
        - Use 'present' to create or update an Container Group and 'absent' to delete it.
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
  - name: Create (or update) Container Group
    azure_rm_containerinstance:
      resource_group: demo
      name: mycontainers
      location: westus
      containers:
        - name: mycontainers
          image: nginx
          command:
            - []
          ports:
            - port: 80
          resources:
            requests:
              memory_in_gb: 1.5
              cpu: 1
          volume_mounts:
            - name: volume1
              mount_path: /mnt/volume1
              read_only: False
      ip_address:
        ports:
          - protocol: TCP
            port: 80
        type: Public
      os_type: Linux
      volumes:
        - name: volume1
          azure_file:
            share_name: shareName
            storage_account_name: accountName
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: /subscriptions/ae43b1e3-c35d-4c8c-bc0d-f148b4c52b78/resourceGroups/demo/providers/Microsoft.ContainerInstance/containerGroups/mycontainers
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.containerinstance import ContainerInstanceManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMContainerGroup(AzureRMModuleBase):
    """Configuration class for an Azure RM Container Group resource"""

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
            containers=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    image=dict(
                        type='str'
                    ),
                    command=dict(
                        type='list'
                    ),
                    ports=dict(
                        type='list',
                        options=dict(
                            protocol=dict(
                                type='str',
                                choices=['tcp',
                                         'udp']
                            ),
                            port=dict(
                                type='int'
                            )
                        )
                    ),
                    environment_variables=dict(
                        type='list',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            value=dict(
                                type='str'
                            )
                        )
                    ),
                    resources=dict(
                        type='dict',
                        options=dict(
                            requests=dict(
                                type='dict',
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
                                type='dict',
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
                    volume_mounts=dict(
                        type='list',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            mount_path=dict(
                                type='str'
                            ),
                            read_only=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            image_registry_credentials=dict(
                type='list',
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
            restart_policy=dict(
                type='str',
                choices=['always',
                         'on_failure',
                         'never']
            ),
            ip_address=dict(
                type='dict',
                options=dict(
                    ports=dict(
                        type='list',
                        options=dict(
                            protocol=dict(
                                type='str',
                                choices=['tcp',
                                         'udp']
                            ),
                            port=dict(
                                type='int'
                            )
                        )
                    ),
                    type=dict(
                        type='str'
                    ),
                    ip=dict(
                        type='str'
                    )
                )
            ),
            os_type=dict(
                type='str',
                choices=['windows',
                         'linux']
            ),
            volumes=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    azure_file=dict(
                        type='dict',
                        options=dict(
                            share_name=dict(
                                type='str'
                            ),
                            read_only=dict(
                                type='str'
                            ),
                            storage_account_name=dict(
                                type='str'
                            ),
                            storage_account_key=dict(
                                type='str'
                            )
                        )
                    ),
                    empty_dir=dict(
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
        self.name = None
        self.container_group = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMContainerGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.container_group[key] = kwargs[key]

        dict_upper(self.container_group, ['containers', 'ports', 'protocol'])
        dict_camelize(self.container_group, ['restart_policy'], True)
        dict_upper(self.container_group, ['ip_address', 'ports', 'protocol'])
        dict_camelize(self.container_group, ['os_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ContainerInstanceManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_containergroup()

        if not old_response:
            self.log("Container Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Container Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.container_group, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Container Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_containergroup()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Container Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_containergroup()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Container Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_containergroup(self):
        '''
        Creates or updates Container Group with the specified configuration.

        :return: deserialized Container Group instance state dictionary
        '''
        self.log("Creating / Updating the Container Group instance {0}".format(self.name))

        try:
            response = self.mgmt_client.container_groups.create_or_update(resource_group_name=self.resource_group,
                                                                          container_group_name=self.name,
                                                                          container_group=self.container_group)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Container Group instance.')
            self.fail("Error creating the Container Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_containergroup(self):
        '''
        Deletes specified Container Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Container Group instance {0}".format(self.name))
        try:
            response = self.mgmt_client.container_groups.delete(resource_group_name=self.resource_group,
                                                                container_group_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Container Group instance.')
            self.fail("Error deleting the Container Group instance: {0}".format(str(e)))

        return True

    def get_containergroup(self):
        '''
        Gets the properties of the specified Container Group.

        :return: deserialized Container Group instance state dictionary
        '''
        self.log("Checking if the Container Group instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.container_groups.get(resource_group_name=self.resource_group,
                                                             container_group_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Container Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Container Group instance.')
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


def main():
    """Main execution"""
    AzureRMContainerGroup()


if __name__ == '__main__':
    main()
