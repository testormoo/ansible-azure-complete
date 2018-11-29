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
module: azure_rm_storagesyncregisteredserver
version_added: "2.8"
short_description: Manage Azure Registered Server instance.
description:
    - Create, update and delete instance of Azure Registered Server.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    name:
        description:
            - Name of Storage Sync Service resource.
        required: True
    server_id:
        description:
            - GUID identifying the on-premises server.
        required: True
    server_certificate:
        description:
            - Registered Server Certificate
    agent_version:
        description:
            - Registered Server Agent Version
    server_os_version:
        description:
            - Registered Server OS Version
    last_heart_beat:
        description:
            - Registered Server last heart beat
    server_role:
        description:
            - Registered Server serverRole
    cluster_id:
        description:
            - Registered Server clusterId
    cluster_name:
        description:
            - Registered Server clusterName
    server_id:
        description:
            - Registered Server serverId
    friendly_name:
        description:
            - Friendly Name
    state:
      description:
        - Assert the state of the Registered Server.
        - Use 'present' to create or update an Registered Server and 'absent' to delete it.
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
  - name: Create (or update) Registered Server
    azure_rm_storagesyncregisteredserver:
      resource_group: SampleResourceGroup_1
      name: SampleStorageSyncService_1
      server_id: "080d4133-bdb5-40a0-96a0-71a6057bfe9a"
      server_certificate: "MIIDFjCCAf6gAwIBAgIQQS+DS8uhc4VNzUkTw7wbRjANBgkqhkiG9w0BAQ0FADAzMTEwLwYDVQQDEyhhbmt1c2hiLXByb2QzLnJlZG1vbmQuY29ycC5taWNyb3NvZnQuY29tMB4XDTE3MDgwMzE3MDQyNFoXDTE4MDgwNDE3MDQyNFowMzExMC8GA1UEAxMoYW5rdXNoYi1wcm9kMy5yZWRtb25kLmNvcnAubWljcm9zb2Z0LmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALDRvV4gmsIy6jGDPiHsXmvgVP749NNP7DopdlbHaNhjFmYINHl0uWylyaZmgJrROt2mnxN/zEyJtGnqYHlzUr4xvGq/qV5pqgdB9tag/sw9i22gfe9PRZ0FmSOZnXMbLYgLiDFqLtut5gHcOuWMj03YnkfoBEKlFBxWbagvW2yxz/Sxi9OVSJOKCaXra0RpcIHrO/KFl6ho2eE1/7Ykmfa8hZvSdoPd5gHdLiQcMB/pxq+mWp1fI6c8vFZoDu7Atn+NXTzYPKUxKzaisF12TsaKpohUsJpbB3Wocb0F5frn614D2pg14ERB5otjAMWw1m65csQWPI6dP8KIYe0+QPkCAwEAAaMmMCQwIgYDVR0lAQH/BBgwFgYIKwYBBQUHAwIGCisGAQQBgjcKAwwwDQYJKoZIhvcNAQENBQADggEBAA4RhVIBkw34M1RwakJgHvtjsOFxF1tVQA941NtLokx1l2Z8+GFQkcG4xpZSt+UN6wLerdCbnNhtkCErWUDeaT0jxk4g71Ofex7iM04crT4iHJr8mi96/XnhnkTUs+GDk12VgdeeNEczMZz+8Mxw9dJ5NCnYgTwO0SzGlclRsDvjzkLo8rh2ZG6n/jKrEyNXXo+hOqhupij0QbRP2Tvexdfw201kgN1jdZify8XzJ8Oi0bTS0KpJf2pNPOlooK2bjMUei9ANtEdXwwfVZGWvVh6tJjdv6k14wWWJ1L7zhA1IIVb1J+sQUzJji5iX0DrezjTz1Fg+gAzITaA/WsuujlM="
      agent_version: 1.0.277.0
      server_os_version: 10.0.14393.0
      last_heart_beat: "2017-08-08T18:29:06.470652Z"
      server_role: Standalone
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/52b8da2f-61e0-4a1f-8dde-336911f367fb/resourceGroups/SampleResourceGroup_1/providers/10.91.86.47/storageSyncServices/SampleStorage
            SyncService_1/registeredServers/530a0384-50ac-456d-8240-9d6621404151"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storagesync import StorageSyncManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRegisteredServer(AzureRMModuleBase):
    """Configuration class for an Azure RM Registered Server resource"""

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
            server_id=dict(
                type='str',
                required=True
            ),
            server_certificate=dict(
                type='str'
            ),
            agent_version=dict(
                type='str'
            ),
            server_os_version=dict(
                type='str'
            ),
            last_heart_beat=dict(
                type='str'
            ),
            server_role=dict(
                type='str'
            ),
            cluster_id=dict(
                type='str'
            ),
            cluster_name=dict(
                type='str'
            ),
            server_id=dict(
                type='str'
            ),
            friendly_name=dict(
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
        self.server_id = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRegisteredServer, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_registeredserver()

        if not old_response:
            self.log("Registered Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Registered Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Registered Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_registeredserver()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Registered Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_registeredserver()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Registered Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_registeredserver(self):
        '''
        Creates or updates Registered Server with the specified configuration.

        :return: deserialized Registered Server instance state dictionary
        '''
        self.log("Creating / Updating the Registered Server instance {0}".format(self.server_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.registered_servers.create(resource_group_name=self.resource_group,
                                                                      storage_sync_service_name=self.name,
                                                                      server_id=self.server_id,
                                                                      parameters=self.parameters)
            else:
                response = self.mgmt_client.registered_servers.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Registered Server instance.')
            self.fail("Error creating the Registered Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_registeredserver(self):
        '''
        Deletes specified Registered Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Registered Server instance {0}".format(self.server_id))
        try:
            response = self.mgmt_client.registered_servers.delete(resource_group_name=self.resource_group,
                                                                  storage_sync_service_name=self.name,
                                                                  server_id=self.server_id)
        except CloudError as e:
            self.log('Error attempting to delete the Registered Server instance.')
            self.fail("Error deleting the Registered Server instance: {0}".format(str(e)))

        return True

    def get_registeredserver(self):
        '''
        Gets the properties of the specified Registered Server.

        :return: deserialized Registered Server instance state dictionary
        '''
        self.log("Checking if the Registered Server instance {0} is present".format(self.server_id))
        found = False
        try:
            response = self.mgmt_client.registered_servers.get(resource_group_name=self.resource_group,
                                                               storage_sync_service_name=self.name,
                                                               server_id=self.server_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Registered Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Registered Server instance.')
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


def main():
    """Main execution"""
    AzureRMRegisteredServer()


if __name__ == '__main__':
    main()
