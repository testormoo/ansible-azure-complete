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
module: azure_rm_servicefabricmeshsecret
version_added: "2.8"
short_description: Manage Secret instance.
description:
    - Create, update and delete instance of Secret.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    secret_resource_name:
        description:
            - The name of the secret resource.
        required: True
    secret_resource_description:
        description:
            - Description for creating a secret resource.
        required: True
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                required: True
            kind:
                description:
                    - Constant filled by server.
                required: True
            description:
                description:
                    - User readable description of the secret.
            content_type:
                description:
                    - "The type of the content stored in the secret value. The value of this property is opaque to Service Fabric. Once set, the value of
                       this property cannot be changed."
    state:
      description:
        - Assert the state of the Secret.
        - Use 'present' to create or update an Secret and 'absent' to delete it.
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
  - name: Create (or update) Secret
    azure_rm_servicefabricmeshsecret:
      resource_group: sbz_demo
      secret_resource_name: dbConnectionString
      secret_resource_description:
        location: EastUS
        kind: inlinedValue
        description: Mongo DB connection string for backend database!
        content_type: text/plain
'''

RETURN = '''
id:
    description:
        - "Fully qualified identifier for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/secrets/dbConnectionString
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


class AzureRMSecret(AzureRMModuleBase):
    """Configuration class for an Azure RM Secret resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            secret_resource_name=dict(
                type='str',
                required=True
            ),
            secret_resource_description=dict(
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
        self.secret_resource_name = None
        self.secret_resource_description = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSecret, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.secret_resource_description["location"] = kwargs[key]
                elif key == "kind":
                    self.secret_resource_description.setdefault("properties", {})["kind"] = kwargs[key]
                elif key == "description":
                    self.secret_resource_description.setdefault("properties", {})["description"] = kwargs[key]
                elif key == "content_type":
                    self.secret_resource_description.setdefault("properties", {})["content_type"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_secret()

        if not old_response:
            self.log("Secret instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Secret instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Secret instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Secret instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_secret()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Secret instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_secret()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_secret():
                time.sleep(20)
        else:
            self.log("Secret instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_secret(self):
        '''
        Creates or updates Secret with the specified configuration.

        :return: deserialized Secret instance state dictionary
        '''
        self.log("Creating / Updating the Secret instance {0}".format(self.secret_resource_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.secret.create(resource_group_name=self.resource_group,
                                                          secret_resource_name=self.secret_resource_name,
                                                          secret_resource_description=self.secret_resource_description)
            else:
                response = self.mgmt_client.secret.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Secret instance.')
            self.fail("Error creating the Secret instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_secret(self):
        '''
        Deletes specified Secret instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Secret instance {0}".format(self.secret_resource_name))
        try:
            response = self.mgmt_client.secret.delete(resource_group_name=self.resource_group,
                                                      secret_resource_name=self.secret_resource_name)
        except CloudError as e:
            self.log('Error attempting to delete the Secret instance.')
            self.fail("Error deleting the Secret instance: {0}".format(str(e)))

        return True

    def get_secret(self):
        '''
        Gets the properties of the specified Secret.

        :return: deserialized Secret instance state dictionary
        '''
        self.log("Checking if the Secret instance {0} is present".format(self.secret_resource_name))
        found = False
        try:
            response = self.mgmt_client.secret.get(resource_group_name=self.resource_group,
                                                   secret_resource_name=self.secret_resource_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Secret instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Secret instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMSecret()


if __name__ == '__main__':
    main()
