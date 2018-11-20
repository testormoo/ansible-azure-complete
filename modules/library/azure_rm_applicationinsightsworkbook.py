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
module: azure_rm_applicationinsightsworkbook
version_added: "2.8"
short_description: Manage Workbook instance.
description:
    - Create, update and delete instance of Workbook.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Application Insights component resource.
        required: True
    workbook_properties:
        description:
            - Properties that need to be specified to create a new workbook.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
            kind:
                description:
                    - The kind of workbook. Choices are C(C(user)) and C(C(shared)).
                choices:
                    - 'user'
                    - 'shared'
            workbook_name:
                description:
                    - The C(C(user))-defined name of the workbook.
                    - Required when C(state) is I(present).
            serialized_data:
                description:
                    - Configuration of this particular workbook. Configuration data is a string containing valid JSON
                    - Required when C(state) is I(present).
            version:
                description:
                    - "This instance's version of the data model. This can change as new features are added that can be marked workbook."
            workbook_id:
                description:
                    - Internally assigned unique id of the workbook definition.
                    - Required when C(state) is I(present).
            shared_type_kind:
                description:
                    - "Enum indicating if this workbook definition is owned by a specific C(C(user)) or is C(C(shared)) between all users with access to the
                       Application Insights component."
                    - Required when C(state) is I(present).
                choices:
                    - 'user'
                    - 'shared'
            category:
                description:
                    - Workbook category, as defined by the C(C(user)) at creation time.
                    - Required when C(state) is I(present).
            workbook_tags:
                description:
                    - A list of 0 or more tags that are associated with this workbook definition
                type: list
            user_id:
                description:
                    - Unique C(C(user)) id of the specific C(C(user)) that owns this workbook.
                    - Required when C(state) is I(present).
            source_resource_id:
                description:
                    - Optional resourceId for a source resource.
    state:
      description:
        - Assert the state of the Workbook.
        - Use 'present' to create or update an Workbook and 'absent' to delete it.
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
  - name: Create (or update) Workbook
    azure_rm_applicationinsightsworkbook:
      resource_group: my-resource-group
      name: deadb33f-8bee-4d3b-a059-9be8dac93960
      workbook_properties:
        location: west us
        kind: shared
        workbook_name: Blah Blah Blah
        serialized_data: {"version":"Notebook/1.0","items":[{"type":1,"content":"{"json":"## New workbook\r\n---\r\n\r\nWelcome to your new workbook.  This area will display text formatted as markdown.\r\n\r\n\r\nWe've included a basic analytics query to get you started. Use the `Edit` button below each section to configure it or add more sections."}","halfWidth":null,"conditionalVisibility":null},{"type":3,"content":"{"version":"KqlItem/1.0","query":"union withsource=TableName *\n| summarize Count=count() by TableName\n| render barchart","showQuery":false,"size":1,"aggregation":0,"showAnnotations":false}","halfWidth":null,"conditionalVisibility":null}],"isLocked":false}
        workbook_id: deadb33f-8bee-4d3b-a059-9be8dac93960
        shared_type_kind: shared
        category: workbook
        workbook_tags:
          - [
  "TagSample01",
  "TagSample02"
]
        user_id: userId
        source_resource_id: /subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MyGroup/providers/Microsoft.Web/sites/MyTestApp-CodeLens
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: c0deea5e-3344-40f2-96f8-6f8e1c3b5722
version:
    description:
        - "This instance's version of the data model. This can change as new features are added that can be marked workbook."
    returned: always
    type: str
    sample: ME
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


class AzureRMWorkbooks(AzureRMModuleBase):
    """Configuration class for an Azure RM Workbook resource"""

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
            workbook_properties=dict(
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
        self.workbook_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWorkbooks, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.workbook_properties["location"] = kwargs[key]
                elif key == "kind":
                    self.workbook_properties["kind"] = kwargs[key]
                elif key == "workbook_name":
                    self.workbook_properties["workbook_name"] = kwargs[key]
                elif key == "serialized_data":
                    self.workbook_properties["serialized_data"] = kwargs[key]
                elif key == "version":
                    self.workbook_properties["version"] = kwargs[key]
                elif key == "workbook_id":
                    self.workbook_properties["workbook_id"] = kwargs[key]
                elif key == "shared_type_kind":
                    self.workbook_properties["shared_type_kind"] = kwargs[key]
                elif key == "category":
                    self.workbook_properties["category"] = kwargs[key]
                elif key == "workbook_tags":
                    self.workbook_properties["workbook_tags"] = kwargs[key]
                elif key == "user_id":
                    self.workbook_properties["user_id"] = kwargs[key]
                elif key == "source_resource_id":
                    self.workbook_properties["source_resource_id"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_workbook()

        if not old_response:
            self.log("Workbook instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Workbook instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Workbook instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_workbook()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Workbook instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_workbook()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_workbook():
                time.sleep(20)
        else:
            self.log("Workbook instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_workbook(self):
        '''
        Creates or updates Workbook with the specified configuration.

        :return: deserialized Workbook instance state dictionary
        '''
        self.log("Creating / Updating the Workbook instance {0}".format(self.name))

        try:
            response = self.mgmt_client.workbooks.create_or_update(resource_group_name=self.resource_group,
                                                                   resource_name=self.name,
                                                                   workbook_properties=self.workbook_properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Workbook instance.')
            self.fail("Error creating the Workbook instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_workbook(self):
        '''
        Deletes specified Workbook instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Workbook instance {0}".format(self.name))
        try:
            response = self.mgmt_client.workbooks.delete(resource_group_name=self.resource_group,
                                                         resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Workbook instance.')
            self.fail("Error deleting the Workbook instance: {0}".format(str(e)))

        return True

    def get_workbook(self):
        '''
        Gets the properties of the specified Workbook.

        :return: deserialized Workbook instance state dictionary
        '''
        self.log("Checking if the Workbook instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.workbooks.get(resource_group_name=self.resource_group,
                                                      resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Workbook instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Workbook instance.')
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
    AzureRMWorkbooks()


if __name__ == '__main__':
    main()
