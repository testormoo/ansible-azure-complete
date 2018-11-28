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
module: azure_rm_automationpython2package
version_added: "2.8"
short_description: Manage Azure Python2 Package instance.
description:
    - Create, update and delete instance of Azure Python2 Package.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    name:
        description:
            - The name of python package.
        required: True
    uri:
        description:
            - Gets or sets the uri of the runbook content.
    content_hash:
        description:
            - Gets or sets the hash.
        suboptions:
            algorithm:
                description:
                    - Gets or sets the content hash algorithm used to hash the content.
                    - Required when C(state) is I(present).
            value:
                description:
                    - Gets or sets expected hash value of the content.
                    - Required when C(state) is I(present).
    version:
        description:
            - Gets or sets the version of the content.
    state:
      description:
        - Assert the state of the Python2 Package.
        - Use 'present' to create or update an Python2 Package and 'absent' to delete it.
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
  - name: Create (or update) Python2 Package
    azure_rm_automationpython2package:
      resource_group: rg
      automation_account_name: myAutomationAccount33
      name: OmsCompositeResources
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/MyAutomationAccount/python2Packages/MyPython2Package
version:
    description:
        - Gets or sets the version of the module.
    returned: always
    type: str
    sample: version
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPython2Package(AzureRMModuleBase):
    """Configuration class for an Azure RM Python2 Package resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            uri=dict(
                type='str'
            ),
            content_hash=dict(
                type='dict',
                options=dict(
                    algorithm=dict(
                        type='str'
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            version=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.name = None
        self.content_link = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPython2Package, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.content_link[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_python2package()

        if not old_response:
            self.log("Python2 Package instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Python2 Package instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.content_link, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Python2 Package instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_python2package()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Python2 Package instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_python2package()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Python2 Package instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'version': response.get('version', None)
                })
        return self.results

    def create_update_python2package(self):
        '''
        Creates or updates Python2 Package with the specified configuration.

        :return: deserialized Python2 Package instance state dictionary
        '''
        self.log("Creating / Updating the Python2 Package instance {0}".format(self.name))

        try:
            response = self.mgmt_client.python2_package.create_or_update(resource_group_name=self.resource_group,
                                                                         automation_account_name=self.automation_account_name,
                                                                         package_name=self.name,
                                                                         content_link=self.content_link)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Python2 Package instance.')
            self.fail("Error creating the Python2 Package instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_python2package(self):
        '''
        Deletes specified Python2 Package instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Python2 Package instance {0}".format(self.name))
        try:
            response = self.mgmt_client.python2_package.delete(resource_group_name=self.resource_group,
                                                               automation_account_name=self.automation_account_name,
                                                               package_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Python2 Package instance.')
            self.fail("Error deleting the Python2 Package instance: {0}".format(str(e)))

        return True

    def get_python2package(self):
        '''
        Gets the properties of the specified Python2 Package.

        :return: deserialized Python2 Package instance state dictionary
        '''
        self.log("Checking if the Python2 Package instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.python2_package.get(resource_group_name=self.resource_group,
                                                            automation_account_name=self.automation_account_name,
                                                            package_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Python2 Package instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Python2 Package instance.')
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


def main():
    """Main execution"""
    AzureRMPython2Package()


if __name__ == '__main__':
    main()
