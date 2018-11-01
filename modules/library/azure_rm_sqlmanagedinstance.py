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
module: azure_rm_sqlmanagedinstance
version_added: "2.8"
short_description: Manage Managed Instance instance.
description:
    - Create, update and delete instance of Managed Instance.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    managed_instance_name:
        description:
            - The name of the managed instance.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    identity:
        description:
            - The Azure Active Directory identity of the managed instance.
        suboptions:
            type:
                description:
                    - "The identity type. Set this to 'C(system_assigned)' in order to automatically create and assign an Azure Active Directory principal
                       for the resource."
                choices:
                    - 'system_assigned'
    sku:
        description:
            - Managed instance sku
        suboptions:
            name:
                description:
                    - The name of the SKU. Ex - P3. It is typically a letter+number code
                required: True
            tier:
                description:
                    - This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
            size:
                description:
                    - The SKU size. When the name field is the combination of I(tier) and some other value, this would be the standalone code.
            family:
                description:
                    - If the service has different generations of hardware, for the same SKU, then that can be captured here.
            capacity:
                description:
                    - "If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource this
                       may be omitted."
    administrator_login:
        description:
            - Administrator username for the managed instance. Can only be specified when the managed instance is being created (and is required for creation).
    administrator_login_password:
        description:
            - The administrator login password (required for managed instance creation).
    subnet_id:
        description:
            - Subnet resource ID for the managed instance.
    license_type:
        description:
            - "The license type. Possible values are 'LicenseIncluded' and 'BasePrice'."
    v_cores:
        description:
            - The number of VCores.
    storage_size_in_gb:
        description:
            - The maximum storage size in GB.
    dns_zone_partner:
        description:
            - The resource id of another managed instance whose DNS zone this managed instance will share after creation.
    state:
      description:
        - Assert the state of the Managed Instance.
        - Use 'present' to create or update an Managed Instance and 'absent' to delete it.
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
  - name: Create (or update) Managed Instance
    azure_rm_sqlmanagedinstance:
      resource_group: testrg
      managed_instance_name: testinstance
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/20D7082A-0FC7-4468-82BD-542694D5042B/resourceGroups/testrg/providers/Microsoft.Sql/managedInstances/testinstance
fully_qualified_domain_name:
    description:
        - The fully qualified domain name of the managed instance.
    returned: always
    type: str
    sample: fully_qualified_domain_name
state:
    description:
        - The state of the managed instance.
    returned: always
    type: str
    sample: Ready
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagedInstances(AzureRMModuleBase):
    """Configuration class for an Azure RM Managed Instance resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            managed_instance_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            identity=dict(
                type='dict'
            ),
            sku=dict(
                type='dict'
            ),
            administrator_login=dict(
                type='str'
            ),
            administrator_login_password=dict(
                type='str',
                no_log=True
            ),
            subnet_id=dict(
                type='str'
            ),
            license_type=dict(
                type='str'
            ),
            v_cores=dict(
                type='int'
            ),
            storage_size_in_gb=dict(
                type='int'
            ),
            dns_zone_partner=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.managed_instance_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagedInstances, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "identity":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'system_assigned':
                            ev['type'] = 'SystemAssigned'
                    self.parameters["identity"] = ev
                elif key == "sku":
                    self.parameters["sku"] = kwargs[key]
                elif key == "administrator_login":
                    self.parameters["administrator_login"] = kwargs[key]
                elif key == "administrator_login_password":
                    self.parameters["administrator_login_password"] = kwargs[key]
                elif key == "subnet_id":
                    self.parameters["subnet_id"] = kwargs[key]
                elif key == "license_type":
                    self.parameters["license_type"] = kwargs[key]
                elif key == "v_cores":
                    self.parameters["v_cores"] = kwargs[key]
                elif key == "storage_size_in_gb":
                    self.parameters["storage_size_in_gb"] = kwargs[key]
                elif key == "dns_zone_partner":
                    self.parameters["dns_zone_partner"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_managedinstance()

        if not old_response:
            self.log("Managed Instance instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Managed Instance instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Managed Instance instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Managed Instance instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managedinstance()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Managed Instance instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managedinstance()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_managedinstance():
                time.sleep(20)
        else:
            self.log("Managed Instance instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_managedinstance(self):
        '''
        Creates or updates Managed Instance with the specified configuration.

        :return: deserialized Managed Instance instance state dictionary
        '''
        self.log("Creating / Updating the Managed Instance instance {0}".format(self.managed_instance_name))

        try:
            response = self.mgmt_client.managed_instances.create_or_update(resource_group_name=self.resource_group,
                                                                           managed_instance_name=self.managed_instance_name,
                                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Managed Instance instance.')
            self.fail("Error creating the Managed Instance instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_managedinstance(self):
        '''
        Deletes specified Managed Instance instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Managed Instance instance {0}".format(self.managed_instance_name))
        try:
            response = self.mgmt_client.managed_instances.delete(resource_group_name=self.resource_group,
                                                                 managed_instance_name=self.managed_instance_name)
        except CloudError as e:
            self.log('Error attempting to delete the Managed Instance instance.')
            self.fail("Error deleting the Managed Instance instance: {0}".format(str(e)))

        return True

    def get_managedinstance(self):
        '''
        Gets the properties of the specified Managed Instance.

        :return: deserialized Managed Instance instance state dictionary
        '''
        self.log("Checking if the Managed Instance instance {0} is present".format(self.managed_instance_name))
        found = False
        try:
            response = self.mgmt_client.managed_instances.get(resource_group_name=self.resource_group,
                                                              managed_instance_name=self.managed_instance_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Managed Instance instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Managed Instance instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'fully_qualified_domain_name': d.get('fully_qualified_domain_name', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMManagedInstances()


if __name__ == '__main__':
    main()