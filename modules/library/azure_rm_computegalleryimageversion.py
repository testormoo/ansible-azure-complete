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
module: azure_rm_computegalleryimageversion
version_added: "2.8"
short_description: Manage Gallery Image Version instance.
description:
    - Create, update and delete instance of Gallery Image Version.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    gallery_name:
        description:
            - The name of the Shared Image Gallery in which the Image Definition resides.
        required: True
    gallery_image_name:
        description:
            - The name of the gallery Image Definition in which the Image Version is to be created.
        required: True
    gallery_image_version_name:
        description:
            - "The name of the gallery Image Version to be created. Needs to follow semantic version name pattern: The allowed characters are digit and
               period. Digits must be within the range of a 32-bit integer. Format: <MajorVersion>.<MinorVersion>.<Patch>"
        required: True
    gallery_image_version:
        description:
            - Parameters supplied to the create or update gallery Image Version operation.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                required: True
            publishing_profile:
                description:
                required: True
                suboptions:
                    target_regions:
                        description:
                            - The target regions where the Image Version is going to be replicated to. This property is updateable.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The name of the region.
                                required: True
                            regional_replica_count:
                                description:
                                    - The number of replicas of the Image Version to be created per region. This property is updateable.
                    source:
                        description:
                        required: True
                        suboptions:
                            managed_image:
                                description:
                                required: True
                                suboptions:
                                    id:
                                        description:
                                            - The managed artifact id.
                                        required: True
                    replica_count:
                        description:
                            - "The number of replicas of the Image Version to be created per region. This property would take effect for a region when
                               regionalReplicaCount is not specified. This property is updateable."
                    exclude_from_latest:
                        description:
                            - "If set to true, Virtual Machines deployed from the latest version of the Image Definition won't use this Image Version."
                    end_of_life_date:
                        description:
                            - "The end of life date of the gallery Image Version. This property can be used for decommissioning purposes. This property is
                               updateable."
    state:
      description:
        - Assert the state of the Gallery Image Version.
        - Use 'present' to create or update an Gallery Image Version and 'absent' to delete it.
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
  - name: Create (or update) Gallery Image Version
    azure_rm_computegalleryimageversion:
      resource_group: myResourceGroup
      gallery_name: myGalleryName
      gallery_image_name: myGalleryImageName
      gallery_image_version_name: 1.0.0
      gallery_image_version:
        location: West US
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


class AzureRMGalleryImageVersions(AzureRMModuleBase):
    """Configuration class for an Azure RM Gallery Image Version resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            gallery_name=dict(
                type='str',
                required=True
            ),
            gallery_image_name=dict(
                type='str',
                required=True
            ),
            gallery_image_version_name=dict(
                type='str',
                required=True
            ),
            gallery_image_version=dict(
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
        self.gallery_name = None
        self.gallery_image_name = None
        self.gallery_image_version_name = None
        self.gallery_image_version = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGalleryImageVersions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.gallery_image_version["location"] = kwargs[key]
                elif key == "publishing_profile":
                    self.gallery_image_version["publishing_profile"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_galleryimageversion()

        if not old_response:
            self.log("Gallery Image Version instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Gallery Image Version instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Gallery Image Version instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Gallery Image Version instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_galleryimageversion()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Gallery Image Version instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_galleryimageversion()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_galleryimageversion():
                time.sleep(20)
        else:
            self.log("Gallery Image Version instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_galleryimageversion(self):
        '''
        Creates or updates Gallery Image Version with the specified configuration.

        :return: deserialized Gallery Image Version instance state dictionary
        '''
        self.log("Creating / Updating the Gallery Image Version instance {0}".format(self.gallery_image_version_name))

        try:
            response = self.mgmt_client.gallery_image_versions.create_or_update(resource_group_name=self.resource_group,
                                                                                gallery_name=self.gallery_name,
                                                                                gallery_image_name=self.gallery_image_name,
                                                                                gallery_image_version_name=self.gallery_image_version_name,
                                                                                gallery_image_version=self.gallery_image_version)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Gallery Image Version instance.')
            self.fail("Error creating the Gallery Image Version instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_galleryimageversion(self):
        '''
        Deletes specified Gallery Image Version instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Gallery Image Version instance {0}".format(self.gallery_image_version_name))
        try:
            response = self.mgmt_client.gallery_image_versions.delete(resource_group_name=self.resource_group,
                                                                      gallery_name=self.gallery_name,
                                                                      gallery_image_name=self.gallery_image_name,
                                                                      gallery_image_version_name=self.gallery_image_version_name)
        except CloudError as e:
            self.log('Error attempting to delete the Gallery Image Version instance.')
            self.fail("Error deleting the Gallery Image Version instance: {0}".format(str(e)))

        return True

    def get_galleryimageversion(self):
        '''
        Gets the properties of the specified Gallery Image Version.

        :return: deserialized Gallery Image Version instance state dictionary
        '''
        self.log("Checking if the Gallery Image Version instance {0} is present".format(self.gallery_image_version_name))
        found = False
        try:
            response = self.mgmt_client.gallery_image_versions.get(resource_group_name=self.resource_group,
                                                                   gallery_name=self.gallery_name,
                                                                   gallery_image_name=self.gallery_image_name,
                                                                   gallery_image_version_name=self.gallery_image_version_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Gallery Image Version instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Gallery Image Version instance.')
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
    AzureRMGalleryImageVersions()


if __name__ == '__main__':
    main()
