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
module: azure_rm_databoxjob
version_added: "2.8"
short_description: Manage Azure Job instance.
description:
    - Create, update and delete instance of Azure Job.

options:
    resource_group:
        description:
            - The Resource Group Name
        required: True
    name:
        description:
            - "The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any
               alphanumeric and underscore only"
        required: True
    location:
        description:
            - "The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.).
               The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed."
            - Required when C(state) is I(present).
    sku:
        description:
            - The sku type.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - The sku name.
                    - Required when C(state) is I(present).
                choices:
                    - 'data_box'
                    - 'data_box_disk'
                    - 'data_box_heavy'
            display_name:
                description:
                    - The display name of the sku.
            family:
                description:
                    - The sku family.
    details:
        description:
            - Details of a job run. This field will only be sent for expand details filter.
        suboptions:
            expected_data_size_in_tera_bytes:
                description:
                    - The expected size of the data, which needs to be transfered in this job, in tera bytes.
            contact_details:
                description:
                    - Contact details for notification and shipping.
                    - Required when C(state) is I(present).
                suboptions:
                    contact_name:
                        description:
                            - Contact name of the person.
                            - Required when C(state) is I(present).
                    phone:
                        description:
                            - Phone number of the contact person.
                            - Required when C(state) is I(present).
                    phone_extension:
                        description:
                            - I(phone) extension number of the contact person.
                    mobile:
                        description:
                            - Mobile number of the contact person.
                    email_list:
                        description:
                            - List of Email-ids to be notified about job progress.
                            - Required when C(state) is I(present).
                        type: list
                    notification_preference:
                        description:
                            - Notification preference for a job stage.
                        type: list
                        suboptions:
                            stage_name:
                                description:
                                    - Name of the stage.
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'device_prepared'
                                    - 'dispatched'
                                    - 'delivered'
                                    - 'picked_up'
                                    - 'at_azure_dc'
                                    - 'data_copy'
                            send_notification:
                                description:
                                    - Notification is required or not.
                                    - Required when C(state) is I(present).
            shipping_address:
                description:
                    - Shipping address of the customer.
                    - Required when C(state) is I(present).
                suboptions:
                    street_address1:
                        description:
                            - Street Address line 1.
                            - Required when C(state) is I(present).
                    street_address2:
                        description:
                            - Street Address line 2.
                    street_address3:
                        description:
                            - Street Address line 3.
                    city:
                        description:
                            - Name of the City.
                    state_or_province:
                        description:
                            - Name of the State or Province.
                    country:
                        description:
                            - Name of the Country.
                            - Required when C(state) is I(present).
                    postal_code:
                        description:
                            - Postal code.
                            - Required when C(state) is I(present).
                    zip_extended_code:
                        description:
                            - Extended Zip Code.
                    company_name:
                        description:
                            - Name of the company.
                    address_type:
                        description:
                            - Type of address.
                        choices:
                            - 'none'
                            - 'residential'
                            - 'commercial'
            destination_account_details:
                description:
                    - Destination account details.
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    account_id:
                        description:
                            - Destination storage account id.
                            - Required when C(state) is I(present).
            preferences:
                description:
                    - Preferences for the order.
                suboptions:
                    preferred_data_center_region:
                        description:
                        type: list
            job_details_type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Job.
        - Use 'present' to create or update an Job and 'absent' to delete it.
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
  - name: Create (or update) Job
    azure_rm_databoxjob:
      resource_group: SdkRg8120
      name: SdkJob7196
      location: westus
      sku:
        name: DataBox
      details:
        contact_details:
          contact_name: Public SDK Test
          phone: 1234567890
          phone_extension: 1234
          email_list:
            - [
  "testing@microsoft.com"
]
        shipping_address:
          street_address1: 16 TOWNSEND ST
          street_address2: Unit 1
          city: San Francisco
          state_or_province: CA
          country: US
          postal_code: 94107
          company_name: Microsoft
          address_type: Commercial
        destination_account_details:
          - account_id: /subscriptions/fa68082f-8ff7-4a25-95c7-ce9da541242f/resourcegroups/databoxbvt/providers/Microsoft.Storage/storageAccounts/databoxbvttestaccount
'''

RETURN = '''
status:
    description:
        - "Name of the stage which is in progress. Possible values include: 'DeviceOrdered', 'DevicePrepared', 'Dispatched', 'Delivered', 'PickedUp',
           'AtAzureDC', 'DataCopy', 'Completed', 'CompletedWithErrors', 'Cancelled', 'Failed_IssueReportedAtCustomer', 'Failed_IssueDetectedAtAzureDC',
           'Aborted'"
    returned: always
    type: str
    sample: DeviceOrdered
id:
    description:
        - Id of the object.
    returned: always
    type: str
    sample: /subscriptions/fa68082f-8ff7-4a25-95c7-ce9da541242f/resourceGroups/SdkRg8120/providers/Microsoft.DataBox/jobs/SdkJob7196
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.databox import DataBoxManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMJob(AzureRMModuleBase):
    """Configuration class for an Azure RM Job resource"""

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
            sku=dict(
                type='dict'
            ),
            details=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.job_resource = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJob, self).__init__(derived_arg_spec=self.module_arg_spec,
                                         supports_check_mode=True,
                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.job_resource[key] = kwargs[key]

        dict_camelize(self.job_resource, ['sku', 'name'], True)
        dict_camelize(self.job_resource, ['details', 'contact_details', 'notification_preference', 'stage_name'], True)
        dict_map(self.job_resource, ['details', 'contact_details', 'notification_preference', 'stage_name'], {'at_azure_dc': 'AtAzureDC'})
        dict_camelize(self.job_resource, ['details', 'shipping_address', 'address_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataBoxManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_job()

        if not old_response:
            self.log("Job instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.job_resource, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_job()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_job()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_job():
                time.sleep(20)
        else:
            self.log("Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_job(self):
        '''
        Creates or updates Job with the specified configuration.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Creating / Updating the Job instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.jobs.create(resource_group_name=self.resource_group,
                                                        job_name=self.name,
                                                        job_resource=self.job_resource)
            else:
                response = self.mgmt_client.jobs.update(resource_group_name=self.resource_group,
                                                        job_name=self.name,
                                                        job_resource_update_parameter=self.job_resource_update_parameter)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job instance.')
            self.fail("Error creating the Job instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_job(self):
        '''
        Deletes specified Job instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job instance {0}".format(self.name))
        try:
            response = self.mgmt_client.jobs.delete(resource_group_name=self.resource_group,
                                                    job_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Job instance.')
            self.fail("Error deleting the Job instance: {0}".format(str(e)))

        return True

    def get_job(self):
        '''
        Gets the properties of the specified Job.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Checking if the Job instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.jobs.get(resource_group_name=self.resource_group,
                                                 job_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'status': d.get('status', None),
            'id': d.get('id', None)
        }
        return d


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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMJob()


if __name__ == '__main__':
    main()
