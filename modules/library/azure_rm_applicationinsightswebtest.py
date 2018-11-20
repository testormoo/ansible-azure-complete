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
module: azure_rm_applicationinsightswebtest
version_added: "2.8"
short_description: Manage Web Test instance.
description:
    - Create, update and delete instance of Web Test.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Application Insights webtest resource.
        required: True
    web_test_definition:
        description:
            - Properties that need to be specified to create or update an Application Insights web test definition.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                    - Required when C(state) is I(present).
            kind:
                description:
                    - The kind of web test that this web test watches. Choices are C(C(ping)) and C(C(multistep)).
                choices:
                    - 'ping'
                    - 'multistep'
            synthetic_monitor_id:
                description:
                    - Unique ID of this WebTest. This is typically the same value as the Name field.
                    - Required when C(state) is I(present).
            web_test_name:
                description:
                    - User defined name if this WebTest.
                    - Required when C(state) is I(present).
            description:
                description:
                    - Purpose/user defined descriptive test for this WebTest.
            enabled:
                description:
                    - Is the test actively being monitored.
            frequency:
                description:
                    - Interval in seconds between test runs for this WebTest. Default value is 300.
            timeout:
                description:
                    - Seconds until this WebTest will timeout and fail. Default value is 30.
            web_test_kind:
                description:
                    - The I(kind) of web test this is, valid choices are C(C(ping)) and C(C(multistep)).
                    - Required when C(state) is I(present).
                choices:
                    - 'ping'
                    - 'multistep'
            retry_enabled:
                description:
                    - Allow for retries should this WebTest fail.
            locations:
                description:
                    - A list of where to physically run the tests from to give global coverage for accessibility of your application.
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    location:
                        description:
                            - Location ID for the webtest to run from.
            configuration:
                description:
                    - An XML configuration specification for a WebTest.
                suboptions:
                    web_test:
                        description:
                            - The XML specification of a WebTest to run against an application.
    state:
      description:
        - Assert the state of the Web Test.
        - Use 'present' to create or update an Web Test and 'absent' to delete it.
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
  - name: Create (or update) Web Test
    azure_rm_applicationinsightswebtest:
      resource_group: my-resource-group
      name: my-webtest-my-component
      web_test_definition:
        location: South Central US
        kind: ping
        synthetic_monitor_id: my-webtest-my-component
        web_test_name: my-webtest-my-component
        description: Ping web test alert for mytestwebapp
        enabled: True
        frequency: 900
        timeout: 120
        web_test_kind: ping
        retry_enabled: True
        locations:
          - location: us-fl-mia-edge
        configuration:
          web_test: <WebTest Name="my-webtest" Id="678ddf96-1ab8-44c8-9274-123456789abc" Enabled="True" CssProjectStructure="" CssIteration="" Timeout="120" WorkItemIds="" xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010" Description="" CredentialUserName="" CredentialPassword="" PreAuthenticate="True" Proxy="default" StopOnError="False" RecordedResultFile="" ResultsLocale="" ><Items><Request Method="GET" Guid="a4162485-9114-fcfc-e086-123456789abc" Version="1.1" Url="http://my-component.azurewebsites.net" ThinkTime="0" Timeout="120" ParseDependentRequests="True" FollowRedirects="True" RecordResult="True" Cache="False" ResponseTimeGoal="0" Encoding="utf-8" ExpectedHttpStatusCode="200" ExpectedResponseUrl="" ReportingName="" IgnoreHttpStatusCode="False" /></Items></WebTest>
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/my-resource-group/providers/Microsoft.Insights/webtests/my-webtest-my-component
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


class AzureRMWebTests(AzureRMModuleBase):
    """Configuration class for an Azure RM Web Test resource"""

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
            web_test_definition=dict(
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
        self.web_test_definition = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWebTests, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.web_test_definition["location"] = kwargs[key]
                elif key == "kind":
                    self.web_test_definition["kind"] = kwargs[key]
                elif key == "synthetic_monitor_id":
                    self.web_test_definition["synthetic_monitor_id"] = kwargs[key]
                elif key == "web_test_name":
                    self.web_test_definition["web_test_name"] = kwargs[key]
                elif key == "description":
                    self.web_test_definition["description"] = kwargs[key]
                elif key == "enabled":
                    self.web_test_definition["enabled"] = kwargs[key]
                elif key == "frequency":
                    self.web_test_definition["frequency"] = kwargs[key]
                elif key == "timeout":
                    self.web_test_definition["timeout"] = kwargs[key]
                elif key == "web_test_kind":
                    self.web_test_definition["web_test_kind"] = kwargs[key]
                elif key == "retry_enabled":
                    self.web_test_definition["retry_enabled"] = kwargs[key]
                elif key == "locations":
                    self.web_test_definition["locations"] = kwargs[key]
                elif key == "configuration":
                    self.web_test_definition["configuration"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_webtest()

        if not old_response:
            self.log("Web Test instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Web Test instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Web Test instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_webtest()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Web Test instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_webtest()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_webtest():
                time.sleep(20)
        else:
            self.log("Web Test instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_webtest(self):
        '''
        Creates or updates Web Test with the specified configuration.

        :return: deserialized Web Test instance state dictionary
        '''
        self.log("Creating / Updating the Web Test instance {0}".format(self.name))

        try:
            response = self.mgmt_client.web_tests.create_or_update(resource_group_name=self.resource_group,
                                                                   web_test_name=self.name,
                                                                   web_test_definition=self.web_test_definition)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Web Test instance.')
            self.fail("Error creating the Web Test instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_webtest(self):
        '''
        Deletes specified Web Test instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Web Test instance {0}".format(self.name))
        try:
            response = self.mgmt_client.web_tests.delete(resource_group_name=self.resource_group,
                                                         web_test_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Web Test instance.')
            self.fail("Error deleting the Web Test instance: {0}".format(str(e)))

        return True

    def get_webtest(self):
        '''
        Gets the properties of the specified Web Test.

        :return: deserialized Web Test instance state dictionary
        '''
        self.log("Checking if the Web Test instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.web_tests.get(resource_group_name=self.resource_group,
                                                      web_test_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Web Test instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Web Test instance.')
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
    AzureRMWebTests()


if __name__ == '__main__':
    main()
