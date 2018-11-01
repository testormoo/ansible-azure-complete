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
module: azure_rm_blueprintpublishedblueprint
version_added: "2.8"
short_description: Manage Published Blueprint instance.
description:
    - Create, update and delete instance of Published Blueprint.

options:
    management_group_name:
        description:
            - ManagementGroup where blueprint stores.
        required: True
    blueprint_name:
        description:
            - name of the blueprint.
        required: True
    version_id:
        description:
            - version of the published blueprint.
        required: True
    state:
      description:
        - Assert the state of the Published Blueprint.
        - Use 'present' to create or update an Published Blueprint and 'absent' to delete it.
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
  - name: Create (or update) Published Blueprint
    azure_rm_blueprintpublishedblueprint:
      management_group_name: ContosoOnlineGroup
      blueprint_name: simpleBlueprint
      version_id: v2
'''

RETURN = '''
id:
    description:
        - String Id used to locate any resource on Azure.
    returned: always
    type: str
    sample: id
status:
    description:
        - Status of the Blueprint. This field is readonly.
    returned: always
    type: complex
    sample: status
    contains:
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.blueprint import BlueprintManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPublishedBlueprints(AzureRMModuleBase):
    """Configuration class for an Azure RM Published Blueprint resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            management_group_name=dict(
                type='str',
                required=True
            ),
            blueprint_name=dict(
                type='str',
                required=True
            ),
            version_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.management_group_name = None
        self.blueprint_name = None
        self.version_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPublishedBlueprints, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BlueprintManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_publishedblueprint()

        if not old_response:
            self.log("Published Blueprint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Published Blueprint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Published Blueprint instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Published Blueprint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_publishedblueprint()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Published Blueprint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_publishedblueprint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_publishedblueprint():
                time.sleep(20)
        else:
            self.log("Published Blueprint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_publishedblueprint(self):
        '''
        Creates or updates Published Blueprint with the specified configuration.

        :return: deserialized Published Blueprint instance state dictionary
        '''
        self.log("Creating / Updating the Published Blueprint instance {0}".format(self.version_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.published_blueprints.create(management_group_name=self.management_group_name,
                                                                        blueprint_name=self.blueprint_name,
                                                                        version_id=self.version_id)
            else:
                response = self.mgmt_client.published_blueprints.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Published Blueprint instance.')
            self.fail("Error creating the Published Blueprint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_publishedblueprint(self):
        '''
        Deletes specified Published Blueprint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Published Blueprint instance {0}".format(self.version_id))
        try:
            response = self.mgmt_client.published_blueprints.delete(management_group_name=self.management_group_name,
                                                                    blueprint_name=self.blueprint_name,
                                                                    version_id=self.version_id)
        except CloudError as e:
            self.log('Error attempting to delete the Published Blueprint instance.')
            self.fail("Error deleting the Published Blueprint instance: {0}".format(str(e)))

        return True

    def get_publishedblueprint(self):
        '''
        Gets the properties of the specified Published Blueprint.

        :return: deserialized Published Blueprint instance state dictionary
        '''
        self.log("Checking if the Published Blueprint instance {0} is present".format(self.version_id))
        found = False
        try:
            response = self.mgmt_client.published_blueprints.get(management_group_name=self.management_group_name,
                                                                 blueprint_name=self.blueprint_name,
                                                                 version_id=self.version_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Published Blueprint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Published Blueprint instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': {
            }
        }
        return d


def main():
    """Main execution"""
    AzureRMPublishedBlueprints()


if __name__ == '__main__':
    main()