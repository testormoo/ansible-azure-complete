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
module: azure_rm_storageimportexportjob
version_added: "2.8"
short_description: Manage Azure Job instance.
description:
    - Create, update and delete instance of Azure Job.

options:
    job_name:
        description:
            - The name of the import/I(export) job.
        required: True
    resource_group:
        description:
            - The resource group name uniquely identifies the resource group within the user subscription.
        required: True
    self.config.accept_language:
        description:
            - Specifies the preferred language for the response.
    client_tenant_id:
        description:
            - The tenant ID of the client making the request.
    location:
        description:
            - Specifies the supported Azure location where the job should be created
    storage_account_id:
        description:
            - The resource identifier of the storage account where data will be imported to or exported from.
    job_type:
        description:
            - The type of job
    return_address:
        description:
            - Specifies the return address information for the job.
        suboptions:
            recipient_name:
                description:
                    - The name of the recipient who will receive the hard drives when they are returned.
                    - Required when C(state) is I(present).
            street_address1:
                description:
                    - The first line of the street address to use when returning the drives.
                    - Required when C(state) is I(present).
            street_address2:
                description:
                    - The second line of the street address to use when returning the drives.
            city:
                description:
                    - The city name to use when returning the drives.
                    - Required when C(state) is I(present).
            state_or_province:
                description:
                    - The state or province to use when returning the drives.
            postal_code:
                description:
                    - The postal code to use when returning the drives.
                    - Required when C(state) is I(present).
            country_or_region:
                description:
                    - The country or region to use when returning the drives.
                    - Required when C(state) is I(present).
            phone:
                description:
                    - Phone number of the recipient of the returned drives.
                    - Required when C(state) is I(present).
            email:
                description:
                    - Email address of the recipient of the returned drives.
                    - Required when C(state) is I(present).
    return_shipping:
        description:
            - "Specifies the return carrier and customer's account with the carrier. "
        suboptions:
            carrier_name:
                description:
                    - "The carrier's name."
                    - Required when C(state) is I(present).
            carrier_account_number:
                description:
                    - "The customer's account number with the carrier."
                    - Required when C(state) is I(present).
    shipping_information:
        description:
            - Contains information about the Microsoft datacenter to which the drives should be shipped.
        suboptions:
            recipient_name:
                description:
                    - The name of the recipient who will receive the hard drives when they are returned.
                    - Required when C(state) is I(present).
            street_address1:
                description:
                    - The first line of the street address to use when returning the drives.
                    - Required when C(state) is I(present).
            street_address2:
                description:
                    - The second line of the street address to use when returning the drives.
            city:
                description:
                    - The city name to use when returning the drives.
                    - Required when C(state) is I(present).
            state_or_province:
                description:
                    - The state or province to use when returning the drives.
                    - Required when C(state) is I(present).
            postal_code:
                description:
                    - The postal code to use when returning the drives.
                    - Required when C(state) is I(present).
            country_or_region:
                description:
                    - The country or region to use when returning the drives.
                    - Required when C(state) is I(present).
            phone:
                description:
                    - Phone number of the recipient of the returned drives.
    delivery_package:
        description:
            - Contains information about the package being shipped by the customer to the Microsoft data center.
        suboptions:
            carrier_name:
                description:
                    - The name of the carrier that is used to ship the import or export drives.
                    - Required when C(state) is I(present).
            tracking_number:
                description:
                    - The tracking number of the package.
                    - Required when C(state) is I(present).
            drive_count:
                description:
                    - The number of drives included in the package.
                    - Required when C(state) is I(present).
            ship_date:
                description:
                    - The date when the package is shipped.
                    - Required when C(state) is I(present).
    return_package:
        description:
            - "Contains information about the package being shipped from the Microsoft data center to the customer to return the drives. The format is the
               same as the I(delivery_package) property above. This property is not included if the drives have not yet been returned. "
        suboptions:
            carrier_name:
                description:
                    - The name of the carrier that is used to ship the import or export drives.
                    - Required when C(state) is I(present).
            tracking_number:
                description:
                    - The tracking number of the package.
                    - Required when C(state) is I(present).
            drive_count:
                description:
                    - The number of drives included in the package.
                    - Required when C(state) is I(present).
            ship_date:
                description:
                    - The date when the package is shipped.
                    - Required when C(state) is I(present).
    diagnostics_path:
        description:
            - The virtual blob directory to which the copy logs and backups of drive manifest files (if enabled) will be stored.
    log_level:
        description:
            - Default value is Error. Indicates whether error logging or verbose logging will be enabled.
    backup_drive_manifest:
        description:
            - Default value is false. Indicates whether the manifest files on the drives should be copied to block blobs.
    state:
        description:
            - Current state of the job.
    cancel_requested:
        description:
            - Indicates whether a request has been submitted to cancel the job.
    percent_complete:
        description:
            - Overall percentage completed for the job.
    incomplete_blob_list_uri:
        description:
            - "A blob path that points to a block blob containing a list of blob names that were not exported due to insufficient drive space. If all blobs
               were exported successfully, then this element is not included in the response."
    drive_list:
        description:
            - List of up to ten drives that comprise the job. The drive list is a required element for an import job; it is not specified for I(export) jobs.
        type: list
        suboptions:
            drive_id:
                description:
                    - "The drive's hardware serial number, without spaces."
            bit_locker_key:
                description:
                    - The BitLocker key used to encrypt the drive.
            manifest_file:
                description:
                    - The relative path of the manifest file on the drive.
            manifest_hash:
                description:
                    - The Base16-encoded MD5 hash of the manifest file on the drive.
            drive_header_hash:
                description:
                    - The drive header hash value.
            state:
                description:
                    - "The drive's current state."
                choices:
                    - 'specified'
                    - 'received'
                    - 'never_received'
                    - 'transferring'
                    - 'completed'
                    - 'completed_more_info'
                    - 'shipped_back'
            copy_status:
                description:
                    - "Detailed status about the data transfer process. This field is not returned in the response until the drive is in the C(transferring)
                       I(state)."
            percent_complete:
                description:
                    - Percentage C(completed) for the drive.
            verbose_log_uri:
                description:
                    - A URI that points to the blob containing the verbose log for the data transfer operation.
            error_log_uri:
                description:
                    - A URI that points to the blob containing the error log for the data transfer operation.
            manifest_uri:
                description:
                    - A URI that points to the blob containing the drive manifest file.
            bytes_succeeded:
                description:
                    - Bytes successfully transferred for the drive.
    export:
        description:
            - A property containing information about the blobs to be exported for an export job. This property is included for export jobs only.
        suboptions:
            blob_path:
                description:
                    - A collection of blob-path strings.
                type: list
            blob_path_prefix:
                description:
                    - A collection of blob-prefix strings.
                type: list
            blob_listblob_path:
                description:
                    - "The relative URI to the block blob that contains the list of blob paths or blob path prefixes as defined above, beginning with the
                       container name. If the blob is in root container, the URI must begin with $root. "
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
    azure_rm_storageimportexportjob:
      job_name: test-by1-import
      resource_group: Default-Storage-WestUS
      self.config.accept_language: NOT FOUND
      client_tenant_id: NOT FOUND
      location: West US
      storage_account_id: /subscriptions/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/resourceGroups/Default-Storage-WestUS/providers/Microsoft.ClassicStorage/storageAccounts/test
      job_type: Import
      return_address:
        recipient_name: Tets
        street_address1: Street1
        street_address2: street2
        city: Redmond
        state_or_province: wa
        postal_code: 98007
        country_or_region: USA
        phone: 4250000000
        email: Test@contoso.com
      diagnostics_path: waimportexport
      log_level: Verbose
      backup_drive_manifest: True
      drive_list:
        - drive_id: 9CA995BB
          bit_locker_key: 238810-662376-448998-450120-652806-203390-606320-483076
          manifest_file: \DriveManifest.xml
          manifest_hash: 109B21108597EF36D5785F08303F3638
