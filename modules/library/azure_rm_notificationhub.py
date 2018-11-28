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
short_description: Manage Azure Notification Hub instance.
description:
    - Create, update and delete instance of Azure Notification Hub.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    namespace_name:
        description:
            - The namespace name.
        required: True
    name:
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
                    - Required when C(state) is I(present).
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
      name: nh-sdk-hub
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMNotificationHub(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
                options=dict(
                    name=dict(
                        type='str',
                        choices=['free',
                                 'basic',
                                 'standard']
                    ),
                    tier=dict(
                        type='str'
                    ),
                    size=dict(
                        type='str'
                    ),
                    family=dict(
                        type='str'
                    ),
                    capacity=dict(
                        type='int'
                    )
                )
            ),
            notification_hub_create_or_update_parameters_name=dict(
                type='str'
            ),
            registration_ttl=dict(
                type='str'
            ),
            authorization_rules=dict(
                type='list'
                options=dict(
                    rights=dict(
                        type='list'
                    )
                )
            ),
            apns_credential=dict(
                type='dict'
                options=dict(
                    apns_certificate=dict(
                        type='str'
                    ),
                    certificate_key=dict(
                        type='str'
                    ),
                    endpoint=dict(
                        type='str'
                    ),
                    thumbprint=dict(
                        type='str'
                    ),
                    key_id=dict(
                        type='str'
                    ),
                    app_name=dict(
                        type='str'
                    ),
                    app_id=dict(
                        type='str'
                    ),
                    token=dict(
                        type='str'
                    )
                )
            ),
            wns_credential=dict(
                type='dict'
                options=dict(
                    package_sid=dict(
                        type='str'
                    ),
                    secret_key=dict(
                        type='str'
                    ),
                    windows_live_endpoint=dict(
                        type='str'
                    )
                )
            ),
            gcm_credential=dict(
                type='dict'
                options=dict(
                    gcm_endpoint=dict(
                        type='str'
                    ),
                    google_api_key=dict(
                        type='str'
                    )
                )
            ),
            mpns_credential=dict(
                type='dict'
                options=dict(
                    mpns_certificate=dict(
                        type='str'
                    ),
                    certificate_key=dict(
                        type='str'
                    ),
                    thumbprint=dict(
                        type='str'
                    )
                )
            ),
            adm_credential=dict(
                type='dict'
                options=dict(
                    client_id=dict(
                        type='str'
                    ),
                    client_secret=dict(
                        type='str'
                    ),
                    auth_token_url=dict(
                        type='str'
                    )
                )
            ),
            baidu_credential=dict(
                type='dict'
                options=dict(
                    baidu_api_key=dict(
                        type='str'
                    ),
                    baidu_end_point=dict(
                        type='str'
                    ),
                    baidu_secret_key=dict(
                        type='str'
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
        self.namespace_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMNotificationHub, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'name'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Notification Hub instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_notificationhub()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Notification Hub instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_notificationhub()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Notification Hub instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_notificationhub(self):
        '''
        Creates or updates Notification Hub with the specified configuration.

        :return: deserialized Notification Hub instance state dictionary
        '''
        self.log("Creating / Updating the Notification Hub instance {0}".format(self.name))

        try:
            response = self.mgmt_client.notification_hubs.create_or_update(resource_group_name=self.resource_group,
                                                                           namespace_name=self.namespace_name,
                                                                           notification_hub_name=self.name,
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
        self.log("Deleting the Notification Hub instance {0}".format(self.name))
        try:
            response = self.mgmt_client.notification_hubs.delete(resource_group_name=self.resource_group,
                                                                 namespace_name=self.namespace_name,
                                                                 notification_hub_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Notification Hub instance.')
            self.fail("Error deleting the Notification Hub instance: {0}".format(str(e)))

        return True

    def get_notificationhub(self):
        '''
        Gets the properties of the specified Notification Hub.

        :return: deserialized Notification Hub instance state dictionary
        '''
        self.log("Checking if the Notification Hub instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.notification_hubs.get(resource_group_name=self.resource_group,
                                                              namespace_name=self.namespace_name,
                                                              notification_hub_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Notification Hub instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Notification Hub instance.')
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


def main():
    """Main execution"""
    AzureRMNotificationHub()


if __name__ == '__main__':
    main()
