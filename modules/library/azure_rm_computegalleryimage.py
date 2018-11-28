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
module: azure_rm_computegalleryimage
version_added: "2.8"
short_description: Manage Azure Gallery Image instance.
description:
    - Create, update and delete instance of Azure Gallery Image.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    gallery_name:
        description:
            - The name of the Shared Image Gallery in which the Image Definition is to be created.
        required: True
    name:
        description:
            - "The name of the gallery Image Definition to be created or updated. The allowed characters are alphabets and numbers with dots, dashes, and
               periods allowed in the middle. The maximum length is 80 characters."
        required: True
    location:
        description:
            - Resource location
            - Required when C(state) is I(present).
    description:
        description:
            - The description of this gallery Image Definition resource. This property is updateable.
    eula:
        description:
            - The Eula agreement for the gallery Image Definition.
    privacy_statement_uri:
        description:
            - The privacy statement uri.
    release_note_uri:
        description:
            - The release note uri.
    os_type:
        description:
            - "This property allows you to specify the type of the OS that is included in the disk when creating a VM from a managed image. <br><br>
               Possible values are: <br><br> **C(windows)** <br><br> **C(linux)**."
            - Required when C(state) is I(present).
        choices:
            - 'windows'
            - 'linux'
    os_state:
        description:
            - "The allowed values for OS State are 'C(generalized)'."
            - Required when C(state) is I(present).
        choices:
            - 'generalized'
            - 'specialized'
    end_of_life_date:
        description:
            - The end of life date of the gallery Image Definition. This property can be used for decommissioning purposes. This property is updateable.
    identifier:
        description:
            - Required when C(state) is I(present).
        suboptions:
            publisher:
                description:
                    - The name of the gallery Image Definition publisher.
                    - Required when C(state) is I(present).
            offer:
                description:
                    - The name of the gallery Image Definition offer.
                    - Required when C(state) is I(present).
            sku:
                description:
                    - The name of the gallery Image Definition SKU.
                    - Required when C(state) is I(present).
    recommended:
        description:
        suboptions:
            v_cp_us:
                description:
                suboptions:
                    min:
                        description:
                            - The minimum number of the resource.
                    max:
                        description:
                            - The maximum number of the resource.
            memory:
                description:
                suboptions:
                    min:
                        description:
                            - The minimum number of the resource.
                    max:
                        description:
                            - The maximum number of the resource.
    disallowed:
        description:
        suboptions:
            disk_types:
                description:
                    - A list of disk types.
                type: list
    purchase_plan:
        description:
        suboptions:
            name:
                description:
                    - The plan ID.
            publisher:
                description:
                    - The publisher ID.
            product:
                description:
                    - The product ID.
    state:
      description:
        - Assert the state of the Gallery Image.
        - Use 'present' to create or update an Gallery Image and 'absent' to delete it.
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
  - name: Create (or update) Gallery Image
    azure_rm_computegalleryimage:
      resource_group: myResourceGroup
      gallery_name: myGalleryName
      name: myGalleryImageName
      location: West US
      os_type: Windows
      os_state: Generalized
      identifier:
        publisher: myPublisherName
        offer: myOfferName
        sku: mySkuName
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


class AzureRMGalleryImage(AzureRMModuleBase):
    """Configuration class for an Azure RM Gallery Image resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            eula=dict(
                type='str'
            ),
            privacy_statement_uri=dict(
                type='str'
            ),
            release_note_uri=dict(
                type='str'
            ),
            os_type=dict(
                type='str',
                choices=['windows',
                         'linux']
            ),
            os_state=dict(
                type='str',
                choices=['generalized',
                         'specialized']
            ),
            end_of_life_date=dict(
                type='datetime'
            ),
            identifier=dict(
                type='dict',
                options=dict(
                    publisher=dict(
                        type='str'
                    ),
                    offer=dict(
                        type='str'
                    ),
                    sku=dict(
                        type='str'
                    )
                )
            ),
            recommended=dict(
                type='dict',
                options=dict(
                    v_cp_us=dict(
                        type='dict',
                        options=dict(
                            min=dict(
                                type='int'
                            ),
                            max=dict(
                                type='int'
                            )
                        )
                    ),
                    memory=dict(
                        type='dict',
                        options=dict(
                            min=dict(
                                type='int'
                            ),
                            max=dict(
                                type='int'
                            )
                        )
                    )
                )
            ),
            disallowed=dict(
                type='dict',
                options=dict(
                    disk_types=dict(
                        type='list'
                    )
                )
            ),
            purchase_plan=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    publisher=dict(
                        type='str'
                    ),
                    product=dict(
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
        self.gallery_name = None
        self.name = None
        self.gallery_image = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGalleryImage, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.gallery_image[key] = kwargs[key]

        dict_camelize(self.gallery_image, ['os_type'], True)
        dict_camelize(self.gallery_image, ['os_state'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_galleryimage()

        if not old_response:
            self.log("Gallery Image instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Gallery Image instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.gallery_image, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Gallery Image instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_galleryimage()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Gallery Image instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_galleryimage()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Gallery Image instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_galleryimage(self):
        '''
        Creates or updates Gallery Image with the specified configuration.

        :return: deserialized Gallery Image instance state dictionary
        '''
        self.log("Creating / Updating the Gallery Image instance {0}".format(self.name))

        try:
            response = self.mgmt_client.gallery_images.create_or_update(resource_group_name=self.resource_group,
                                                                        gallery_name=self.gallery_name,
                                                                        gallery_image_name=self.name,
                                                                        gallery_image=self.gallery_image)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Gallery Image instance.')
            self.fail("Error creating the Gallery Image instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_galleryimage(self):
        '''
        Deletes specified Gallery Image instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Gallery Image instance {0}".format(self.name))
        try:
            response = self.mgmt_client.gallery_images.delete(resource_group_name=self.resource_group,
                                                              gallery_name=self.gallery_name,
                                                              gallery_image_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Gallery Image instance.')
            self.fail("Error deleting the Gallery Image instance: {0}".format(str(e)))

        return True

    def get_galleryimage(self):
        '''
        Gets the properties of the specified Gallery Image.

        :return: deserialized Gallery Image instance state dictionary
        '''
        self.log("Checking if the Gallery Image instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.gallery_images.get(resource_group_name=self.resource_group,
                                                           gallery_name=self.gallery_name,
                                                           gallery_image_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Gallery Image instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Gallery Image instance.')
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


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def main():
    """Main execution"""
    AzureRMGalleryImage()


if __name__ == '__main__':
    main()
