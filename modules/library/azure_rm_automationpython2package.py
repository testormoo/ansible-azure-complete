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
short_description: Manage Python2 Package instance.
description:
    - Create, update and delete instance of Python2 Package.

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
    content_link:
        description:
            - Gets or sets the module content link.
        required: True
        suboptions:
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
            content_link=dict(
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
                if key == "uri":
                    self.content_link["uri"] = kwargs[key]
                elif key == "content_hash":
                    self.content_link["content_hash"] = kwargs[key]
                elif key == "version":
                    self.content_link["version"] = kwargs[key]

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
                if (not default_compare(self.parameters, old_response, '')):
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
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_python2package():
                time.sleep(20)
        else:
            self.log("Python2 Package instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
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

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'version': d.get('version', None)
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
    AzureRMPython2Package()


if __name__ == '__main__':
    main()
