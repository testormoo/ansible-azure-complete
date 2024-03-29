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
module: azure_rm_schedulerjobcollection
version_added: "2.8"
short_description: Manage Azure Job Collection instance.
description:
    - Create, update and delete instance of Azure Job Collection.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    name:
        description:
            - The job collection name.
        required: True
    name:
        description:
            - Gets or sets the job collection resource name.
    location:
        description:
            - Gets or sets the storage account location.
    sku:
        description:
            - Gets or sets the SKU.
        suboptions:
            name:
                description:
                    - Gets or set the SKU.
                choices:
                    - 'standard'
                    - 'free'
                    - 'p10_premium'
                    - 'p20_premium'
    state:
        description:
            - Gets or sets the state.
        choices:
            - 'enabled'
            - 'disabled'
            - 'suspended'
            - 'deleted'
    quota:
        description:
            - Gets or sets the job collection quota.
        suboptions:
            max_job_count:
                description:
                    - Gets or set the maximum job count.
            max_job_occurrence:
                description:
                    - Gets or sets the maximum job occurrence.
            max_recurrence:
                description:
                    - Gets or set the maximum recurrence.
                suboptions:
                    frequency:
                        description:
                            - Gets or sets the frequency of recurrence (second, C(minute), C(hour), C(day), C(week), C(month)).
                        choices:
                            - 'minute'
                            - 'hour'
                            - 'day'
                            - 'week'
                            - 'month'
                    interval:
                        description:
                            - Gets or sets the interval between retries.
    state:
      description:
        - Assert the state of the Job Collection.
        - Use 'present' to create or update an Job Collection and 'absent' to delete it.
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
  - name: Create (or update) Job Collection
    azure_rm_schedulerjobcollection:
      resource_group: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Gets the job collection resource identifier.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.scheduler import SchedulerManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMJobCollection(AzureRMModuleBase):
    """Configuration class for an Azure RM Job Collection resource"""

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
            name=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['standard',
                                 'free',
                                 'p10_premium',
                                 'p20_premium']
                    )
                )
            ),
            state=dict(
                type='str',
                choices=['enabled',
                         'disabled',
                         'suspended',
                         'deleted']
            ),
            quota=dict(
                type='dict',
                options=dict(
                    max_job_count=dict(
                        type='int'
                    ),
                    max_job_occurrence=dict(
                        type='int'
                    ),
                    max_recurrence=dict(
                        type='dict',
                        options=dict(
                            frequency=dict(
                                type='str',
                                choices=['minute',
                                         'hour',
                                         'day',
                                         'week',
                                         'month']
                            ),
                            interval=dict(
                                type='int'
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.job_collection = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobCollection, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.job_collection[key] = kwargs[key]

        dict_camelize(self.job_collection, ['sku', 'name'], True)
        dict_expand(self.job_collection, ['sku'])
        dict_expand(self.job_collection, ['state'])
        dict_camelize(self.job_collection, ['state'], True)
        dict_camelize(self.job_collection, ['quota', 'max_recurrence', 'frequency'], True)
        dict_expand(self.job_collection, ['quota'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SchedulerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_jobcollection()

        if not old_response:
            self.log("Job Collection instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job Collection instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.job_collection, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Collection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobcollection()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job Collection instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_jobcollection()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Job Collection instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_jobcollection(self):
        '''
        Creates or updates Job Collection with the specified configuration.

        :return: deserialized Job Collection instance state dictionary
        '''
        self.log("Creating / Updating the Job Collection instance {0}".format(self.name))

        try:
            response = self.mgmt_client.job_collections.create_or_update(resource_group_name=self.resource_group,
                                                                         job_collection_name=self.name,
                                                                         job_collection=self.job_collection)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job Collection instance.')
            self.fail("Error creating the Job Collection instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_jobcollection(self):
        '''
        Deletes specified Job Collection instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job Collection instance {0}".format(self.name))
        try:
            response = self.mgmt_client.job_collections.delete(resource_group_name=self.resource_group,
                                                               job_collection_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Job Collection instance.')
            self.fail("Error deleting the Job Collection instance: {0}".format(str(e)))

        return True

    def get_jobcollection(self):
        '''
        Gets the properties of the specified Job Collection.

        :return: deserialized Job Collection instance state dictionary
        '''
        self.log("Checking if the Job Collection instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.job_collections.get(resource_group_name=self.resource_group,
                                                            job_collection_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Collection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Collection instance.')
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


def main():
    """Main execution"""
    AzureRMJobCollection()


if __name__ == '__main__':
    main()
