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
module: azure_rm_apimanagementlogger_facts
version_added: "2.8"
short_description: Get Azure Logger facts.
description:
    - Get facts of Azure Logger.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    filter:
        description:
            - | Field | Supported operators    | Supported functions                         |
            - |-------|------------------------|---------------------------------------------|
            - | id    | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | type  | eq                     |                                             |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    loggerid:
        description:
            - Logger identifier. Must be unique in the API Management service instance.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Logger
    azure_rm_apimanagementlogger_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Logger
    azure_rm_apimanagementlogger_facts:
      resource_group: resource_group_name
      name: service_name
      loggerid: loggerid
'''

RETURN = '''
logger:
    description: A list of dictionaries containing facts for Logger.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/loggers/kloudapilogger1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: kloudapilogger1
        description:
            description:
                - Logger description.
            returned: always
            type: str
            sample: testeventhub3again
        credentials:
            description:
                - "The name and SendRule connection string of the event hub for azureEventHub logger.\nInstrumentation key for applicationInsights logger."
            returned: always
            type: complex
            sample: "{\n  'name': 'testeventhub4',\n  'connectionString':
                     'Endpoint=sb://eventhubapim.servicebus.windows.net/;SharedAccessKeyName=Sender;SharedAccessKey=************'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLoggerFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            ),
            loggerid=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.filter = None
        self.top = None
        self.skip = None
        self.loggerid = None
        super(AzureRMLoggerFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['logger'] = self.list_by_service()
        elif self.loggerid is not None:
            self.results['logger'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.logger.list_by_service(resource_group_name=self.resource_group,
                                                               service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Logger.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.logger.get(resource_group_name=self.resource_group,
                                                   service_name=self.name,
                                                   loggerid=self.loggerid)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Logger.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None),
            'credentials': d.get('credentials', None)
        }
        return d


def main():
    AzureRMLoggerFacts()


if __name__ == '__main__':
    main()
