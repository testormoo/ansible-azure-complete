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
module: azure_rm_notificationhub
version_added: "2.8"
short_description: Manage Notification Hub instance.
description:
    - Create, update and delete instance of Notification Hub.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    namespace_name:
        description:
            - The namespace name.
        required: True
    notification_hub_name:
        description:
            - The notification hub name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The sku of the created namespace
        suboptions:
            name:
                description:
                    - Name of the notification hub sku.
                required: True
                choices:
                    - 'free'
                    - 'basic'
                    - 'standard'
            tier:
                description:
                    - The tier of particular sku
            size:
                description:
                    - The Sku size
            family:
                description:
                    - The Sku Family
            capacity:
                description:
                    - The capacity of the resource
    notification_hub_create_or_update_parameters_name:
        description:
            - The NotificationHub name.
    registration_ttl:
        description:
            - The RegistrationTtl of the created NotificationHub
    authorization_rules:
        description:
            - The AuthorizationRules of the created NotificationHub
        type: list
        suboptions:
            rights:
                description:
                    - The rights associated with the rule.
                type: list
    apns_credential:
        description:
            - The ApnsCredential of the created NotificationHub
        suboptions:
            apns_certificate:
                description:
                    - The APNS certificate.
            certificate_key:
                description:
                    - The certificate key.
            endpoint:
                description:
                    - The endpoint of this credential.
            thumbprint:
                description:
                    - The Apns certificate Thumbprint
            key_id:
                description:
                    - A 10-character key identifier (kid) key, obtained from your developer account
            app_name:
                description:
                    - The name of the application
            app_id:
                description:
                    - The issuer (iss) registered claim key, whose value is your 10-character Team ID, obtained from your developer account
            token:
                description:
                    - Provider Authentication Token, obtained through your developer account
    wns_credential:
        description:
            - The WnsCredential of the created NotificationHub
        suboptions:
            package_sid:
                description:
                    - The package ID for this credential.
            secret_key:
                description:
                    - The secret key.
            windows_live_endpoint:
                description:
                    - The Windows Live endpoint.
    gcm_credential:
        description:
            - The GcmCredential of the created NotificationHub
        suboptions:
            gcm_endpoint:
                description:
                    - The GCM endpoint.
            google_api_key:
                description:
                    - The Google API key.
    mpns_credential:
        description:
            - The MpnsCredential of the created NotificationHub
        suboptions:
            mpns_certificate:
                description:
                    - The MPNS certificate.
            certificate_key:
                description:
                    - The certificate key for this credential.
            thumbprint:
                description:
                    - The Mpns certificate Thumbprint
    adm_credential:
        description:
            - The AdmCredential of the created NotificationHub
        suboptions:
            client_id:
                description:
                    - The client identifier.
            client_secret:
                description:
                    - The credential secret access key.
            auth_token_url:
                description:
                    - The URL of the authorization token.
    baidu_credential:
        description:
            - The BaiduCredential of the created NotificationHub
        suboptions:
            baidu_api_key:
                description:
                    - Baidu Api Key.
            baidu_end_point:
                description:
                    - Baidu Endpoint.
            baidu_secret_key:
                description:
                    - Baidu Secret Key
    state:
      description:
        - Assert the state of the Notification Hub.
        - Use 'present' to create or update an Notification Hub and 'absent' to delete it.
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
  - name: Create (or update) Notification Hub
    azure_rm_notificationhub:
      resource_group: 5ktrial
      namespace_name: nh-sdk-ns
      notification_hub_name: nh-sdk-hub
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/29cfa613-cbbc-4512-b1d6-1b3a92c7fa40/resourceGroups/sdkresourceGroup/providers/Microsoft.NotificationHubs/namespaces/nh-sdk-ns/no
            tificationHubs/nh-sdk-hub"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.notificationhubs import NotificationHubsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMNotificationHubs(AzureRMModuleBase):
    """Configuration class for an Azure RM Notification Hub resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            namespace_name=dict(
                type='str',
                required=True
            ),
            notification_hub_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            notification_hub_create_or_update_parameters_name=dict(
                type='str'
            ),
            registration_ttl=dict(
                type='str'
            ),
            authorization_rules=dict(
                type='list'
            ),
            apns_credential=dict(
                type='dict'
            ),
            wns_credential=dict(
                type='dict'
            ),
            gcm_credential=dict(
                type='dict'
            ),
            mpns_credential=dict(
                type='dict'
            ),
            adm_credential=dict(
                type='dict'
            ),
            baidu_credential=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.namespace_name = None
        self.notification_hub_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMNotificationHubs, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'free':
                            ev['name'] = 'Free'
                        elif ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                    self.parameters["sku"] = ev
                elif key == "notification_hub_create_or_update_parameters_name":
                    self.parameters["notification_hub_create_or_update_parameters_name"] = kwargs[key]
                elif key == "registration_ttl":
                    self.parameters["registration_ttl"] = kwargs[key]
                elif key == "authorization_rules":
                    self.parameters["authorization_rules"] = kwargs[key]
                elif key == "apns_credential":
                    self.parameters["apns_credential"] = kwargs[key]
                elif key == "wns_credential":
                    self.parameters["wns_credential"] = kwargs[key]
                elif key == "gcm_credential":
                    self.parameters["gcm_credential"] = kwargs[key]
                elif key == "mpns_credential":
                    self.parameters["mpns_credential"] = kwargs[key]
                elif key == "adm_credential":
                    self.parameters["adm_credential"] = kwargs[key]
                elif key == "baidu_credential":
                    self.parameters["baidu_credential"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NotificationHubsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_notificationhub()

        if not old_response:
            self.log("Notification Hub instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Notification Hub instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Notification Hub instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Notification Hub instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_notificationhub()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Notification Hub instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_notificationhub()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_notificationhub():
                time.sleep(20)
        else:
            self.log("Notification Hub instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_notificationhub(self):
        '''
        Creates or updates Notification Hub with the specified configuration.

        :return: deserialized Notification Hub instance state dictionary
        '''
        self.log("Creating / Updating the Notification Hub instance {0}".format(self.notification_hub_name))

        try:
            response = self.mgmt_client.notification_hubs.create_or_update(resource_group_name=self.resource_group,
                                                                           namespace_name=self.namespace_name,
                                                                           notification_hub_name=self.notification_hub_name,
                                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Notification Hub instance.')
            self.fail("Error creating the Notification Hub instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_notificationhub(self):
        '''
        Deletes specified Notification Hub instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Notification Hub instance {0}".format(self.notification_hub_name))
        try:
            response = self.mgmt_client.notification_hubs.delete(resource_group_name=self.resource_group,
                                                                 namespace_name=self.namespace_name,
                                                                 notification_hub_name=self.notification_hub_name)
        except CloudError as e:
            self.log('Error attempting to delete the Notification Hub instance.')
            self.fail("Error deleting the Notification Hub instance: {0}".format(str(e)))

        return True

    def get_notificationhub(self):
        '''
        Gets the properties of the specified Notification Hub.

        :return: deserialized Notification Hub instance state dictionary
        '''
        self.log("Checking if the Notification Hub instance {0} is present".format(self.notification_hub_name))
        found = False
        try:
            response = self.mgmt_client.notification_hubs.get(resource_group_name=self.resource_group,
                                                              namespace_name=self.namespace_name,
                                                              notification_hub_name=self.notification_hub_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Notification Hub instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Notification Hub instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMNotificationHubs()


if __name__ == '__main__':
    main()
