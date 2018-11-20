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
module: azure_rm_webservice
version_added: "2.8"
short_description: Manage Web Service instance.
description:
    - Create, update and delete instance of Web Service.

options:
    resource_group:
        description:
            - Name of the resource group in which the web service is located.
        required: True
    name:
        description:
            - The name of the web service.
        required: True
    create_or_update_payload:
        description:
            - The payload that is used to create or update the web service.
        required: True
        suboptions:
            location:
                description:
                    - Specifies the location of the resource.
                    - Required when C(state) is I(present).
            title:
                description:
                    - The title of the web service.
            description:
                description:
                    - The description of the web service.
            keys:
                description:
                    - "Contains the web service provisioning keys. If you do not specify provisioning keys, the Azure Machine Learning system generates them
                       for you. Note: The keys are not returned from calls to GET operations."
                suboptions:
                    primary:
                        description:
                            - The primary access key.
                    secondary:
                        description:
                            - The secondary access key.
            read_only:
                description:
                    - "When set to true, indicates that the web service is read-only and can no longer be updated or patched, only removed. Default, is
                       false. Note: Once set to true, you cannot change its value."
            expose_sample_data:
                description:
                    - "When set to true, sample data is included in the web service's swagger definition. The default value is true."
            realtime_configuration:
                description:
                    - Contains the configuration settings for the web service endpoint.
                suboptions:
                    max_concurrent_calls:
                        description:
                            - "Specifies the maximum concurrent calls that can be made to the web service. Minimum value: 4, Maximum value: 200."
            diagnostics:
                description:
                    - Settings controlling the diagnostics traces collection for the web service.
                suboptions:
                    level:
                        description:
                            - "Specifies the verbosity of the diagnostic output. Valid values are: C(none) - disables tracing; C(error) - collects only
                               C(error) (stderr) traces; C(all) - collects C(all) traces (stdout and stderr)."
                            - Required when C(state) is I(present).
                        choices:
                            - 'none'
                            - 'error'
                            - 'all'
                    expiry:
                        description:
                            - Specifies the date and time when the logging will cease. If null, diagnostic collection is not time limited.
            storage_account:
                description:
                    - "Specifies the storage account that Azure Machine Learning uses to store information about the web service. Only the name of the
                       storage account is returned from calls to GET operations. When updating the storage account information, you must ensure that all
                       necessary I(assets) are available in the new storage account or calls to your web service will fail."
                suboptions:
                    name:
                        description:
                            - Specifies the name of the storage account.
                    key:
                        description:
                            - Specifies the key used to access the storage account.
            machine_learning_workspace:
                description:
                    - Specifies the Machine Learning workspace containing the experiment that is source for the web service.
                suboptions:
                    id:
                        description:
                            - Specifies the workspace ID of the machine learning workspace associated with the web service
                            - Required when C(state) is I(present).
            commitment_plan:
                description:
                    - "Contains the commitment plan associated with this web service. Set at creation time. Once set, this value cannot be changed. Note:
                       The commitment plan is not returned from calls to GET operations."
                suboptions:
                    id:
                        description:
                            - Specifies the Azure Resource Manager ID of the commitment plan associated with the web service.
                            - Required when C(state) is I(present).
            input:
                description:
                    - "Contains the Swagger 2.0 schema describing one or more of the web service's inputs. For more information, see the Swagger
                       specification."
                suboptions:
                    title:
                        description:
                            - The title of your Swagger schema.
                    description:
                        description:
                            - The description of the Swagger schema.
                    type:
                        description:
                            - "The type of the entity described in swagger. Always 'object'."
                            - Required when C(state) is I(present).
            output:
                description:
                    - "Contains the Swagger 2.0 schema describing one or more of the web service's outputs. For more information, see the Swagger
                       specification."
                suboptions:
                    title:
                        description:
                            - The title of your Swagger schema.
                    description:
                        description:
                            - The description of the Swagger schema.
                    type:
                        description:
                            - "The type of the entity described in swagger. Always 'object'."
                            - Required when C(state) is I(present).
            example_request:
                description:
                    - "Defines sample I(input) data for one or more of the service's inputs."
                suboptions:
                    inputs:
                        description:
                            - "Sample input data for the web service's input(s) given as an input name to sample input values matrix map."
                    global_parameters:
                        description:
                            - "Sample input data for the web service's global parameters"
            assets:
                description:
                    - Contains user defined properties describing web service assets. Properties are expressed as Key/Value pairs.
            parameters:
                description:
                    - "The set of global parameters values defined for the web service, given as a global parameter name to default value map. If no default
                       value is specified, the parameter is considered to be required."
            payloads_in_blob_storage:
                description:
                    - "When set to true, indicates that the payload size is larger than 3 MB. Otherwise false. If the payload size exceed 3 MB, the payload
                       is stored in a blob and the I(payloads_location) parameter contains the URI of the blob. Otherwise, this will be set to false and
                       I(assets), I(input), I(output), Package, I(parameters), I(example_request) are inline. The Payload sizes is determined by adding the
                       size of the I(assets), I(input), I(output), Package, I(parameters), and the I(example_request)."
            payloads_location:
                description:
                    - "The URI of the payload blob. This paramater contains a value only if the I(payloads_in_blob_storage) parameter is set to true.
                       Otherwise is set to null."
                suboptions:
                    uri:
                        description:
                            - "The URI from which the blob is accessible from. For example, aml://abc for system assets or https://xyz for user assets or
                               payload."
                            - Required when C(state) is I(present).
                    credentials:
                        description:
                            - Access credentials for the blob, if applicable (e.g. blob specified by storage account connection string + blob I(uri))
            package_type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Web Service.
        - Use 'present' to create or update an Web Service and 'absent' to delete it.
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
  - name: Create (or update) Web Service
    azure_rm_webservice:
      resource_group: OneResourceGroupName
      name: TargetWebServiceName
      create_or_update_payload:
        location: West US
        title: Web Service Title
        description: Web Service Description
        read_only: False
        expose_sample_data: True
        realtime_configuration:
          max_concurrent_calls: 4
        diagnostics:
          level: None
        storage_account:
          name: Storage_Name
          key: Storage_Key
        machine_learning_workspace:
          id: workspaceId
        commitment_plan:
          id: /subscriptions/subscriptionId/resourceGroups/resourceGroupName/providers/Microsoft.MachineLearning/commitmentPlans/commitmentPlanName
        input:
          type: object
        output:
          type: object
        example_request:
          inputs: {
  "input1": [
    [
      "age"
    ],
    [
      "workclass"
    ],
    [
      "fnlwgt"
    ],
    [
      "education"
    ],
    [
      "education-num"
    ]
  ]
}
        assets: {
  "asset1": {
    "name": "Execute R Script",
    "type": "Module",
    "locationInfo": {
      "uri": "aml://module/moduleId-1",
      "credentials": ""
    }
  },
  "asset2": {
    "name": "Import Data",
    "type": "Module",
    "locationInfo": {
      "uri": "aml://module/moduleId-2",
      "credentials": ""
    }
  }
}
        parameters: {}
        payloads_in_blob_storage: False