'''

RETURN = '''
id:
    description:
        - Specifies the resource identifier of the job.
    returned: always
    type: str
    sample: /subscriptions/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/resourceGroups/Default-Storage-WestUS/providers/Microsoft.ImportExport/jobs/test-by1-import
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storageimportexport import StorageImportExport
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
            job_name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            self.config.accept_language=dict(
                type='str'
            ),
            client_tenant_id=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            storage_account_id=dict(
                type='str'
            ),
            job_type=dict(
                type='str'
            ),
            return_address=dict(
                type='dict',
                options=dict(
                    recipient_name=dict(
                        type='str'
                    ),
                    street_address1=dict(
                        type='str'
                    ),
                    street_address2=dict(
                        type='str'
                    ),
                    city=dict(
                        type='str'
                    ),
                    state_or_province=dict(
                        type='str'
                    ),
                    postal_code=dict(
                        type='str'
                    ),
                    country_or_region=dict(
                        type='str'
                    ),
                    phone=dict(
                        type='str'
                    ),
                    email=dict(
                        type='str'
                    )
                )
            ),
            return_shipping=dict(
                type='dict',
                options=dict(
                    carrier_name=dict(
                        type='str'
                    ),
                    carrier_account_number=dict(
                        type='str'
                    )
                )
            ),
            shipping_information=dict(
                type='dict',
                options=dict(
                    recipient_name=dict(
                        type='str'
                    ),
                    street_address1=dict(
                        type='str'
                    ),
                    street_address2=dict(
                        type='str'
                    ),
                    city=dict(
                        type='str'
                    ),
                    state_or_province=dict(
                        type='str'
                    ),
                    postal_code=dict(
                        type='str'
                    ),
                    country_or_region=dict(
                        type='str'
                    ),
                    phone=dict(
                        type='str'
                    )
                )
            ),
            delivery_package=dict(
                type='dict',
                options=dict(
                    carrier_name=dict(
                        type='str'
                    ),
                    tracking_number=dict(
                        type='str'
                    ),
                    drive_count=dict(
                        type='int'
                    ),
                    ship_date=dict(
                        type='str'
                    )
                )
            ),
            return_package=dict(
                type='dict',
                options=dict(
                    carrier_name=dict(
                        type='str'
                    ),
                    tracking_number=dict(
                        type='str'
                    ),
                    drive_count=dict(
                        type='int'
                    ),
                    ship_date=dict(
                        type='str'
                    )
                )
            ),
            diagnostics_path=dict(
                type='str'
            ),
            log_level=dict(
                type='str'
            ),
            backup_drive_manifest=dict(
                type='str'
            ),
            state=dict(
                type='str'
            ),
            cancel_requested=dict(
                type='str'
            ),
            percent_complete=dict(
                type='int'
            ),
            incomplete_blob_list_uri=dict(
                type='str'
            ),
            drive_list=dict(
                type='list',
                options=dict(
                    drive_id=dict(
                        type='str'
                    ),
                    bit_locker_key=dict(
                        type='str'
                    ),
                    manifest_file=dict(
                        type='str'
                    ),
                    manifest_hash=dict(
                        type='str'
                    ),
                    drive_header_hash=dict(
                        type='str'
                    ),
                    state=dict(
                        type='str',
                        choices=['specified',
                                 'received',
                                 'never_received',
                                 'transferring',
                                 'completed',
                                 'completed_more_info',
                                 'shipped_back']
                    ),
                    copy_status=dict(
                        type='str'
                    ),
                    percent_complete=dict(
                        type='int'
                    ),
                    verbose_log_uri=dict(
                        type='str'
                    ),
                    error_log_uri=dict(
                        type='str'
                    ),
                    manifest_uri=dict(
                        type='str'
                    ),
                    bytes_succeeded=dict(
                        type='int'
                    )
                )
            ),
            export=dict(
                type='dict',
                options=dict(
                    blob_path=dict(
                        type='list'
                    ),
                    blob_path_prefix=dict(
                        type='list'
                    ),
                    blob_listblob_path=dict(
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

        self.job_name = None
        self.resource_group = None
        self.self.config.accept_language = None
        self.client_tenant_id = None
        self.body = dict()

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
                self.body[key] = kwargs[key]

        dict_expand(self.body, ['storage_account_id'])
        dict_expand(self.body, ['job_type'])
        dict_expand(self.body, ['return_address'])
        dict_expand(self.body, ['return_shipping'])
        dict_expand(self.body, ['shipping_information'])
        dict_expand(self.body, ['delivery_package'])
        dict_expand(self.body, ['return_package'])
        dict_expand(self.body, ['diagnostics_path'])
        dict_expand(self.body, ['log_level'])
        dict_expand(self.body, ['backup_drive_manifest'])
        dict_expand(self.body, ['state'])
        dict_expand(self.body, ['cancel_requested'])
        dict_expand(self.body, ['percent_complete'])
        dict_expand(self.body, ['incomplete_blob_list_uri'])
        dict_camelize(self.body, ['drive_list', 'state'], True)
        dict_expand(self.body, ['drive_list'])
        dict_expand(self.body, ['export'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageImportExport,
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
                if (not default_compare(self.body, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_job(self):
        '''
        Creates or updates Job with the specified configuration.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Creating / Updating the Job instance {0}".format(self.self.config.accept_language))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.jobs.create(job_name=self.job_name,
                                                        resource_group_name=self.resource_group,
                                                        body=self.body)
            else:
                response = self.mgmt_client.jobs.update(job_name=self.job_name,
                                                        resource_group_name=self.resource_group,
                                                        body=self.body)
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
        self.log("Deleting the Job instance {0}".format(self.self.config.accept_language))
        try:
            response = self.mgmt_client.jobs.delete(job_name=self.job_name,
                                                    resource_group_name=self.resource_group)
        except CloudError as e:
            self.log('Error attempting to delete the Job instance.')
            self.fail("Error deleting the Job instance: {0}".format(str(e)))

        return True

    def get_job(self):
        '''
        Gets the properties of the specified Job.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Checking if the Job instance {0} is present".format(self.self.config.accept_language))
        found = False
        try:
            response = self.mgmt_client.jobs.get(job_name=self.job_name,
                                                 resource_group_name=self.resource_group)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job instance.')
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
    AzureRMJob()


if __name__ == '__main__':
    main()
