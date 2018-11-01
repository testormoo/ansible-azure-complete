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
module: azure_rm_applicationinsightsannotation
version_added: "2.8"
short_description: Manage Annotation instance.
description:
    - Create, update and delete instance of Annotation.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    resource_name:
        description:
            - The name of the Application Insights component resource.
        required: True
    annotation_properties:
        description:
            - Properties that need to be specified to create an annotation of a Application Insights component.
        required: True
        suboptions:
            annotation_name:
                description:
                    - Name of annotation
            category:
                description:
                    - Category of annotation, free form
            event_time:
                description:
                    - Time when event occurred
            id:
                description:
                    - Unique Id for annotation
            related_annotation:
                description:
                    - Related parent annotation if any
    state:
      description:
        - Assert the state of the Annotation.
        - Use 'present' to create or update an Annotation and 'absent' to delete it.
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
  - name: Create (or update) Annotation
    azure_rm_applicationinsightsannotation:
      resource_group: my-resource-group
      resource_name: my-component
      annotation_properties:
        annotation_name: TestAnnotation
        category: Text
        event_time: 2018-01-31T13:41:38.657Z
        id: 444e2c08-274a-4bbb-a89e-d77bb720f44a
'''

RETURN = '''
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAnnotations(AzureRMModuleBase):
    """Configuration class for an Azure RM Annotation resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            annotation_properties=dict(
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
        self.resource_name = None
        self.annotation_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAnnotations, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "annotation_name":
                    self.annotation_properties["annotation_name"] = kwargs[key]
                elif key == "category":
                    self.annotation_properties["category"] = kwargs[key]
                elif key == "event_time":
                    self.annotation_properties["event_time"] = kwargs[key]
                elif key == "id":
                    self.annotation_properties["id"] = kwargs[key]
                elif key == "related_annotation":
                    self.annotation_properties["related_annotation"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_annotation()

        if not old_response:
            self.log("Annotation instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Annotation instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Annotation instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Annotation instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_annotation()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Annotation instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_annotation()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_annotation():
                time.sleep(20)
        else:
            self.log("Annotation instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_annotation(self):
        '''
        Creates or updates Annotation with the specified configuration.

        :return: deserialized Annotation instance state dictionary
        '''
        self.log("Creating / Updating the Annotation instance {0}".format(self.annotation_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.annotations.create(resource_group_name=self.resource_group,
                                                               resource_name=self.resource_name,
                                                               annotation_properties=self.annotation_properties)
            else:
                response = self.mgmt_client.annotations.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Annotation instance.')
            self.fail("Error creating the Annotation instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_annotation(self):
        '''
        Deletes specified Annotation instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Annotation instance {0}".format(self.annotation_id))
        try:
            response = self.mgmt_client.annotations.delete(resource_group_name=self.resource_group,
                                                           resource_name=self.resource_name,
                                                           annotation_id=self.annotation_id)
        except CloudError as e:
            self.log('Error attempting to delete the Annotation instance.')
            self.fail("Error deleting the Annotation instance: {0}".format(str(e)))

        return True

    def get_annotation(self):
        '''
        Gets the properties of the specified Annotation.

        :return: deserialized Annotation instance state dictionary
        '''
        self.log("Checking if the Annotation instance {0} is present".format(self.annotation_id))
        found = False
        try:
            response = self.mgmt_client.annotations.get(resource_group_name=self.resource_group,
                                                        resource_name=self.resource_name,
                                                        annotation_id=self.annotation_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Annotation instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Annotation instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMAnnotations()


if __name__ == '__main__':
    main()
