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
short_description: Manage Azure Web Service instance.
description:
    - Create, update and delete instance of Azure Web Service.

options:
    resource_group:
        description:
            - Name of the resource group in which the web service is located.
        required: True
    name:
        description:
            - The name of the web service.
        required: True
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
            - "Contains the web service provisioning keys. If you do not specify provisioning keys, the Azure Machine Learning system generates them for
               you. Note: The keys are not returned from calls to GET operations."
        suboptions:
            primary:
                description:
                    - The primary access key.
            secondary:
                description:
                    - The secondary access key.
    read_only:
        description:
            - "When set to true, indicates that the web service is read-only and can no longer be updated or patched, only removed. Default, is false. Note:
               Once set to true, you cannot change its value."
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
                    - "Specifies the verbosity of the diagnostic output. Valid values are: C(none) - disables tracing; C(error) - collects only C(error)
                       (stderr) traces; C(all) - collects C(all) traces (stdout and stderr)."
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
            - "Specifies the storage account that Azure Machine Learning uses to store information about the web service. Only the name of the storage
               account is returned from calls to GET operations. When updating the storage account information, you must ensure that all necessary
               I(assets) are available in the new storage account or calls to your web service will fail."
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
            - "Contains the commitment plan associated with this web service. Set at creation time. Once set, this value cannot be changed. Note: The
               commitment plan is not returned from calls to GET operations."
        suboptions:
            id:
                description:
                    - Specifies the Azure Resource Manager ID of the commitment plan associated with the web service.
                    - Required when C(state) is I(present).
    input:
        description:
            - "Contains the Swagger 2.0 schema describing one or more of the web service's inputs. For more information, see the Swagger specification."
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
            - "Contains the Swagger 2.0 schema describing one or more of the web service's outputs. For more information, see the Swagger specification."
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
            - "The set of global parameters values defined for the web service, given as a global parameter name to default value map. If no default value
               is specified, the parameter is considered to be required."
    payloads_in_blob_storage:
        description:
            - "When set to true, indicates that the payload size is larger than 3 MB. Otherwise false. If the payload size exceed 3 MB, the payload is
               stored in a blob and the I(payloads_location) parameter contains the URI of the blob. Otherwise, this will be set to false and I(assets),
               I(input), I(output), Package, I(parameters), I(example_request) are inline. The Payload sizes is determined by adding the size of the
               I(assets), I(input), I(output), Package, I(parameters), and the I(example_request)."
    payloads_location:
        description:
            - "The URI of the payload blob. This paramater contains a value only if the I(payloads_in_blob_storage) parameter is set to true. Otherwise is
               set to null."
        suboptions:
            uri:
                description:
                    - "The URI from which the blob is accessible from. For example, aml://abc for system assets or https://xyz for user assets or payload."
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMWebService(AzureRMModuleBase):
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
            location=dict(
                type='str'
            ),
            title=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            keys=dict(
                type='dict',
                options=dict(
                    primary=dict(
                        type='str'
                    ),
                    secondary=dict(
                        type='str'
                    )
                )
            ),
            read_only=dict(
                type='str'
            ),
            expose_sample_data=dict(
                type='str'
            ),
            realtime_configuration=dict(
                type='dict',
                options=dict(
                    max_concurrent_calls=dict(
                        type='int'
                    )
                )
            ),
            diagnostics=dict(
                type='dict',
                options=dict(
                    level=dict(
                        type='str',
                        choices=['none',
                                 'error',
                                 'all']
                    ),
                    expiry=dict(
                        type='datetime'
                    )
                )
            ),
            storage_account=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    key=dict(
                        type='str'
                    )
                )
            ),
            machine_learning_workspace=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            commitment_plan=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            input=dict(
                type='dict',
                options=dict(
                    title=dict(
                        type='str'
                    ),
                    description=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    ),
                    properties=dict(
                        type='dict'
                    )
                )
            ),
            output=dict(
                type='dict',
                options=dict(
                    title=dict(
                        type='str'
                    ),
                    description=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    ),
                    properties=dict(
                        type='dict'
                    )
                )
            ),
            example_request=dict(
                type='dict',
                options=dict(
                    inputs=dict(
                        type='dict'
                    ),
                    global_parameters=dict(
                        type='dict'
                    )
                )
            ),
            assets=dict(
                type='dict'
            ),
            parameters=dict(
                type='dict'
            ),
            payloads_in_blob_storage=dict(
                type='str'
            ),
            payloads_location=dict(
                type='dict',
                options=dict(
                    uri=dict(
                        type='str'
                    ),
                    credentials=dict(
                        type='str'
                    )
                )
            ),
            package_type=dict(
                type='str'
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

        super(AzureRMWebService, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.create_or_update_payload[key] = kwargs[key]

        dict_expand(self.create_or_update_payload, ['title'])
        dict_expand(self.create_or_update_payload, ['description'])
        dict_expand(self.create_or_update_payload, ['keys'])
        dict_expand(self.create_or_update_payload, ['read_only'])
        dict_expand(self.create_or_update_payload, ['expose_sample_data'])
        dict_expand(self.create_or_update_payload, ['realtime_configuration'])
        dict_camelize(self.create_or_update_payload, ['diagnostics', 'level'], True)
        dict_expand(self.create_or_update_payload, ['diagnostics'])
        dict_expand(self.create_or_update_payload, ['storage_account'])
        dict_resource_id(self.create_or_update_payload, ['machine_learning_workspace', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_expand(self.create_or_update_payload, ['machine_learning_workspace'])
        dict_resource_id(self.create_or_update_payload, ['commitment_plan', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_expand(self.create_or_update_payload, ['commitment_plan'])
        dict_expand(self.create_or_update_payload, ['input'])
        dict_expand(self.create_or_update_payload, ['output'])
        dict_expand(self.create_or_update_payload, ['example_request'])
        dict_expand(self.create_or_update_payload, ['assets'])
        dict_expand(self.create_or_update_payload, ['parameters'])
        dict_expand(self.create_or_update_payload, ['payloads_in_blob_storage'])
        dict_expand(self.create_or_update_payload, ['payloads_location'])
        dict_expand(self.create_or_update_payload, ['package_type'])

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
                if (not default_compare(self.create_or_update_payload, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Web Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
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
            else:
                key = list(old[0])[0]
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


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


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
    AzureRMWebService()


if __name__ == '__main__':
    main()
