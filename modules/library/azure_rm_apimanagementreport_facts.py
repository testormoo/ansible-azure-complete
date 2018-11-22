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
module: azure_rm_apimanagementreport_facts
version_added: "2.8"
short_description: Get Azure Report facts.
description:
    - Get facts of Azure Report.

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
            - The filter to apply on the operation.
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    interval:
        description:
            - "By time interval. Interval must be multiple of 15 minutes and may not be zero. The value should be in ISO  8601 format
               (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string:
               XmlConvert.ToString(new TimeSpan(hours, minutes, secconds))"

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip
      interval: interval

  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: List instances of Report
    azure_rm_apimanagementreport_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip
'''

RETURN = '''
reports:
    description: A list of dictionaries containing facts for Report.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMReportFacts(AzureRMModuleBase):
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
            interval=dict(
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
        self.interval = None
        super(AzureRMReportFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.interval is not None:
            self.results['reports'] = self.list_by_time()
        elif self.filter is not None:
            self.results['reports'] = self.list_by_api()
        elif self.filter is not None:
            self.results['reports'] = self.list_by_user()
        elif self.filter is not None:
            self.results['reports'] = self.list_by_operation()
        elif self.filter is not None:
            self.results['reports'] = self.list_by_product()
        elif self.filter is not None:
            self.results['reports'] = self.list_by_request()
        else:
            self.results['reports'] = self.list_by_geo()
        else:
            self.results['reports'] = self.list_by_subscription()
        return self.results

    def list_by_time(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_time(resource_group_name=self.resource_group,
                                                             service_name=self.name,
                                                             interval=self.interval)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_api(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_api(resource_group_name=self.resource_group,
                                                            service_name=self.name,
                                                            filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_user(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_user(resource_group_name=self.resource_group,
                                                             service_name=self.name,
                                                             filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_operation(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_operation(resource_group_name=self.resource_group,
                                                                  service_name=self.name,
                                                                  filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_product(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_product(resource_group_name=self.resource_group,
                                                                service_name=self.name,
                                                                filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_geo(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_geo(resource_group_name=self.resource_group,
                                                            service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_subscription(resource_group_name=self.resource_group,
                                                                     service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_request(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.reports.list_by_request(resource_group_name=self.resource_group,
                                                                service_name=self.name,
                                                                filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMReportFacts()


if __name__ == '__main__':
    main()
