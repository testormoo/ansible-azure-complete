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
module: azure_rm_batchpool
version_added: "2.8"
short_description: Manage Pool instance.
description:
    - Create, update and delete instance of Pool.

options:
    resource_group:
        description:
            - The name of the resource group that contains the Batch account.
        required: True
    account_name:
        description:
            - The name of the Batch account.
        required: True
    pool_name:
        description:
            - The pool name. This must be unique within the account.
        required: True
    display_name:
        description:
            - The display name need not be unique and can contain any Unicode characters up to a maximum length of 1024.
    vm_size:
        description:
            - "For information about available sizes of virtual machines for Cloud Services pools (pools created with cloudServiceConfiguration), see Sizes
               for Cloud Services (http://azure.microsoft.com/documentation/articles/cloud-services-sizes-specs/). Batch supports all Cloud Services VM
               sizes except ExtraSmall. For information about available VM sizes for pools using images from the Virtual Machines Marketplace (pools
               created with virtualMachineConfiguration) see Sizes for Virtual Machines (Linux)
               (https://azure.microsoft.com/documentation/articles/virtual-machines-linux-sizes/) or Sizes for Virtual Machines (Windows)
               (https://azure.microsoft.com/documentation/articles/virtual-machines-windows-sizes/). Batch supports all Azure VM sizes except STANDARD_A0
               and those with premium storage (STANDARD_GS, STANDARD_DS, and STANDARD_DSV2 series)."
    deployment_configuration:
        description:
            - "Using CloudServiceConfiguration specifies that the nodes should be creating using Azure Cloud Services (PaaS), while
               VirtualMachineConfiguration uses Azure Virtual Machines (IaaS)."
        suboptions:
            cloud_service_configuration:
                description:
                    - "This property and I(virtual_machine_configuration) are mutually exclusive and one of the properties must be specified. This property
                       cannot be specified if the Batch account was created with its poolAllocationMode property set to 'UserSubscription'."
                suboptions:
                    os_family:
                        description:
                            - "Possible values are: 2 - OS Family 2, equivalent to Windows Server 2008 R2 SP1. 3 - OS Family 3, equivalent to Windows Server
                               2012. 4 - OS Family 4, equivalent to Windows Server 2012 R2. 5 - OS Family 5, equivalent to Windows Server 2016. For more
                               information, see Azure Guest OS Releases
                               (https://azure.microsoft.com/documentation/articles/cloud-services-guestos-update-matrix/#releases)."
                        required: True
                    target_os_version:
                        description:
                            - The default value is * which specifies the latest operating system version for the specified OS family.
                    current_os_version:
                        description:
                            - "This may differ from I(target_os_version) if the pool state is Upgrading. In this case some virtual machines may be on the
                               I(target_os_version) and some may be on the currentOSVersion during the upgrade process. Once all virtual machines have
                               upgraded, currentOSVersion is updated to be the same as I(target_os_version)."
            virtual_machine_configuration:
                description:
                    - This property and I(cloud_service_configuration) are mutually exclusive and one of the properties must be specified.
                suboptions:
                    image_reference:
                        description:
                        required: True
                        suboptions:
                            publisher:
                                description:
                                    - For example, Canonical or MicrosoftWindowsServer.
                            offer:
                                description:
                                    - For example, UbuntuServer or WindowsServer.
                            sku:
                                description:
                                    - For example, 14.04.0-LTS or 2012-R2-Datacenter.
                            version:
                                description:
                                    - "A value of 'latest' can be specified to select the latest version of an image. If omitted, the default is 'latest'."
                            id:
                                description:
                                    - "This property is mutually exclusive with other properties. The virtual machine image must be in the same region and
                                       subscription as the Azure Batch account. For information about the firewall settings for Batch node agent to
                                       communicate with Batch service see
                                       https://docs.microsoft.com/en-us/azure/batch/batch-api-basics#virtual-network-vnet-and-firewall-configuration ."
                    os_disk:
                        description:
                        suboptions:
                            caching:
                                description:
                                    - Default value is C(none).
                                choices:
                                    - 'none'
                                    - 'read_only'
                                    - 'read_write'
                    node_agent_sku_id:
                        description:
                            - "The Batch node agent is a program that runs on each node in the pool, and provides the command-and-control interface between
                               the node and the Batch service. There are different implementations of the node agent, known as SKUs, for different
                               operating systems. You must specify a node agent SKU which matches the selected image reference. To get the list of
                               supported node agent SKUs along with their list of verified image references, see the 'List supported node agent SKUs'
                               operation."
                        required: True
                    windows_configuration:
                        description:
                            - This property must not be specified if the I(image_reference) specifies a Linux OS image.
                        suboptions:
                            enable_automatic_updates:
                                description:
                                    - If omitted, the default value is true.
                    data_disks:
                        description:
                            - This property must be specified if the compute nodes in the pool need to have empty data disks attached to them.
                        type: list
                        suboptions:
                            lun:
                                description:
                                    - The lun is used to uniquely identify each data disk. If attaching multiple disks, each should have a distinct lun.
                                required: True
                            caching:
                                description:
                                    - "Values are:"
                                    -  C(none) - The caching mode for the disk is not enabled.
                                    -  C(read_only) - The caching mode for the disk is read only.
                                    -  C(read_write) - The caching mode for the disk is read and write.
                                    - " The default value for caching is C(none). For information about the caching options see:
                                       https://blogs.msdn.microsoft.com/windowsazurestorage/2012/06/27/exploring-windows-azure-drives-disks-and-images/."
                                choices:
                                    - 'none'
                                    - 'read_only'
                                    - 'read_write'
                            disk_size_gb:
                                description:
                                required: True
                            storage_account_type:
                                description:
                                    - "If omitted, the default is 'C(standard_lrs)'. Values are:"
                                    -  C(standard_lrs) - The data disk should use standard locally redundant storage.
                                    -  C(premium_lrs) - The data disk should use premium locally redundant storage.
                                choices:
                                    - 'standard_lrs'
                                    - 'premium_lrs'
                    license_type:
                        description:
                            - "This only applies to images that contain the Windows operating system, and should only be used when you hold valid
                               on-premises licenses for the nodes which will be deployed. If omitted, no on-premises licensing discount is applied. Values
                               are:"
                            -  Windows_Server - The on-premises license is for Windows Server.
                            -  Windows_Client - The on-premises license is for Windows Client.
    scale_settings:
        description:
        suboptions:
            fixed_scale:
                description:
                    - This property and I(auto_scale) are mutually exclusive and one of the properties must be specified.
                suboptions:
                    resize_timeout:
                        description:
                            - "The default value is 15 minutes. Timeout values use ISO 8601 format. For example, use PT10M for 10 minutes. The minimum value
                               is 5 minutes. If you specify a value less than 5 minutes, the Batch service rejects the request with an error; if you are
                               calling the REST API directly, the HTTP status code is 400 (Bad Request)."
                    target_dedicated_nodes:
                        description:
                            - At least one of targetDedicatedNodes, targetLowPriority nodes must be set.
                    target_low_priority_nodes:
                        description:
                            - At least one of I(target_dedicated_nodes), targetLowPriority nodes must be set.
                    node_deallocation_option:
                        description:
                            - If omitted, the default value is C(requeue).
                        choices:
                            - 'requeue'
                            - 'terminate'
                            - 'task_completion'
                            - 'retained_data'
            auto_scale:
                description:
                    - This property and I(fixed_scale) are mutually exclusive and one of the properties must be specified.
                suboptions:
                    formula:
                        description:
                        required: True
                    evaluation_interval:
                        description:
                            - If omitted, the default value is 15 minutes (PT15M).
    inter_node_communication:
        description:
            - "This imposes restrictions on which nodes can be assigned to the pool. Enabling this value can reduce the chance of the requested number of
               nodes to be allocated in the pool. If not specified, this value defaults to 'C(disabled)'."
        choices:
            - 'enabled'
            - 'disabled'
    network_configuration:
        description:
        suboptions:
            subnet_id:
                description:
                    - "The virtual network must be in the same region and subscription as the Azure Batch account. The specified subnet should have enough
                       free IP addresses to accommodate the number of nodes in the pool. If the subnet doesn't have enough free IP addresses, the pool will
                       partially allocate compute nodes, and a resize error will occur. The 'MicrosoftAzureBatch' service principal must have the 'Classic
                       Virtual Machine Contributor' Role-Based Access Control (RBAC) role for the specified VNet. The specified subnet must allow
                       communication from the Azure Batch service to be able to schedule tasks on the compute nodes. This can be verified by checking if
                       the specified VNet has any associated Network Security Groups (NSG). If communication to the compute nodes in the specified subnet
                       is denied by an NSG, then the Batch service will set the state of the compute nodes to unusable. For pools created via
                       virtualMachineConfiguration the Batch account must have poolAllocationMode userSubscription in order to use a VNet. If the specified
                       VNet has any associated Network Security Groups (NSG), then a few reserved system ports must be enabled for inbound communication.
                       For pools created with a virtual machine configuration, enable ports 29876 and 29877, as well as port 22 for Linux and port 3389 for
                       Windows. For pools created with a cloud service configuration, enable ports 10100, 20100, and 30100. Also enable outbound
                       connections to Azure Storage on port 443. For more details see:
                       https://docs.microsoft.com/en-us/azure/batch/batch-api-basics#virtual-network-vnet-and-firewall-configuration"
            endpoint_configuration:
                description:
                    - Pool endpoint configuration is only supported on pools with the virtualMachineConfiguration property.
                suboptions:
                    inbound_nat_pools:
                        description:
                            - "The maximum number of inbound NAT pools per Batch pool is 5. If the maximum number of inbound NAT pools is exceeded the
                               request fails with HTTP status code 400."
                        required: True
                        type: list
                        suboptions:
                            name:
                                description:
                                    - "The name must be unique within a Batch pool, can contain letters, numbers, underscores, periods, and hyphens. Names
                                       must start with a letter or number, must end with a letter, number, or underscore, and cannot exceed 77 characters.
                                       If any invalid values are provided the request fails with HTTP status code 400."
                                required: True
                            protocol:
                                description:
                                    - "Possible values include: 'C(tcp)', 'C(udp)'"
                                required: True
                                choices:
                                    - 'tcp'
                                    - 'udp'
                            backend_port:
                                description:
                                    - "This must be unique within a Batch pool. Acceptable values are between 1 and 65535 except for 22, 3389, 29876 and
                                       29877 as these are reserved. If any reserved values are provided the request fails with HTTP status code 400."
                                required: True
                            frontend_port_range_start:
                                description:
                                    - "Acceptable values range between 1 and 65534 except ports from 50000 to 55000 which are reserved. All ranges within a
                                       pool must be distinct and cannot overlap. If any reserved or overlapping values are provided the request fails with
                                       HTTP status code 400."
                                required: True
                            frontend_port_range_end:
                                description:
                                    - "Acceptable values range between 1 and 65534 except ports from 50000 to 55000 which are reserved by the Batch service.
                                       All ranges within a pool must be distinct and cannot overlap. If any reserved or overlapping values are provided the
                                       request fails with HTTP status code 400."
                                required: True
                            network_security_group_rules:
                                description:
                                    - "The maximum number of rules that can be specified across all the endpoints on a Batch pool is 25. If no network
                                       security group rules are specified, a default rule will be created to allow inbound access to the specified
                                       I(backend_port). If the maximum number of network security group rules is exceeded the request fails with HTTP
                                       status code 400."
                                type: list
                                suboptions:
                                    priority:
                                        description:
                                            - "Priorities within a pool must be unique and are evaluated in order of priority. The lower the number the
                                               higher the priority. For example, rules could be specified with order numbers of 150, 250, and 350. The rule
                                               with the order number of 150 takes precedence over the rule that has an order of 250. Allowed priorities are
                                               150 to 3500. If any reserved or duplicate values are provided the request fails with HTTP status code 400."
                                        required: True
                                    access:
                                        description:
                                            - "Possible values include: 'C(allow)', 'C(deny)'"
                                        required: True
                                        choices:
                                            - 'allow'
                                            - 'deny'
                                    source_address_prefix:
                                        description:
                                            - "Valid values are a single IP address (i.e. 10.10.10.10), IP subnet (i.e. 192.168.1.0/24), default tag, or *
                                               (for all addresses).  If any other values are provided the request fails with HTTP status code 400."
                                        required: True
    max_tasks_per_node:
        description:
    task_scheduling_policy:
        description:
        suboptions:
            node_fill_type:
                description:
                    - "Possible values include: 'C(spread)', 'C(pack)'"
                required: True
                choices:
                    - 'spread'
                    - 'pack'
    user_accounts:
        description:
        type: list
        suboptions:
            name:
                description:
                required: True
            password:
                description:
                required: True
            elevation_level:
                description:
                    - "C(non_admin) - The auto user is a standard user without elevated access. C(admin) - The auto user is a user with elevated access and
                       operates with full Administrator permissions. The default value is C(non_admin)."
                choices:
                    - 'non_admin'
                    - 'admin'
            linux_user_configuration:
                description:
                    - This property is ignored if specified on a Windows pool. If not specified, the user is created with the default options.
                suboptions:
                    uid:
                        description:
                            - "The uid and I(gid) properties must be specified together or not at all. If not specified the underlying operating system
                               picks the uid."
                    gid:
                        description:
                            - "The I(uid) and gid properties must be specified together or not at all. If not specified the underlying operating system
                               picks the gid."
                    ssh_private_key:
                        description:
                            - "The private key must not be password protected. The private key is used to automatically configure asymmetric-key based
                               authentication for SSH between nodes in a Linux pool when the pool's enableInterNodeCommunication property is true (it is
                               ignored if enableInterNodeCommunication is false). It does this by placing the key pair into the user's .ssh directory. If
                               not specified, password-less SSH is not configured between nodes (no modification of the user's .ssh directory is done)."
    metadata:
        description:
            - The Batch service does not assign any meaning to metadata; it is solely for the use of user code.
        type: list
        suboptions:
            name:
                description:
                required: True
            value:
                description:
                required: True
    start_task:
        description:
            - In an PATCH (update) operation, this property can be set to an empty object to remove the start task from the pool.
        suboptions:
            command_line:
                description:
                    - "The command line does not run under a shell, and therefore cannot take advantage of shell features such as environment variable
                       expansion. If you want to take advantage of such features, you should invoke the shell in the command line, for example using 'cmd
                       /c MyCommand' in Windows or '/bin/sh -c MyCommand' in Linux. Required if any other properties of the startTask are specified."
            resource_files:
                description:
                type: list
                suboptions:
                    blob_source:
                        description:
                            - "This URL must be readable using anonymous access; that is, the Batch service does not present any credentials when
                               downloading the blob. There are two ways to get such a URL for a blob in Azure storage: include a Shared Access Signature
                               (SAS) granting read permissions on the blob, or set the ACL for the blob or its container to allow public access."
                        required: True
                    file_path:
                        description:
                        required: True
                    file_mode:
                        description:
                            - "This property applies only to files being downloaded to Linux compute nodes. It will be ignored if it is specified for a
                               resourceFile which will be downloaded to a Windows node. If this property is not specified for a Linux node, then a default
                               value of 0770 is applied to the file."
            environment_settings:
                description:
                type: list
                suboptions:
                    name:
                        description:
                        required: True
                    value:
                        description:
            user_identity:
                description:
                    - If omitted, the task runs as a non-administrative user unique to the task.
                suboptions:
                    user_name:
                        description:
                            - The userName and I(auto_user) properties are mutually exclusive; you must specify one but not both.
                    auto_user:
                        description:
                            - The I(user_name) and autoUser properties are mutually exclusive; you must specify one but not both.
                        suboptions:
                            scope:
                                description:
                                    - "C(pool) - specifies that the C(task) runs as the common auto user account which is created on every node in a
                                       C(pool). C(task) - specifies that the service should create a new user for the C(task). The default value is
                                       C(task)."
                                choices:
                                    - 'task'
                                    - 'pool'
                            elevation_level:
                                description:
                                    - "C(non_admin) - The auto user is a standard user without elevated access. C(admin) - The auto user is a user with
                                       elevated access and operates with full Administrator permissions. The default value is C(non_admin)."
                                choices:
                                    - 'non_admin'
                                    - 'admin'
            max_task_retry_count:
                description:
                    - "The Batch service retries a task if its exit code is nonzero. Note that this value specifically controls the number of retries. The
                       Batch service will try the task once, and may then retry up to this limit. For example, if the maximum retry count is 3, Batch tries
                       the task up to 4 times (one initial try and 3 retries). If the maximum retry count is 0, the Batch service does not retry the task.
                       If the maximum retry count is -1, the Batch service retries the task without limit."
            wait_for_success:
                description:
                    - "If true and the start task fails on a compute node, the Batch service retries the start task up to its maximum retry count
                       (I(max_task_retry_count)). If the task has still not completed successfully after all retries, then the Batch service marks the
                       compute node unusable, and will not schedule tasks to it. This condition can be detected via the node state and scheduling error
                       detail. If false, the Batch service will not wait for the start task to complete. In this case, other tasks can start executing on
                       the compute node while the start task is still running; and even if the start task fails, new tasks will continue to be scheduled on
                       the node. The default is false."
    certificates:
        description:
            - "For Windows compute nodes, the Batch service installs the certificates to the specified certificate store and location. For Linux compute
               nodes, the certificates are stored in a directory inside the task working directory and an environment variable AZ_BATCH_CERTIFICATES_DIR is
               supplied to the task to query for this location. For certificates with visibility of 'remoteUser', a 'certs' directory is created in the
               user's home directory (e.g., /home/{user-name}/certs) and certificates are placed in that directory."
        type: list
        suboptions:
            id:
                description:
                required: True
            store_location:
                description:
                    - "The default value is C(current_user). This property is applicable only for pools configured with Windows nodes (that is, created with
                       cloudServiceConfiguration, or with virtualMachineConfiguration using a Windows image reference). For Linux compute nodes, the
                       certificates are stored in a directory inside the task working directory and an environment variable AZ_BATCH_CERTIFICATES_DIR is
                       supplied to the task to query for this location. For certificates with I(visibility) of 'remoteUser', a 'certs' directory is created
                       in the user's home directory (e.g., /home/{user-name}/certs) and certificates are placed in that directory."
                choices:
                    - 'current_user'
                    - 'local_machine'
            store_name:
                description:
                    - "This property is applicable only for pools configured with Windows nodes (that is, created with cloudServiceConfiguration, or with
                       virtualMachineConfiguration using a Windows image reference). Common store names include: My, Root, CA, Trust, Disallowed,
                       TrustedPeople, TrustedPublisher, AuthRoot, AddressBook, but any custom store name can also be used. The default value is My."
            visibility:
                description:
                    - "Values are:"
                    -  starttask - The user account under which the start task is run.
                    -  task - The accounts under which job tasks are run.
                    -  remoteuser - The accounts under which users remotely access the node.
                    -  You can specify more than one visibility in this collection. The default is all accounts.
                type: list
    application_packages:
        description:
            - "Changes to application packages affect all new compute nodes joining the pool, but do not affect compute nodes that are already in the pool
               until they are rebooted or reimaged."
        type: list
        suboptions:
            id:
                description:
                required: True
            version:
                description:
                    - "If this is omitted, and no default version is specified for this application, the request fails with the error code
                       InvalidApplicationPackageReferences. If you are calling the REST API directly, the HTTP status code is 409."
    application_licenses:
        description:
            - "The list of application licenses must be a subset of available Batch service application licenses. If a license is requested which is not
               supported, pool creation will fail."
        type: list
    if_match:
        description:
            - "The entity state (ETag) version of the pool to update. A value of '*' can be used to apply the operation only if the pool already exists. If
               omitted, this operation will always be applied."
    if_none_match:
        description:
            - "Set to '*' to allow a new pool to be created, but to prevent updating an existing pool. Other values will be ignored."
    state:
      description:
        - Assert the state of the Pool.
        - Use 'present' to create or update an Pool and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Pool
    azure_rm_batchpool:
      resource_group: default-azurebatch-japaneast
      account_name: sampleacct
      pool_name: testpool
      if_match: NOT FOUND
      if_none_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The ID of the resource.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/default-azurebatch-japaneast/providers/Microsoft.Batch/batchAccounts/sampleacct/pools/testpool
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.batch import BatchManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPool(AzureRMModuleBase):
    """Configuration class for an Azure RM Pool resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            pool_name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='str'
            ),
            vm_size=dict(
                type='str'
            ),
            deployment_configuration=dict(
                type='dict'
            ),
            scale_settings=dict(
                type='dict'
            ),
            inter_node_communication=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            network_configuration=dict(
                type='dict'
            ),
            max_tasks_per_node=dict(
                type='int'
            ),
            task_scheduling_policy=dict(
                type='dict'
            ),
            user_accounts=dict(
                type='list'
            ),
            metadata=dict(
                type='list'
            ),
            start_task=dict(
                type='dict'
            ),
            certificates=dict(
                type='list'
            ),
            application_packages=dict(
                type='list'
            ),
            application_licenses=dict(
                type='list'
            ),
            if_match=dict(
                type='str'
            ),
            if_none_match=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.pool_name = None
        self.parameters = dict()
        self.if_match = None
        self.if_none_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPool, self).__init__(derived_arg_spec=self.module_arg_spec,
                                          supports_check_mode=True,
                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "vm_size":
                    self.parameters["vm_size"] = kwargs[key]
                elif key == "deployment_configuration":
                    self.parameters["deployment_configuration"] = kwargs[key]
                elif key == "scale_settings":
                    self.parameters["scale_settings"] = kwargs[key]
                elif key == "inter_node_communication":
                    self.parameters["inter_node_communication"] = _snake_to_camel(kwargs[key], True)
                elif key == "network_configuration":
                    self.parameters["network_configuration"] = kwargs[key]
                elif key == "max_tasks_per_node":
                    self.parameters["max_tasks_per_node"] = kwargs[key]
                elif key == "task_scheduling_policy":
                    ev = kwargs[key]
                    if 'node_fill_type' in ev:
                        if ev['node_fill_type'] == 'spread':
                            ev['node_fill_type'] = 'Spread'
                        elif ev['node_fill_type'] == 'pack':
                            ev['node_fill_type'] = 'Pack'
                    self.parameters["task_scheduling_policy"] = ev
                elif key == "user_accounts":
                    ev = kwargs[key]
                    if 'elevation_level' in ev:
                        if ev['elevation_level'] == 'non_admin':
                            ev['elevation_level'] = 'NonAdmin'
                        elif ev['elevation_level'] == 'admin':
                            ev['elevation_level'] = 'Admin'
                    self.parameters["user_accounts"] = ev
                elif key == "metadata":
                    self.parameters["metadata"] = kwargs[key]
                elif key == "start_task":
                    self.parameters["start_task"] = kwargs[key]
                elif key == "certificates":
                    ev = kwargs[key]
                    if 'store_location' in ev:
                        if ev['store_location'] == 'current_user':
                            ev['store_location'] = 'CurrentUser'
                        elif ev['store_location'] == 'local_machine':
                            ev['store_location'] = 'LocalMachine'
                    self.parameters["certificates"] = ev
                elif key == "application_packages":
                    self.parameters["application_packages"] = kwargs[key]
                elif key == "application_licenses":
                    self.parameters["application_licenses"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BatchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_pool()

        if not old_response:
            self.log("Pool instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Pool instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Pool instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Pool instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_pool()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Pool instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_pool()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_pool():
                time.sleep(20)
        else:
            self.log("Pool instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_pool(self):
        '''
        Creates or updates Pool with the specified configuration.

        :return: deserialized Pool instance state dictionary
        '''
        self.log("Creating / Updating the Pool instance {0}".format(self.pool_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.pool.create(resource_group_name=self.resource_group,
                                                        account_name=self.account_name,
                                                        pool_name=self.pool_name,
                                                        parameters=self.parameters)
            else:
                response = self.mgmt_client.pool.update(resource_group_name=self.resource_group,
                                                        account_name=self.account_name,
                                                        pool_name=self.pool_name,
                                                        parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Pool instance.')
            self.fail("Error creating the Pool instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_pool(self):
        '''
        Deletes specified Pool instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Pool instance {0}".format(self.pool_name))
        try:
            response = self.mgmt_client.pool.delete(resource_group_name=self.resource_group,
                                                    account_name=self.account_name,
                                                    pool_name=self.pool_name)
        except CloudError as e:
            self.log('Error attempting to delete the Pool instance.')
            self.fail("Error deleting the Pool instance: {0}".format(str(e)))

        return True

    def get_pool(self):
        '''
        Gets the properties of the specified Pool.

        :return: deserialized Pool instance state dictionary
        '''
        self.log("Checking if the Pool instance {0} is present".format(self.pool_name))
        found = False
        try:
            response = self.mgmt_client.pool.get(resource_group_name=self.resource_group,
                                                 account_name=self.account_name,
                                                 pool_name=self.pool_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Pool instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Pool instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMPool()


if __name__ == '__main__':
    main()
