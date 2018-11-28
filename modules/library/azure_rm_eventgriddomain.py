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
module: azure_rm_eventgriddomain
version_added: "2.8"
short_description: Manage Azure Domain instance.
description:
    - Create, update and delete instance of Azure Domain.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription."
        required: True
    name:
        description:
            - Name of the domain
        required: True
    location:
        description:
            - Location of the resource
            - Required when C(state) is I(present).
    input_schema:
        description:
            - This determines the format that Event Grid should expect for incoming events published to the domain.
        choices:
            - 'event_grid_schema'
            - 'custom_event_schema'
            - 'cloud_event_v01_schema'
    input_schema_mapping:
        description:
            - Information about the InputSchemaMapping which specified the info about mapping event payload.
        suboptions:
            input_schema_mapping_type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Domain.
        - Use 'present' to create or update an Domain and 'absent' to delete it.
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
  - name: Create (or update) Domain
    azure_rm_eventgriddomain:
      resource_group: examplerg
      name: exampledomain1
      location: westus2
'''

RETURN = '''
id:
    description:
        - Fully qualified identifier of the resource
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
    from azure.mgmt.eventgrid import EventGridManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDomain(AzureRMModuleBase):
    """Configuration class for an Azure RM Domain resource"""

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
            input_schema=dict(
                type='str',
                choices=['event_grid_schema',
                         'custom_event_schema',
                         'cloud_event_v01_schema']
            ),
            input_schema_mapping=dict(
                type='dict'
                options=dict(
                    input_schema_mapping_type=dict(
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
        self.domain_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDomain, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.domain_info[key] = kwargs[key]

        dict_camelize(self.domain_info, ['input_schema'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_domain()

        if not old_response:
            self.log("Domain instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Domain instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.domain_info, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Domain instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_domain()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Domain instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_domain()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Domain instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_domain(self):
        '''
        Creates or updates Domain with the specified configuration.

        :return: deserialized Domain instance state dictionary
        '''
        self.log("Creating / Updating the Domain instance {0}".format(self.name))

        try:
            response = self.mgmt_client.domains.create_or_update(resource_group_name=self.resource_group,
                                                                 domain_name=self.name,
                                                                 domain_info=self.domain_info)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Domain instance.')
            self.fail("Error creating the Domain instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_domain(self):
        '''
        Deletes specified Domain instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Domain instance {0}".format(self.name))
        try:
            response = self.mgmt_client.domains.delete(resource_group_name=self.resource_group,
                                                       domain_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Domain instance.')
            self.fail("Error deleting the Domain instance: {0}".format(str(e)))

        return True

    def get_domain(self):
        '''
        Gets the properties of the specified Domain.

        :return: deserialized Domain instance state dictionary
        '''
        self.log("Checking if the Domain instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.domains.get(resource_group_name=self.resource_group,
                                                    domain_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Domain instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Domain instance.')
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
    AzureRMDomain()


if __name__ == '__main__':
    main()
