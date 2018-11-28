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
module: azure_rm_botserviceenterprisechannel
version_added: "2.8"
short_description: Manage Azure Enterprise Channel instance.
description:
    - Create, update and delete instance of Azure Enterprise Channel.

options:
    resource_group:
        description:
            - The name of the C(bot) resource group in the user subscription.
        required: True
    name:
        description:
            - The name of the C(bot) resource.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - Gets or sets the SKU of the resource.
        suboptions:
            name:
                description:
                    - The sku name.
                    - Required when C(state) is I(present).
                choices:
                    - 'f0'
                    - 's1'
    kind:
        description:
            - Required. Gets or sets the Kind of the resource.
        choices:
            - 'sdk'
            - 'designer'
            - 'bot'
            - 'function'
    state:
        description:
            - The current state of the Enterprise Channel.
        choices:
            - 'creating'
            - 'create_failed'
            - 'started'
            - 'starting'
            - 'start_failed'
            - 'stopped'
            - 'stopping'
            - 'stop_failed'
            - 'deleting'
            - 'delete_failed'
    nodes:
        description:
            - The nodes associated with the Enterprise Channel.
            - Required when C(state) is I(present).
        type: list
        suboptions:
            state:
                description:
                    - The current state of the Enterprise Channel Node.
                choices:
                    - 'creating'
                    - 'create_failed'
                    - 'started'
                    - 'starting'
                    - 'start_failed'
                    - 'stopped'
                    - 'stopping'
                    - 'stop_failed'
                    - 'deleting'
                    - 'delete_failed'
            name:
                description:
                    - The name of the Enterprise Channel Node.
                    - Required when C(state) is I(present).
            azure_sku:
                description:
                    - The sku of the Enterprise Channel Node.
                    - Required when C(state) is I(present).
            azure_location:
                description:
                    - The location of the Enterprise Channel Node.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Enterprise Channel.
        - Use 'present' to create or update an Enterprise Channel and 'absent' to delete it.
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
  - name: Create (or update) Enterprise Channel
    azure_rm_botserviceenterprisechannel:
      resource_group: OneResourceGroupName
      name: contoso-dl
      location: eastus
      sku:
        name: S1
      nodes:
        - name: Node 1
          azure_sku: Int1
          azure_location: WestUs
'''

RETURN = '''
id:
    description:
        - Specifies the resource ID.
    returned: always
    type: str
    sample: someid
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.botservice import AzureBotService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMEnterpriseChannel(AzureRMModuleBase):
    """Configuration class for an Azure RM Enterprise Channel resource"""

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
            sku=dict(
                type='dict'
                options=dict(
                    name=dict(
                        type='str',
                        choices=['f0',
                                 's1']
                    )
                )
            ),
            kind=dict(
                type='str',
                choices=['sdk',
                         'designer',
                         'bot',
                         'function']
            ),
            state=dict(
                type='str',
                choices=['creating',
                         'create_failed',
                         'started',
                         'starting',
                         'start_failed',
                         'stopped',
                         'stopping',
                         'stop_failed',
                         'deleting',
                         'delete_failed']
            ),
            nodes=dict(
                type='list'
                options=dict(
                    state=dict(
                        type='str',
                        choices=['creating',
                                 'create_failed',
                                 'started',
                                 'starting',
                                 'start_failed',
                                 'stopped',
                                 'stopping',
                                 'stop_failed',
                                 'deleting',
                                 'delete_failed']
                    ),
                    name=dict(
                        type='str'
                    ),
                    azure_sku=dict(
                        type='str'
                    ),
                    azure_location=dict(
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
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEnterpriseChannel, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_expand(self.parameters, ['state'])
        dict_camelize(self.parameters, ['state'], True)
        dict_camelize(self.parameters, ['nodes', 'state'], True)
        dict_expand(self.parameters, ['nodes'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureBotService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_enterprisechannel()

        if not old_response:
            self.log("Enterprise Channel instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Enterprise Channel instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Enterprise Channel instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_enterprisechannel()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Enterprise Channel instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_enterprisechannel()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Enterprise Channel instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_enterprisechannel(self):
        '''
        Creates or updates Enterprise Channel with the specified configuration.

        :return: deserialized Enterprise Channel instance state dictionary
        '''
        self.log("Creating / Updating the Enterprise Channel instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.enterprise_channels.create(resource_group_name=self.resource_group,
                                                                       resource_name=self.name,
                                                                       parameters=self.parameters)
            else:
                response = self.mgmt_client.enterprise_channels.update(resource_group_name=self.resource_group,
                                                                       resource_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Enterprise Channel instance.')
            self.fail("Error creating the Enterprise Channel instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_enterprisechannel(self):
        '''
        Deletes specified Enterprise Channel instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Enterprise Channel instance {0}".format(self.name))
        try:
            response = self.mgmt_client.enterprise_channels.delete(resource_group_name=self.resource_group,
                                                                   resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Enterprise Channel instance.')
            self.fail("Error deleting the Enterprise Channel instance: {0}".format(str(e)))

        return True

    def get_enterprisechannel(self):
        '''
        Gets the properties of the specified Enterprise Channel.

        :return: deserialized Enterprise Channel instance state dictionary
        '''
        self.log("Checking if the Enterprise Channel instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.enterprise_channels.get(resource_group_name=self.resource_group,
                                                                resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Enterprise Channel instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Enterprise Channel instance.')
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
    AzureRMEnterpriseChannel()


if __name__ == '__main__':
    main()