'''

RETURN = '''
id:
    description:
        - Specifies the resource ID.
    returned: always
    type: str
    sample: TheWebServiceId
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.webservices import AzureMLWebServicesManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWebServices(AzureRMModuleBase):
    """Configuration class for an Azure RM Web Service resource"""

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
            create_or_update_payload=dict(
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
        self.create_or_update_payload = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWebServices, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.create_or_update_payload["location"] = kwargs[key]
                elif key == "title":
                    self.create_or_update_payload.setdefault("properties", {})["title"] = kwargs[key]
                elif key == "description":
                    self.create_or_update_payload.setdefault("properties", {})["description"] = kwargs[key]
                elif key == "keys":
                    self.create_or_update_payload.setdefault("properties", {})["keys"] = kwargs[key]
                elif key == "read_only":
                    self.create_or_update_payload.setdefault("properties", {})["read_only"] = kwargs[key]
                elif key == "expose_sample_data":
                    self.create_or_update_payload.setdefault("properties", {})["expose_sample_data"] = kwargs[key]
                elif key == "realtime_configuration":
                    self.create_or_update_payload.setdefault("properties", {})["realtime_configuration"] = kwargs[key]
                elif key == "diagnostics":
                    ev = kwargs[key]
                    if 'level' in ev:
                        if ev['level'] == 'none':
                            ev['level'] = 'None'
                        elif ev['level'] == 'error':
                            ev['level'] = 'Error'
                        elif ev['level'] == 'all':
                            ev['level'] = 'All'
                    self.create_or_update_payload.setdefault("properties", {})["diagnostics"] = ev
                elif key == "storage_account":
                    self.create_or_update_payload.setdefault("properties", {})["storage_account"] = kwargs[key]
                elif key == "machine_learning_workspace":
                    self.create_or_update_payload.setdefault("properties", {})["machine_learning_workspace"] = kwargs[key]
                elif key == "commitment_plan":
                    self.create_or_update_payload.setdefault("properties", {})["commitment_plan"] = kwargs[key]
                elif key == "input":
                    self.create_or_update_payload.setdefault("properties", {})["input"] = kwargs[key]
                elif key == "output":
                    self.create_or_update_payload.setdefault("properties", {})["output"] = kwargs[key]
                elif key == "example_request":
                    self.create_or_update_payload.setdefault("properties", {})["example_request"] = kwargs[key]
                elif key == "assets":
                    self.create_or_update_payload.setdefault("properties", {})["assets"] = kwargs[key]
                elif key == "parameters":
                    self.create_or_update_payload.setdefault("properties", {})["parameters"] = kwargs[key]
                elif key == "payloads_in_blob_storage":
                    self.create_or_update_payload.setdefault("properties", {})["payloads_in_blob_storage"] = kwargs[key]
                elif key == "payloads_location":
                    self.create_or_update_payload.setdefault("properties", {})["payloads_location"] = kwargs[key]
                elif key == "package_type":
                    self.create_or_update_payload.setdefault("properties", {})["package_type"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMLWebServicesManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_webservice()

        if not old_response:
            self.log("Web Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Web Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Web Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_webservice()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Web Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_webservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_webservice():
                time.sleep(20)
        else:
            self.log("Web Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_webservice(self):
        '''
        Creates or updates Web Service with the specified configuration.

        :return: deserialized Web Service instance state dictionary
        '''
        self.log("Creating / Updating the Web Service instance {0}".format(self.))

        try:
            response = self.mgmt_client.web_services.create_or_update(resource_group_name=self.resource_group,
                                                                      web_service_name=self.name,
                                                                      create_or_update_payload=self.create_or_update_payload)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Web Service instance.')
            self.fail("Error creating the Web Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_webservice(self):
        '''
        Deletes specified Web Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Web Service instance {0}".format(self.))
        try:
            response = self.mgmt_client.web_services.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Web Service instance.')
            self.fail("Error deleting the Web Service instance: {0}".format(str(e)))

        return True

    def get_webservice(self):
        '''
        Gets the properties of the specified Web Service.

        :return: deserialized Web Service instance state dictionary
        '''
        self.log("Checking if the Web Service instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.web_services.get(resource_group_name=self.resource_group,
                                                         web_service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Web Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Web Service instance.')
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
    AzureRMWebServices()


if __name__ == '__main__':
    main()
