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
module: azure_rm_computegallery
version_added: "2.8"
short_description: Manage Gallery instance.
description:
    - Create, update and delete instance of Gallery.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - "The name of the Shared Image I(gallery). The allowed characters are alphabets and numbers with dots and periods allowed in the middle. The
               maximum length is 80 characters."
        required: True
    gallery:
        description:
            - Parameters supplied to the create or update Shared Image Gallery operation.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                    - Required when C(state) is I(present).
            description:
                description:
                    - The description of this Shared Image Gallery resource. This property is updateable.
            identifier:
                description:
    state:
      description:
        - Assert the state of the Gallery.
        - Use 'present' to create or update an Gallery and 'absent' to delete it.
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
  - name: Create (or update) Gallery
    azure_rm_computegallery:
      resource_group: myResourceGroup
      name: myGalleryName
      gallery:
        location: West US
        description: This is the gallery description.
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGalleries(AzureRMModuleBase):
    """Configuration class for an Azure RM Gallery resource"""

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
            gallery=dict(
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
        self.name = None
        self.gallery = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGalleries, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.gallery["location"] = kwargs[key]
                elif key == "description":
                    self.gallery["description"] = kwargs[key]
                elif key == "identifier":
                    self.gallery["identifier"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_gallery()

        if not old_response:
            self.log("Gallery instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Gallery instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Gallery instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_gallery()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Gallery instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_gallery()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_gallery():
                time.sleep(20)
        else:
            self.log("Gallery instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_gallery(self):
        '''
        Creates or updates Gallery with the specified configuration.

        :return: deserialized Gallery instance state dictionary
        '''
        self.log("Creating / Updating the Gallery instance {0}".format(self.name))

        try:
            response = self.mgmt_client.galleries.create_or_update(resource_group_name=self.resource_group,
                                                                   gallery_name=self.name,
                                                                   gallery=self.gallery)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Gallery instance.')
            self.fail("Error creating the Gallery instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_gallery(self):
        '''
        Deletes specified Gallery instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Gallery instance {0}".format(self.name))
        try:
            response = self.mgmt_client.galleries.delete(resource_group_name=self.resource_group,
                                                         gallery_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Gallery instance.')
            self.fail("Error deleting the Gallery instance: {0}".format(str(e)))

        return True

    def get_gallery(self):
        '''
        Gets the properties of the specified Gallery.

        :return: deserialized Gallery instance state dictionary
        '''
        self.log("Checking if the Gallery instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.galleries.get(resource_group_name=self.resource_group,
                                                      gallery_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Gallery instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Gallery instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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
    AzureRMGalleries()


if __name__ == '__main__':
    main()
