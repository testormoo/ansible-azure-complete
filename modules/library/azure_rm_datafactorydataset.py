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
module: azure_rm_datafactorydataset
version_added: "2.8"
short_description: Manage Azure Dataset instance.
description:
    - Create, update and delete instance of Azure Dataset.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    name:
        description:
            - The dataset name.
        required: True
    if_match:
        description:
            - ETag of the dataset entity.  Should only be specified for update, for which it should match existing entity or can be * for unconditional update.
    additional_properties:
        description:
            - Unmatched properties from the message are deserialized this collection
    description:
        description:
            - Dataset description.
    structure:
        description:
            - "Columns that define the structure of the dataset. I(type): array (or Expression with resultType array), itemType: DatasetDataElement."
    linked_service_name:
        description:
            - Linked service reference.
            - Required when C(state) is I(present).
        suboptions:
            type:
                description:
                    - Linked service reference type.
                    - Required when C(state) is I(present).
            reference_name:
                description:
                    - Reference LinkedService name.
                    - Required when C(state) is I(present).
            parameters:
                description:
                    - Arguments for LinkedService.
    parameters:
        description:
            - Parameters for dataset.
    annotations:
        description:
            - List of tags that can be used for describing the Dataset.
        type: list
    folder:
        description:
            - The folder that this Dataset is in. If not specified, Dataset will appear at the root level.
        suboptions:
            name:
                description:
                    - The name of the folder that this Dataset is in.
    type:
        description:
            - Constant filled by server.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Dataset.
        - Use 'present' to create or update an Dataset and 'absent' to delete it.
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
  - name: Create (or update) Dataset
    azure_rm_datafactorydataset:
      resource_group: exampleResourceGroup
      factory_name: exampleFactoryName
      name: exampleDataset
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: "/subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/exampleFactoryN
            ame/datasets/exampleDataset"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDataset(AzureRMModuleBase):
    """Configuration class for an Azure RM Dataset resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            factory_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            additional_properties=dict(
                type='dict'
            ),
            description=dict(
                type='str'
            ),
            structure=dict(
                type='str'
            ),
            linked_service_name=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str'
                    ),
                    reference_name=dict(
                        type='str'
                    ),
                    parameters=dict(
                        type='dict'
                    )
                )
            ),
            parameters=dict(
                type='dict'
            ),
            annotations=dict(
                type='list'
            ),
            folder=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    )
                )
            ),
            type=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.factory_name = None
        self.name = None
        self.if_match = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDataset, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.properties[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_dataset()

        if not old_response:
            self.log("Dataset instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Dataset instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dataset instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dataset()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dataset instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dataset()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Dataset instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_dataset(self):
        '''
        Creates or updates Dataset with the specified configuration.

        :return: deserialized Dataset instance state dictionary
        '''
        self.log("Creating / Updating the Dataset instance {0}".format(self.name))

        try:
            response = self.mgmt_client.datasets.create_or_update(resource_group_name=self.resource_group,
                                                                  factory_name=self.factory_name,
                                                                  dataset_name=self.name,
                                                                  properties=self.properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Dataset instance.')
            self.fail("Error creating the Dataset instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_dataset(self):
        '''
        Deletes specified Dataset instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Dataset instance {0}".format(self.name))
        try:
            response = self.mgmt_client.datasets.delete(resource_group_name=self.resource_group,
                                                        factory_name=self.factory_name,
                                                        dataset_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Dataset instance.')
            self.fail("Error deleting the Dataset instance: {0}".format(str(e)))

        return True

    def get_dataset(self):
        '''
        Gets the properties of the specified Dataset.

        :return: deserialized Dataset instance state dictionary
        '''
        self.log("Checking if the Dataset instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.datasets.get(resource_group_name=self.resource_group,
                                                     factory_name=self.factory_name,
                                                     dataset_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Dataset instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Dataset instance.')
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
    AzureRMDataset()


if __name__ == '__main__':
    main()
