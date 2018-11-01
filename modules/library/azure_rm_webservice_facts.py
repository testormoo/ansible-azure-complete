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
module: azure_rm_webservice_facts
version_added: "2.8"
short_description: Get Azure Web Service facts.
description:
    - Get facts of Azure Web Service.

options:
    resource_group:
        description:
            - Name of the resource group in which the web service is located.
    web_service_name:
        description:
            - The name of the web service.
    region:
        description:
            - The region for which encrypted credential parameters are valid.
    skiptoken:
        description:
            - Continuation token for pagination.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Web Service
    azure_rm_webservice_facts:
      resource_group: resource_group_name
      web_service_name: web_service_name
      region: region

  - name: List instances of Web Service
    azure_rm_webservice_facts:
      resource_group: resource_group_name
      skiptoken: skiptoken

  - name: List instances of Web Service
    azure_rm_webservice_facts:
      skiptoken: skiptoken
'''

RETURN = '''
web_services:
    description: A list of dictionaries containing facts for Web Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Specifies the resource ID.
            returned: always
            type: str
            sample: TheWebServiceId
        location:
            description:
                - Specifies the location of the resource.
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Contains resource tags defined as key/value pairs.
            returned: always
            type: complex
            sample: "{\n  'tag1': 'value1',\n  'tag2': 'value2'\n}"
        properties:
            description:
                - Contains the property payload that describes the web service.
            returned: always
            type: complex
            sample: properties
            contains:
                title:
                    description:
                        - The title of the web service.
                    returned: always
                    type: str
                    sample: Web Service Title
                description:
                    description:
                        - The description of the web service.
                    returned: always
                    type: str
                    sample: Web Service Description
                diagnostics:
                    description:
                        - Settings controlling the diagnostics traces collection for the web service.
                    returned: always
                    type: complex
                    sample: diagnostics
                    contains:
                        level:
                            description:
                                - "Specifies the verbosity of the diagnostic output. Valid values are: None - disables tracing; Error - collects only error
                                   (stderr) traces; All - collects all traces (stdout and stderr). Possible values include: 'None', 'Error', 'All'"
                            returned: always
                            type: str
                            sample: None
                input:
                    description:
                        - "Contains the Swagger 2.0 schema describing one or more of the web service's inputs. For more information, see the Swagger
                           specification."
                    returned: always
                    type: complex
                    sample: input
                    contains:
                        title:
                            description:
                                - The title of your Swagger schema.
                            returned: always
                            type: str
                            sample: title
                        description:
                            description:
                                - The description of the Swagger schema.
                            returned: always
                            type: str
                            sample: description
                        type:
                            description:
                                - "The type of the entity described in swagger. Always 'object'."
                            returned: always
                            type: str
                            sample: object
                        properties:
                            description:
                                - "Specifies a collection that contains the column schema for each input or output of the web service. For more information,
                                   see the Swagger specification."
                            returned: always
                            type: complex
                            sample: "{\n  'input1': {\n    'title': '',\n    'description': '',\n    'type': 'object',\n    'properties': {\n
                                     'column_name': {\n        'type': 'String',\n        'x-ms-isnullable': false\n      }\n    }\n  }\n}"
                output:
                    description:
                        - "Contains the Swagger 2.0 schema describing one or more of the web service's outputs. For more information, see the Swagger
                           specification."
                    returned: always
                    type: complex
                    sample: output
                    contains:
                        title:
                            description:
                                - The title of your Swagger schema.
                            returned: always
                            type: str
                            sample: title
                        description:
                            description:
                                - The description of the Swagger schema.
                            returned: always
                            type: str
                            sample: description
                        type:
                            description:
                                - "The type of the entity described in swagger. Always 'object'."
                            returned: always
                            type: str
                            sample: object
                        properties:
                            description:
                                - "Specifies a collection that contains the column schema for each input or output of the web service. For more information,
                                   see the Swagger specification."
                            returned: always
                            type: complex
                            sample: "{\n  'output1': {\n    'title': '',\n    'description': '',\n    'type': 'object',\n    'properties': {\n      'age':
                                     {\n        'type': 'Integer',\n        'format': 'Int32',\n        'x-ms-isnullable': true\n      },\n
                                     'workclass': {\n        'type': 'String',\n        'x-ms-isnullable': false\n      }\n    }\n  }\n}"
                assets:
                    description:
                        - Contains user defined properties describing web service assets. Properties are expressed as Key/Value pairs.
                    returned: always
                    type: complex
                    sample: "{\n  'asset1': {\n    'name': 'Execute R Script',\n    'type': 'Module',\n    'locationInfo': {\n      'uri':
                             'aml://module/moduleId-1',\n      'credentials': ''\n    }\n  },\n  'asset2': {\n    'name': 'Import Data',\n    'type':
                             'Module',\n    'locationInfo': {\n      'uri': 'aml://module/moduleId-2',\n      'credentials': ''\n    }\n  }\n}"
                parameters:
                    description:
                        - "The set of global parameters values defined for the web service, given as a global parameter name to default value map. If no
                           default value is specified, the parameter is considered to be required."
                    returned: always
                    type: complex
                    sample: {}
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.webservices import AzureMLWebServicesManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWebServicesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            web_service_name=dict(
                type='str'
            ),
            region=dict(
                type='str'
            ),
            skiptoken=dict(
                type='str'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.web_service_name = None
        self.region = None
        self.skiptoken = None
        self.tags = None
        super(AzureRMWebServicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMLWebServicesManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.web_service_name is not None):
            self.results['web_services'] = self.get()
        elif self.resource_group is not None:
            self.results['web_services'] = self.list_by_resource_group()
        else:
            self.results['web_services'] = self.list_by_subscription_id()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.web_services.get(resource_group_name=self.resource_group,
                                                         web_service_name=self.web_service_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WebServices.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.web_services.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WebServices.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription_id(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.web_services.list_by_subscription_id()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WebServices.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'properties': {
                'title': d.get('properties', {}).get('title', None),
                'description': d.get('properties', {}).get('description', None),
                'diagnostics': {
                    'level': d.get('properties', {}).get('diagnostics', {}).get('level', None)
                },
                'input': {
                    'title': d.get('properties', {}).get('input', {}).get('title', None),
                    'description': d.get('properties', {}).get('input', {}).get('description', None),
                    'type': d.get('properties', {}).get('input', {}).get('type', None),
                    'properties': d.get('properties', {}).get('input', {}).get('properties', None)
                },
                'output': {
                    'title': d.get('properties', {}).get('output', {}).get('title', None),
                    'description': d.get('properties', {}).get('output', {}).get('description', None),
                    'type': d.get('properties', {}).get('output', {}).get('type', None),
                    'properties': d.get('properties', {}).get('output', {}).get('properties', None)
                },
                'assets': d.get('properties', {}).get('assets', None),
                'parameters': d.get('properties', {}).get('parameters', None)
            }
        }
        return d


def main():
    AzureRMWebServicesFacts()


if __name__ == '__main__':
    main()
