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
short_description: Manage Azure Gallery Image Version instance.
description:
    - Create, update and delete instance of Azure Gallery Image Version.

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
    name:
        description:
            - "The name of the gallery Image Version to be created. Needs to follow semantic version name pattern: The allowed characters are digit and
               period. Digits must be within the range of a 32-bit integer. Format: <MajorVersion>.<MinorVersion>.<Patch>"
        required: True
    location:
        description:
            - Resource location
            - Required when C(state) is I(present).
    publishing_profile:
        description:
            - Required when C(state) is I(present).
        suboptions:
            target_regions:
                description:
                    - The target regions where the Image Version is going to be replicated to. This property is updateable.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the region.
                            - Required when C(state) is I(present).
                    regional_replica_count:
                        description:
                            - The number of replicas of the Image Version to be created per region. This property is updateable.
            source:
                description:
                    - Required when C(state) is I(present).
                suboptions:
                    managed_image:
                        description:
                            - Required when C(state) is I(present).
                        suboptions:
                            id:
                                description:
                                    - The managed artifact id.
                                    - Required when C(state) is I(present).
            replica_count:
                description:
                    - "The number of replicas of the Image Version to be created per region. This property would take effect for a region when
                       regionalReplicaCount is not specified. This property is updateable."
            exclude_from_latest:
                description:
                    - "If set to true, Virtual Machines deployed from the latest version of the Image Definition won't use this Image Version."
            end_of_life_date:
                description:
                    - The end of life date of the gallery Image Version. This property can be used for decommissioning purposes. This property is updateable.
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
      name: 1.0.0
      location: West US
      publishing_profile:
        target_regions:
          - name: West US
            regional_replica_count: 1
        source:
          managed_image:
            id: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/images/{imageName}
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMGalleryImageVersion(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            publishing_profile=dict(
                type='dict',
                options=dict(
                    target_regions=dict(
                        type='list',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            regional_replica_count=dict(
                                type='int'
                            )
                        )
                    ),
                    source=dict(
                        type='dict',
                        options=dict(
                            managed_image=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    replica_count=dict(
                        type='int'
                    ),
                    exclude_from_latest=dict(
                        type='str'
                    ),
                    end_of_life_date=dict(
                        type='datetime'
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
        self.gallery_name = None
        self.gallery_image_name = None
        self.name = None
        self.gallery_image_version = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGalleryImageVersion, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.gallery_image_version[key] = kwargs[key]

        dict_resource_id(self.gallery_image_version, ['publishing_profile', 'source', 'managed_image', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

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
                if (not default_compare(self.gallery_image_version, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Gallery Image Version instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_galleryimageversion()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Gallery Image Version instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_galleryimageversion()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Gallery Image Version instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_galleryimageversion(self):
        '''
        Creates or updates Gallery Image Version with the specified configuration.

        :return: deserialized Gallery Image Version instance state dictionary
        '''
        self.log("Creating / Updating the Gallery Image Version instance {0}".format(self.name))

        try:
            response = self.mgmt_client.gallery_image_versions.create_or_update(resource_group_name=self.resource_group,
                                                                                gallery_name=self.gallery_name,
                                                                                gallery_image_name=self.gallery_image_name,
                                                                                gallery_image_version_name=self.name,
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
        self.log("Deleting the Gallery Image Version instance {0}".format(self.name))
        try:
            response = self.mgmt_client.gallery_image_versions.delete(resource_group_name=self.resource_group,
                                                                      gallery_name=self.gallery_name,
                                                                      gallery_image_name=self.gallery_image_name,
                                                                      gallery_image_version_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Gallery Image Version instance.')
            self.fail("Error deleting the Gallery Image Version instance: {0}".format(str(e)))

        return True

    def get_galleryimageversion(self):
        '''
        Gets the properties of the specified Gallery Image Version.

        :return: deserialized Gallery Image Version instance state dictionary
        '''
        self.log("Checking if the Gallery Image Version instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.gallery_image_versions.get(resource_group_name=self.resource_group,
                                                                   gallery_name=self.gallery_name,
                                                                   gallery_image_name=self.gallery_image_name,
                                                                   gallery_image_version_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Gallery Image Version instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Gallery Image Version instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMGalleryImageVersion()


if __name__ == '__main__':
    main()
