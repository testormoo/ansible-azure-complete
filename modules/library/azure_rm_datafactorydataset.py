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
short_description: Manage Dataset instance.
description:
    - Create, update and delete instance of Dataset.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    dataset_name:
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
        required: True
        suboptions:
            type:
                description:
                    - Linked service reference type.
                required: True
            reference_name:
                description:
                    - Reference LinkedService name.
                required: True
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
        required: True
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
      dataset_name: exampleDataset
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


class AzureRMDatasets(AzureRMModuleBase):
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
            dataset_name=dict(
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
                required=True
            ),
            parameters=dict(
                type='dict'
            ),
            annotations=dict(
                type='list'
            ),
            folder=dict(
                type='dict'
            ),
            type=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.factory_name = None
        self.dataset_name = None
        self.if_match = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDatasets, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "additional_properties":
                    self.properties["additional_properties"] = kwargs[key]
                elif key == "description":
                    self.properties["description"] = kwargs[key]
                elif key == "structure":
                    self.properties["structure"] = kwargs[key]
                elif key == "linked_service_name":
                    self.properties["linked_service_name"] = kwargs[key]
                elif key == "parameters":
                    self.properties["parameters"] = kwargs[key]
                elif key == "annotations":
                    self.properties["annotations"] = kwargs[key]
                elif key == "folder":
                    self.properties["folder"] = kwargs[key]
                elif key == "type":
                    self.properties["type"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Dataset instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dataset instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dataset()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dataset instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dataset()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_dataset():
                time.sleep(20)
        else:
            self.log("Dataset instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_dataset(self):
        '''
        Creates or updates Dataset with the specified configuration.

        :return: deserialized Dataset instance state dictionary
        '''
        self.log("Creating / Updating the Dataset instance {0}".format(self.dataset_name))

        try:
            response = self.mgmt_client.datasets.create_or_update(resource_group_name=self.resource_group,
                                                                  factory_name=self.factory_name,
                                                                  dataset_name=self.dataset_name,
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
        self.log("Deleting the Dataset instance {0}".format(self.dataset_name))
        try:
            response = self.mgmt_client.datasets.delete(resource_group_name=self.resource_group,
                                                        factory_name=self.factory_name,
                                                        dataset_name=self.dataset_name)
        except CloudError as e:
            self.log('Error attempting to delete the Dataset instance.')
            self.fail("Error deleting the Dataset instance: {0}".format(str(e)))

        return True

    def get_dataset(self):
        '''
        Gets the properties of the specified Dataset.

        :return: deserialized Dataset instance state dictionary
        '''
        self.log("Checking if the Dataset instance {0} is present".format(self.dataset_name))
        found = False
        try:
            response = self.mgmt_client.datasets.get(resource_group_name=self.resource_group,
                                                     factory_name=self.factory_name,
                                                     dataset_name=self.dataset_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Dataset instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Dataset instance.')
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
    AzureRMDatasets()


if __name__ == '__main__':
    main()
