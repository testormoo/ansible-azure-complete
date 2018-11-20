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
module: azure_rm_webdomain
version_added: "2.8"
short_description: Manage Domain instance.
description:
    - Create, update and delete instance of Domain.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Name of the I(domain).
        required: True
    domain:
        description:
            - Domain registration information.
        required: True
        suboptions:
            kind:
                description:
                    - Kind of resource.
            location:
                description:
                    - Resource Location.
                    - Required when C(state) is I(present).
            contact_admin:
                description:
                    - Administrative contact.
                suboptions:
                    address_mailing:
                        description:
                            - Mailing address.
                        suboptions:
                            address1:
                                description:
                                    - First line of an Address.
                                    - Required when C(state) is I(present).
                            address2:
                                description:
                                    - The second line of the Address. Optional.
                            city:
                                description:
                                    - The city for the address.
                                    - Required when C(state) is I(present).
                            country:
                                description:
                                    - The country for the address.
                                    - Required when C(state) is I(present).
                            postal_code:
                                description:
                                    - The postal code for the address.
                                    - Required when C(state) is I(present).
                            state:
                                description:
                                    - The state or province for the address.
                                    - Required when C(state) is I(present).
                    email:
                        description:
                            - Email address.
                            - Required when C(state) is I(present).
                    fax:
                        description:
                            - Fax number.
                    job_title:
                        description:
                            - Job title.
                    name_first:
                        description:
                            - First name.
                            - Required when C(state) is I(present).
                    name_last:
                        description:
                            - Last name.
                            - Required when C(state) is I(present).
                    name_middle:
                        description:
                            - Middle name.
                    organization:
                        description:
                            - Organization contact belongs to.
                    phone:
                        description:
                            - Phone number.
                            - Required when C(state) is I(present).
            contact_billing:
                description:
                    - Billing contact.
                suboptions:
                    address_mailing:
                        description:
                            - Mailing address.
                        suboptions:
                            address1:
                                description:
                                    - First line of an Address.
                                    - Required when C(state) is I(present).
                            address2:
                                description:
                                    - The second line of the Address. Optional.
                            city:
                                description:
                                    - The city for the address.
                                    - Required when C(state) is I(present).
                            country:
                                description:
                                    - The country for the address.
                                    - Required when C(state) is I(present).
                            postal_code:
                                description:
                                    - The postal code for the address.
                                    - Required when C(state) is I(present).
                            state:
                                description:
                                    - The state or province for the address.
                                    - Required when C(state) is I(present).
                    email:
                        description:
                            - Email address.
                            - Required when C(state) is I(present).
                    fax:
                        description:
                            - Fax number.
                    job_title:
                        description:
                            - Job title.
                    name_first:
                        description:
                            - First name.
                            - Required when C(state) is I(present).
                    name_last:
                        description:
                            - Last name.
                            - Required when C(state) is I(present).
                    name_middle:
                        description:
                            - Middle name.
                    organization:
                        description:
                            - Organization contact belongs to.
                    phone:
                        description:
                            - Phone number.
                            - Required when C(state) is I(present).
            contact_registrant:
                description:
                    - Registrant contact.
                suboptions:
                    address_mailing:
                        description:
                            - Mailing address.
                        suboptions:
                            address1:
                                description:
                                    - First line of an Address.
                                    - Required when C(state) is I(present).
                            address2:
                                description:
                                    - The second line of the Address. Optional.
                            city:
                                description:
                                    - The city for the address.
                                    - Required when C(state) is I(present).
                            country:
                                description:
                                    - The country for the address.
                                    - Required when C(state) is I(present).
                            postal_code:
                                description:
                                    - The postal code for the address.
                                    - Required when C(state) is I(present).
                            state:
                                description:
                                    - The state or province for the address.
                                    - Required when C(state) is I(present).
                    email:
                        description:
                            - Email address.
                            - Required when C(state) is I(present).
                    fax:
                        description:
                            - Fax number.
                    job_title:
                        description:
                            - Job title.
                    name_first:
                        description:
                            - First name.
                            - Required when C(state) is I(present).
                    name_last:
                        description:
                            - Last name.
                            - Required when C(state) is I(present).
                    name_middle:
                        description:
                            - Middle name.
                    organization:
                        description:
                            - Organization contact belongs to.
                    phone:
                        description:
                            - Phone number.
                            - Required when C(state) is I(present).
            contact_tech:
                description:
                    - Technical contact.
                suboptions:
                    address_mailing:
                        description:
                            - Mailing address.
                        suboptions:
                            address1:
                                description:
                                    - First line of an Address.
                                    - Required when C(state) is I(present).
                            address2:
                                description:
                                    - The second line of the Address. Optional.
                            city:
                                description:
                                    - The city for the address.
                                    - Required when C(state) is I(present).
                            country:
                                description:
                                    - The country for the address.
                                    - Required when C(state) is I(present).
                            postal_code:
                                description:
                                    - The postal code for the address.
                                    - Required when C(state) is I(present).
                            state:
                                description:
                                    - The state or province for the address.
                                    - Required when C(state) is I(present).
                    email:
                        description:
                            - Email address.
                            - Required when C(state) is I(present).
                    fax:
                        description:
                            - Fax number.
                    job_title:
                        description:
                            - Job title.
                    name_first:
                        description:
                            - First name.
                            - Required when C(state) is I(present).
                    name_last:
                        description:
                            - Last name.
                            - Required when C(state) is I(present).
                    name_middle:
                        description:
                            - Middle name.
                    organization:
                        description:
                            - Organization contact belongs to.
                    phone:
                        description:
                            - Phone number.
                            - Required when C(state) is I(present).
            privacy:
                description:
                    - <code>true</code> if domain privacy is enabled for this domain; otherwise, <code>false</code>.
            auto_renew:
                description:
                    - <code>true</code> if the domain should be automatically renewed; otherwise, <code>false</code>.
            consent:
                description:
                    - Legal agreement consent.
                suboptions:
                    agreement_keys:
                        description:
                            - "List of applicable legal agreement keys. This list can be retrieved using ListLegalAgreements API under
                               <code>TopLevelDomain</code> resource."
                        type: list
                    agreed_by:
                        description:
                            - Client IP address.
                    agreed_at:
                        description:
                            - Timestamp when the agreements were accepted.
            dns_type:
                description:
                    - Current DNS type.
                choices:
                    - 'azure_dns'
                    - 'default_domain_registrar_dns'
            dns_zone_id:
                description:
                    - Azure DNS Zone to use
            target_dns_type:
                description:
                    - Target DNS type (would be used for migration).
                choices:
                    - 'azure_dns'
                    - 'default_domain_registrar_dns'
            auth_code:
                description:
    state:
      description:
        - Assert the state of the Domain.
        - Use 'present' to create or update an Domain and 'absent' to delete it.
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
  - name: Create (or update) Domain
    azure_rm_webdomain:
      resource_group: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.web import WebSiteManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDomains(AzureRMModuleBase):
    """Configuration class for an Azure RM Domain resource"""

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
            domain=dict(
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
        self.domain = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDomains, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "kind":
                    self.domain["kind"] = kwargs[key]
                elif key == "location":
                    self.domain["location"] = kwargs[key]
                elif key == "contact_admin":
                    self.domain["contact_admin"] = kwargs[key]
                elif key == "contact_billing":
                    self.domain["contact_billing"] = kwargs[key]
                elif key == "contact_registrant":
                    self.domain["contact_registrant"] = kwargs[key]
                elif key == "contact_tech":
                    self.domain["contact_tech"] = kwargs[key]
                elif key == "privacy":
                    self.domain["privacy"] = kwargs[key]
                elif key == "auto_renew":
                    self.domain["auto_renew"] = kwargs[key]
                elif key == "consent":
                    self.domain["consent"] = kwargs[key]
                elif key == "dns_type":
                    self.domain["dns_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "dns_zone_id":
                    self.domain["dns_zone_id"] = kwargs[key]
                elif key == "target_dns_type":
                    self.domain["target_dns_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "auth_code":
                    self.domain["auth_code"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(WebSiteManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_domain()

        if not old_response:
            self.log("Domain instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Domain instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Domain instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_domain()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Domain instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_domain()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_domain():
                time.sleep(20)
        else:
            self.log("Domain instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_domain(self):
        '''
        Creates or updates Domain with the specified configuration.

        :return: deserialized Domain instance state dictionary
        '''
        self.log("Creating / Updating the Domain instance {0}".format(self.name))

        try:
            response = self.mgmt_client.domains.create_or_update(resource_group_name=self.resource_group,
                                                                 domain_name=self.name,
                                                                 domain=self.domain)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Domain instance.')
            self.fail("Error creating the Domain instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_domain(self):
        '''
        Deletes specified Domain instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Domain instance {0}".format(self.name))
        try:
            response = self.mgmt_client.domains.delete(resource_group_name=self.resource_group,
                                                       domain_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Domain instance.')
            self.fail("Error deleting the Domain instance: {0}".format(str(e)))

        return True

    def get_domain(self):
        '''
        Gets the properties of the specified Domain.

        :return: deserialized Domain instance state dictionary
        '''
        self.log("Checking if the Domain instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.domains.get(resource_group_name=self.resource_group,
                                                    domain_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Domain instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Domain instance.')
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMDomains()


if __name__ == '__main__':
    main()
