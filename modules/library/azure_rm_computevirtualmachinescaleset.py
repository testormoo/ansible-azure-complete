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
module: azure_rm_computevirtualmachinescaleset
version_added: "2.8"
short_description: Manage Virtual Machine Scale Set instance.
description:
    - Create, update and delete instance of Virtual Machine Scale Set.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the VM scale set to create or update.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The virtual machine scale set sku.
        suboptions:
            name:
                description:
                    - The sku name.
            tier:
                description:
                    - "Specifies the tier of virtual machines in a scale set.<br /><br /> Possible Values:<br /><br /> **Standard**<br /><br /> **Basic**"
            capacity:
                description:
                    - Specifies the number of virtual machines in the scale set.
    plan:
        description:
            - "Specifies information about the marketplace image used to create the virtual machine. This element is only used for marketplace images.
               Before you can use a marketplace image from an API, you must enable the image for programmatic use.  In the Azure portal, find the
               marketplace image that you want to use and then click **Want to deploy programmatically, Get Started ->**. Enter any required information
               and then click **Save**."
        suboptions:
            name:
                description:
                    - The plan ID.
            publisher:
                description:
                    - The publisher ID.
            product:
                description:
                    - Specifies the product of the image from the marketplace. This is the same value as Offer under the imageReference element.
            promotion_code:
                description:
                    - The promotion code.
    upgrade_policy:
        description:
            - The upgrade policy.
        suboptions:
            mode:
                description:
                    - "Specifies the mode of an upgrade to virtual machines in the scale set.<br /><br /> Possible values are:<br /><br /> **C(manual)** -
                       You  control the application of updates to virtual machines in the scale set. You do this by using the manualUpgrade action.<br
                       /><br /> **C(automatic)** - All virtual machines in the scale set are  automatically updated at the same time."
                choices:
                    - 'automatic'
                    - 'manual'
                    - 'rolling'
            rolling_upgrade_policy:
                description:
                    - The configuration parameters used while performing a C(rolling) upgrade.
                suboptions:
                    max_batch_instance_percent:
                        description:
                            - "The maximum percent of total virtual machine instances that will be upgraded simultaneously by the rolling upgrade in one
                               batch. As this is a maximum, unhealthy instances in previous or future batches can cause the percentage of instances in a
                               batch to decrease to ensure higher reliability. The default value for this parameter is 20%."
                    max_unhealthy_instance_percent:
                        description:
                            - "The maximum percentage of the total virtual machine instances in the scale set that can be simultaneously unhealthy, either
                               as a result of being upgraded, or by being found in an unhealthy state by the virtual machine health checks before the
                               rolling upgrade aborts. This constraint will be checked prior to starting any batch. The default value for this parameter is
                               20%."
                    max_unhealthy_upgraded_instance_percent:
                        description:
                            - "The maximum percentage of upgraded virtual machine instances that can be found to be in an unhealthy state. This check will
                               happen after each batch is upgraded. If this percentage is ever exceeded, the rolling update aborts. The default value for
                               this parameter is 20%."
                    pause_time_between_batches:
                        description:
                            - "The wait time between completing the update for all virtual machines in one batch and starting the next batch. The time
                               duration should be specified in ISO 8601 format. The default value is 0 seconds (PT0S)."
            automatic_os_upgrade_policy:
                description:
                    - Configuration parameters used for performing C(automatic) OS Upgrade.
                suboptions:
                    enable_automatic_os_upgrade:
                        description:
                            - "Whether OS upgrades should automatically be applied to scale set instances in a rolling fashion when a newer version of the
                               image becomes available. Default value is false."
                    disable_automatic_rollback:
                        description:
                            - Whether OS image rollback feature should be disabled. Default value is false.
    virtual_machine_profile:
        description:
            - The virtual machine profile.
        suboptions:
            os_profile:
                description:
                    - Specifies the operating system settings for the virtual machines in the scale set.
                suboptions:
                    computer_name_prefix:
                        description:
                            - "Specifies the computer name prefix for all of the virtual machines in the scale set. Computer name prefixes must be 1 to 15
                               characters long."
                    admin_username:
                        description:
                            - "Specifies the name of the administrator account. <br><br> **Windows-only restriction:** Cannot end in '.' <br><br>
                               **Disallowed values:** 'administrator', 'admin', 'user', 'user1', 'test', 'user2', 'test1', 'user3', 'admin1', '1', '123',
                               'a', 'actuser', 'adm', 'admin2', 'aspnet', 'backup', 'console', 'david', 'guest', 'john', 'owner', 'root', 'server', 'sql',
                               'support', 'support_388945a0', 'sys', 'test2', 'test3', 'user4', 'user5'. <br><br> **Minimum-length (Linux):** 1  character
                               <br><br> **Max-length (Linux):** 64 characters <br><br> **Max-length (Windows):** 20 characters  <br><br><li> For root
                               access to the Linux VM, see [Using root privileges on Linux virtual machines in
                               Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-use-root-privileges?toc=%2fazure%2fvirtual-ma
                              chines%2flinux%2ftoc.json)<br><li> For a list of built-in system users on Linux that should not be used in this field, see
                               [Selecting User Names for Linux on
                               Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-usernames?toc=%2fazure%2fvirtual-machines%2fl
                              inux%2ftoc.json)"
                    admin_password:
                        description:
                            - "Specifies the password of the administrator account. <br><br> **Minimum-length (Windows):** 8 characters <br><br>
                               **Minimum-length (Linux):** 6 characters <br><br> **Max-length (Windows):** 123 characters <br><br> **Max-length (Linux):**
                               72 characters <br><br> **Complexity requirements:** 3 out of 4 conditions below need to be fulfilled <br> Has lower
                               characters <br>Has upper characters <br> Has a digit <br> Has a special character (Regex match [\W_]) <br><br> **Disallowed
                               values:** 'abc@123', 'P@$$w0rd', 'P@ssw0rd', 'P@ssword123', 'Pa$$word', 'pass@word1', 'Password!', 'Password1',
                               'Password22', 'iloveyou!' <br><br> For resetting the password, see [How to reset the Remote Desktop service or its login
                               password in a Windows
                               VM](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-reset-rdp?toc=%2fazure%2fvirtual-machines%2fwi
                              ndows%2ftoc.json) <br><br> For resetting root password, see [Manage users, SSH, and check or repair disks on Azure Linux VMs
                               using the VMAccess
                               Extension](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-using-vmaccess-extension?toc=%2fazure%2fv
                              irtual-machines%2flinux%2ftoc.json#reset-root-password)"
                    custom_data:
                        description:
                            - "Specifies a base-64 encoded string of custom data. The base-64 encoded string is decoded to a binary array that is saved as a
                               file on the Virtual Machine. The maximum length of the binary array is 65535 bytes. <br><br> For using cloud-init for your
                               VM, see [Using cloud-init to customize a Linux VM during
                               creation](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-using-cloud-init?toc=%2fazure%2fvirtual-ma
                              chines%2flinux%2ftoc.json)"
                    windows_configuration:
                        description:
                            - Specifies Windows operating system settings on the virtual machine.
                        suboptions:
                            provision_vm_agent:
                                description:
                                    - "Indicates whether virtual machine agent should be provisioned on the virtual machine. <br><br> When this property is
                                       not specified in the request body, default behavior is to set it to true.  This will ensure that VM Agent is
                                       installed on the VM so that extensions can be added to the VM later."
                            enable_automatic_updates:
                                description:
                                    - Indicates whether virtual machine is enabled for automatic updates.
                            time_zone:
                                description:
                                    - "Specifies the time zone of the virtual machine. e.g. 'Pacific Standard Time'"
                            additional_unattend_content:
                                description:
                                    - "Specifies additional base-64 encoded XML formatted information that can be included in the Unattend.xml file, which
                                       is used by Windows Setup."
                                type: list
                                suboptions:
                                    pass_name:
                                        description:
                                            - The pass name. Currently, the only allowable value is C(oobe_system).
                                        choices:
                                            - 'oobe_system'
                                    component_name:
                                        description:
                                            - The component name. Currently, the only allowable value is C(microsoft-_windows-_shell-_setup).
                                        choices:
                                            - 'microsoft-_windows-_shell-_setup'
                                    setting_name:
                                        description:
                                            - "Specifies the name of the setting to which the I(content) applies. Possible values are:
                                               C(first_logon_commands) and C(auto_logon)."
                                        choices:
                                            - 'auto_logon'
                                            - 'first_logon_commands'
                                    content:
                                        description:
                                            - "Specifies the XML formatted content that is added to the unattend.xml file for the specified path and
                                               component. The XML must be less than 4KB and must include the root element for the setting or feature that
                                               is being inserted."
                            win_rm:
                                description:
                                    - Specifies the Windows Remote Management listeners. This enables remote Windows PowerShell.
                                suboptions:
                                    listeners:
                                        description:
                                            - The list of Windows Remote Management listeners
                                        type: list
                    linux_configuration:
                        description:
                            - "Specifies the Linux operating system settings on the virtual machine. <br><br>For a list of supported Linux distributions,
                               see [Linux on Azure-Endorsed
                               Distributions](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-endorsed-distros?toc=%2fazure%2fvirtu
                              al-machines%2flinux%2ftoc.json) <br><br> For running non-endorsed distributions, see [Information for Non-Endorsed
                               Distributions](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-create-upload-generic?toc=%2fazure%2f
                              virtual-machines%2flinux%2ftoc.json)."
                        suboptions:
                            disable_password_authentication:
                                description:
                                    - Specifies whether password authentication should be disabled.
                            ssh:
                                description:
                                    - Specifies the ssh key configuration for a Linux OS.
                                suboptions:
                                    public_keys:
                                        description:
                                            - The list of SSH public keys used to authenticate with linux based VMs.
                                        type: list
                            provision_vm_agent:
                                description:
                                    - "Indicates whether virtual machine agent should be provisioned on the virtual machine. <br><br> When this property is
                                       not specified in the request body, default behavior is to set it to true.  This will ensure that VM Agent is
                                       installed on the VM so that extensions can be added to the VM later."
                    secrets:
                        description:
                            - Specifies set of certificates that should be installed onto the virtual machines in the scale set.
                        type: list
                        suboptions:
                            source_vault:
                                description:
                                    - The relative URL of the Key Vault containing all of the certificates in I(vault_certificates).
                                suboptions:
                                    id:
                                        description:
                                            - Resource Id
                            vault_certificates:
                                description:
                                    - The list of key vault references in I(source_vault) which contain certificates.
                                type: list
                                suboptions:
                                    certificate_url:
                                        description:
                                            - "This is the URL of a certificate that has been uploaded to Key Vault as a secret. For adding a secret to the
                                               Key Vault, see [Add a key or secret to the key
                                               vault](https://docs.microsoft.com/azure/key-vault/key-vault-get-started/#add). In this case, your
                                               certificate needs to be It is the Base64 encoding of the following JSON Object which is encoded in UTF-8:
                                               <br><br> {<br>  'data':'<Base64-encoded-certificate>',<br>  'dataType':'pfx',<br>
                                               'password':'<pfx-file-password>'<br>}"
                                    certificate_store:
                                        description:
                                            - "For Windows VMs, specifies the certificate store on the Virtual Machine to which the certificate should be
                                               added. The specified certificate store is implicitly in the LocalMachine account. <br><br>For Linux VMs, the
                                               certificate file is placed under the /var/lib/waagent directory, with the file name
                                               <UppercaseThumbprint>.crt for the X509 certificate file and <UppercaseThumbpring>.prv for private key. Both
                                               of these files are .pem formatted."
            storage_profile:
                description:
                    - Specifies the storage settings for the virtual machine disks.
                suboptions:
                    image_reference:
                        description:
                            - "Specifies information about the image to use. You can specify information about platform images, marketplace images, or
                               virtual machine images. This element is required when you want to use a platform image, marketplace image, or virtual
                               machine image, but is not used in other creation operations."
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                            publisher:
                                description:
                                    - The image publisher.
                            offer:
                                description:
                                    - Specifies the offer of the platform image or marketplace image used to create the virtual machine.
                            sku:
                                description:
                                    - The image SKU.
                            version:
                                description:
                                    - "Specifies the version of the platform image or marketplace image used to create the virtual machine. The allowed
                                       formats are Major.Minor.Build or 'latest'. Major, Minor, and Build are decimal numbers. Specify 'latest' to use the
                                       latest version of an image available at deploy time. Even if you use 'latest', the VM image will not automatically
                                       update after deploy time even if a new version becomes available."
                    os_disk:
                        description:
                            - "Specifies information about the operating system disk used by the virtual machines in the scale set. <br><br> For more
                               information about disks, see [About disks and VHDs for Azure virtual
                               machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-about-disks-vhds?toc=%2fazure%2fvirtual-
                              machines%2fwindows%2ftoc.json)."
                        suboptions:
                            name:
                                description:
                                    - The disk name.
                            caching:
                                description:
                                    - "Specifies the caching requirements. <br><br> Possible values are: <br><br> **C(none)** <br><br> **C(read_only)**
                                       <br><br> **C(read_write)** <br><br> Default: **C(none) for Standard storage. C(read_only) for Premium storage**."
                                choices:
                                    - 'none'
                                    - 'read_only'
                                    - 'read_write'
                            write_accelerator_enabled:
                                description:
                                    - Specifies whether writeAccelerator should be enabled or disabled on the disk.
                            create_option:
                                description:
                                    - "Specifies how the virtual machines in the scale set should be created.<br><br> The only allowed value is:
                                       **C(from_image)** \u2013 This value is used when you are using an I(image) to create the virtual machine. If you are
                                       using a platform I(image), you also use the imageReference element described above. If you are using a marketplace
                                       I(image), you  also use the plan element previously described."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'from_image'
                                    - 'empty'
                                    - 'attach'
                            diff_disk_settings:
                                description:
                                    - Specifies the differencing Disk Settings for the operating system disk used by the virtual machine scale set.
                                suboptions:
                                    option:
                                        description:
                                            - Specifies the differencing disk settings for operating system disk.
                                        choices:
                                            - 'local'
                            disk_size_gb:
                                description:
                                    - "Specifies the size of the operating system disk in gigabytes. This element can be used to overwrite the size of the
                                       disk in a virtual machine I(image). <br><br> This value cannot be larger than 1023 GB"
                            os_type:
                                description:
                                    - "This property allows you to specify the type of the OS that is included in the disk if creating a VM from
                                       user-I(image) or a specialized VHD. <br><br> Possible values are: <br><br> **C(windows)** <br><br> **C(linux)**."
                                choices:
                                    - 'windows'
                                    - 'linux'
                            image:
                                description:
                                    - Specifies information about the unmanaged user image to base the scale set on.
                                suboptions:
                                    uri:
                                        description:
                                            - "Specifies the virtual hard disk's uri."
                            vhd_containers:
                                description:
                                    - Specifies the container urls that are used to store operating system disks for the scale set.
                                type: list
                            managed_disk:
                                description:
                                    - The managed disk parameters.
                                suboptions:
                                    storage_account_type:
                                        description:
                                            - "Specifies the storage account type for the managed disk. NOTE: C(ultra_ssd_lrs) can only be used with data
                                               disks, it cannot be used with OS Disk."
                                        choices:
                                            - 'standard_lrs'
                                            - 'premium_lrs'
                                            - 'standard_ssd_lrs'
                                            - 'ultra_ssd_lrs'
                    data_disks:
                        description:
                            - "Specifies the parameters that are used to add data disks to the virtual machines in the scale set. <br><br> For more
                               information about disks, see [About disks and VHDs for Azure virtual
                               machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-about-disks-vhds?toc=%2fazure%2fvirtual-
                              machines%2fwindows%2ftoc.json)."
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The disk name.
                            lun:
                                description:
                                    - "Specifies the logical unit number of the data disk. This value is used to identify data disks within the VM and
                                       therefore must be unique for each data disk attached to a VM."
                                    - Required when C(state) is I(present).
                            caching:
                                description:
                                    - "Specifies the caching requirements. <br><br> Possible values are: <br><br> **C(none)** <br><br> **C(read_only)**
                                       <br><br> **C(read_write)** <br><br> Default: **C(none) for Standard storage. C(read_only) for Premium storage**."
                                choices:
                                    - 'none'
                                    - 'read_only'
                                    - 'read_write'
                            write_accelerator_enabled:
                                description:
                                    - Specifies whether writeAccelerator should be enabled or disabled on the disk.
                            create_option:
                                description:
                                    - The create option.
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'from_image'
                                    - 'empty'
                                    - 'attach'
                            disk_size_gb:
                                description:
                                    - "Specifies the size of an C(empty) data disk in gigabytes. This element can be used to overwrite the size of the disk
                                       in a virtual machine image. <br><br> This value cannot be larger than 1023 GB"
                            managed_disk:
                                description:
                                    - The managed disk parameters.
                                suboptions:
                                    storage_account_type:
                                        description:
                                            - "Specifies the storage account type for the managed disk. NOTE: C(ultra_ssd_lrs) can only be used with data
                                               disks, it cannot be used with OS Disk."
                                        choices:
                                            - 'standard_lrs'
                                            - 'premium_lrs'
                                            - 'standard_ssd_lrs'
                                            - 'ultra_ssd_lrs'
            additional_capabilities:
                description:
                    - "Specifies additional capabilities enabled or disabled on the virtual machine in the scale set. For instance: whether the virtual
                       machine has the capability to support attaching managed data disks with UltraSSD_LRS storage account type."
                suboptions:
                    ultra_ssd_enabled:
                        description:
                            - "The flag that enables or disables a capability to have one or more managed data disks with UltraSSD_LRS storage account type
                               on the VM or VMSS. Managed disks with storage account type UltraSSD_LRS can be added to a virtual machine or virtual machine
                               scale set only if this property is enabled."
            network_profile:
                description:
                    - Specifies properties of the network interfaces of the virtual machines in the scale set.
                suboptions:
                    health_probe:
                        description:
                            - "A reference to a load balancer probe used to determine the health of an instance in the virtual machine scale set. The
                               reference will be in the form:
                               '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/loadBalancers/{loadBalancerNa
                              me}/probes/{probeName}'."
                        suboptions:
                            id:
                                description:
                                    - The ARM resource id in the form of /subscriptions/{SubcriptionId}/resourceGroups/{ResourceGroupName}/...
                    network_interface_configurations:
                        description:
                            - The list of network configurations.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                            name:
                                description:
                                    - The network configuration name.
                                    - Required when C(state) is I(present).
                            primary:
                                description:
                                    - Specifies the primary network interface in case the virtual machine has more than 1 network interface.
                            enable_accelerated_networking:
                                description:
                                    - Specifies whether the network interface is accelerated networking-enabled.
                            network_security_group:
                                description:
                                    - The network security group.
                                suboptions:
                                    id:
                                        description:
                                            - Resource Id
                            dns_settings:
                                description:
                                    - The dns settings to be applied on the network interfaces.
                                suboptions:
                                    dns_servers:
                                        description:
                                            - List of DNS servers IP addresses
                                        type: list
                            ip_configurations:
                                description:
                                    - Specifies the IP configurations of the network interface.
                                    - Required when C(state) is I(present).
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource Id
                                    name:
                                        description:
                                            - The IP configuration name.
                                            - Required when C(state) is I(present).
                                    subnet:
                                        description:
                                            - Specifies the identifier of the subnet.
                                    primary:
                                        description:
                                            - Specifies the primary network interface in case the virtual machine has more than 1 network interface.
                                    public_ip_address_configuration:
                                        description:
                                            - The publicIPAddressConfiguration.
                                    private_ip_address_version:
                                        description:
                                            - "Available from Api-Version 2017-03-30 onwards, it represents whether the specific ipconfiguration is C(ipv4)
                                               or C(ipv6). Default is taken as C(ipv4).  Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                                        choices:
                                            - 'ipv4'
                                            - 'ipv6'
                                    application_gateway_backend_address_pools:
                                        description:
                                            - "Specifies an array of references to backend address pools of application gateways. A scale set can reference
                                               backend address pools of multiple application gateways. Multiple scale sets cannot use the same application
                                               gateway."
                                        type: list
                                    application_security_groups:
                                        description:
                                            - Specifies an array of references to application security group.
                                        type: list
                                    load_balancer_backend_address_pools:
                                        description:
                                            - "Specifies an array of references to backend address pools of load balancers. A scale set can reference
                                               backend address pools of one public and one internal load balancer. Multiple scale sets cannot use the same
                                               load balancer."
                                        type: list
                                    load_balancer_inbound_nat_pools:
                                        description:
                                            - "Specifies an array of references to inbound Nat pools of the load balancers. A scale set can reference
                                               inbound nat pools of one public and one internal load balancer. Multiple scale sets cannot use the same load
                                               balancer"
                                        type: list
                            enable_ip_forwarding:
                                description:
                                    - Whether IP forwarding enabled on this NIC.
            diagnostics_profile:
                description:
                    - "Specifies the boot diagnostic settings state. <br><br>Minimum api-version: 2015-06-15."
                suboptions:
                    boot_diagnostics:
                        description:
                            - "Boot Diagnostics is a debugging feature which allows you to view Console Output and Screenshot to diagnose VM status.
                               <br><br> You can easily view the output of your console log. <br><br> Azure also enables you to see a screenshot of the VM
                               from the hypervisor."
                        suboptions:
                            enabled:
                                description:
                                    - Whether boot diagnostics should be enabled on the Virtual Machine.
                            storage_uri:
                                description:
                                    - Uri of the storage account to use for placing the console output and screenshot.
            extension_profile:
                description:
                    - Specifies a collection of settings for extensions installed on virtual machines in the scale set.
                suboptions:
                    extensions:
                        description:
                            - The virtual machine scale set child extension resources.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The name of the extension.
                            force_update_tag:
                                description:
                                    - "If a value is provided and is different from the previous value, the extension handler will be forced to update even
                                       if the extension configuration has not changed."
                            publisher:
                                description:
                                    - The name of the extension handler publisher.
                            type:
                                description:
                                    - "Specifies the type of the extension; an example is 'CustomScriptExtension'."
                            type_handler_version:
                                description:
                                    - Specifies the version of the script handler.
                            auto_upgrade_minor_version:
                                description:
                                    - "Indicates whether the extension should use a newer minor version if one is available at deployment time. Once
                                       deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to
                                       true."
                            settings:
                                description:
                                    - Json formatted public settings for the extension.
                            protected_settings:
                                description:
                                    - The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected I(settings) at all.
            license_type:
                description:
                    - "Specifies that the image or disk that is being used was licensed on-premises. This element is only used for images that contain the
                       Windows Server operating system. <br><br> Possible values are: <br><br> Windows_Client <br><br> Windows_Server <br><br> If this
                       element is included in a request for an update, the value must match the initial value. This value cannot be updated. <br><br> For
                       more information, see [Azure Hybrid Use Benefit for Windows
                       Server](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-hybrid-use-benefit-licensing?toc=%2fazure%2fvirtua
                      l-machines%2fwindows%2ftoc.json) <br><br> Minimum api-version: 2015-06-15"
            priority:
                description:
                    - "Specifies the priority for the virtual machines in the scale set. <br><br>Minimum api-version: 2017-10-30-preview."
                choices:
                    - 'regular'
                    - 'low'
            eviction_policy:
                description:
                    - "Specifies the eviction policy for virtual machines in a C(low) I(priority) scale set. <br><br>Minimum api-version:
                       2017-10-30-preview."
                choices:
                    - 'deallocate'
                    - 'delete'
    overprovision:
        description:
            - Specifies whether the Virtual Machine Scale Set should be overprovisioned.
    single_placement_group:
        description:
            - When true this limits the scale set to a single placement group, of max size 100 virtual machines.
    zone_balance:
        description:
            - Whether to force stictly even Virtual Machine distribution cross x-I(zones) in case there is zone outage.
    platform_fault_domain_count:
        description:
            - Fault Domain count for each placement group.
    identity:
        description:
            - The identity of the virtual machine scale set, if configured.
        suboptions:
            type:
                description:
                    - "The type of identity used for the virtual machine scale set. The type 'C(system_assigned), C(user_assigned)' includes both an
                       implicitly created identity and a set of user assigned identities. The type 'C(none)' will remove any identities from the virtual
                       machine scale set."
                choices:
                    - 'system_assigned'
                    - 'user_assigned'
                    - 'system_assigned, _user_assigned'
                    - 'none'
            user_assigned_identities:
                description:
                    - "The list of user identities associated with the virtual machine scale set. The user identity dictionary key references will be ARM
                       resource ids in the form:
                       '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{ident
                      ityName}'."
    zones:
        description:
            - The virtual machine scale set zones.
        type: list
    state:
      description:
        - Assert the state of the Virtual Machine Scale Set.
        - Use 'present' to create or update an Virtual Machine Scale Set and 'absent' to delete it.
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
  - name: Create (or update) Virtual Machine Scale Set
    azure_rm_computevirtualmachinescaleset:
      resource_group: myResourceGroup
      name: {vmss-name}
      location: eastus
      sku:
        name: Standard_D1_v2
        tier: Standard
        capacity: 3
      upgrade_policy:
        mode: Manual
      virtual_machine_profile:
        os_profile:
          computer_name_prefix: {vmss-name}
          admin_username: {your-username}
          admin_password: {your-password}
        storage_profile:
          image_reference:
            publisher: MicrosoftWindowsServer
            offer: WindowsServer
            sku: 2016-Datacenter
            version: latest
          os_disk:
            caching: ReadWrite
            create_option: FromImage
            managed_disk:
              storage_account_type: Standard_LRS
        network_profile:
          network_interface_configurations:
            - name: {vmss-name}
              primary: True
              ip_configurations:
                - name: {vmss-name}
                  subnet: {
  "id": "/subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/{existing-virtual-network-name}/subnets/{existing-subnet-name}"
}
              enable_ip_forwarding: True
      overprovision: True
'''

RETURN = '''
id:
    description:
        - Resource Id
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
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualMachineScaleSets(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Machine Scale Set resource"""

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
            plan=dict(
                type='dict'
            ),
            upgrade_policy=dict(
                type='dict'
            ),
            virtual_machine_profile=dict(
                type='dict'
            ),
            overprovision=dict(
                type='str'
            ),
            single_placement_group=dict(
                type='str'
            ),
            zone_balance=dict(
                type='str'
            ),
            platform_fault_domain_count=dict(
                type='int'
            ),
            identity=dict(
                type='dict'
            ),
            zones=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualMachineScaleSets, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                    self.parameters["sku"] = kwargs[key]
                elif key == "plan":
                    self.parameters["plan"] = kwargs[key]
                elif key == "upgrade_policy":
                    ev = kwargs[key]
                    if 'mode' in ev:
                        if ev['mode'] == 'automatic':
                            ev['mode'] = 'Automatic'
                        elif ev['mode'] == 'manual':
                            ev['mode'] = 'Manual'
                        elif ev['mode'] == 'rolling':
                            ev['mode'] = 'Rolling'
                    self.parameters["upgrade_policy"] = ev
                elif key == "virtual_machine_profile":
                    ev = kwargs[key]
                    if 'priority' in ev:
                        if ev['priority'] == 'regular':
                            ev['priority'] = 'Regular'
                        elif ev['priority'] == 'low':
                            ev['priority'] = 'Low'
                    if 'eviction_policy' in ev:
                        if ev['eviction_policy'] == 'deallocate':
                            ev['eviction_policy'] = 'Deallocate'
                        elif ev['eviction_policy'] == 'delete':
                            ev['eviction_policy'] = 'Delete'
                    self.parameters["virtual_machine_profile"] = ev
                elif key == "overprovision":
                    self.parameters["overprovision"] = kwargs[key]
                elif key == "single_placement_group":
                    self.parameters["single_placement_group"] = kwargs[key]
                elif key == "zone_balance":
                    self.parameters["zone_balance"] = kwargs[key]
                elif key == "platform_fault_domain_count":
                    self.parameters["platform_fault_domain_count"] = kwargs[key]
                elif key == "identity":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'system_assigned':
                            ev['type'] = 'SystemAssigned'
                        elif ev['type'] == 'user_assigned':
                            ev['type'] = 'UserAssigned'
                        elif ev['type'] == 'system_assigned, _user_assigned':
                            ev['type'] = 'SystemAssigned, UserAssigned'
                        elif ev['type'] == 'none':
                            ev['type'] = 'None'
                    self.parameters["identity"] = ev
                elif key == "zones":
                    self.parameters["zones"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_virtualmachinescaleset()

        if not old_response:
            self.log("Virtual Machine Scale Set instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Machine Scale Set instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Machine Scale Set instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualmachinescaleset()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Machine Scale Set instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualmachinescaleset()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_virtualmachinescaleset():
                time.sleep(20)
        else:
            self.log("Virtual Machine Scale Set instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_virtualmachinescaleset(self):
        '''
        Creates or updates Virtual Machine Scale Set with the specified configuration.

        :return: deserialized Virtual Machine Scale Set instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Machine Scale Set instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_machine_scale_sets.create_or_update(resource_group_name=self.resource_group,
                                                                                    vm_scale_set_name=self.name,
                                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Machine Scale Set instance.')
            self.fail("Error creating the Virtual Machine Scale Set instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualmachinescaleset(self):
        '''
        Deletes specified Virtual Machine Scale Set instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Machine Scale Set instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_machine_scale_sets.delete(resource_group_name=self.resource_group,
                                                                          vm_scale_set_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Machine Scale Set instance.')
            self.fail("Error deleting the Virtual Machine Scale Set instance: {0}".format(str(e)))

        return True

    def get_virtualmachinescaleset(self):
        '''
        Gets the properties of the specified Virtual Machine Scale Set.

        :return: deserialized Virtual Machine Scale Set instance state dictionary
        '''
        self.log("Checking if the Virtual Machine Scale Set instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_machine_scale_sets.get(resource_group_name=self.resource_group,
                                                                       vm_scale_set_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Machine Scale Set instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Machine Scale Set instance.')
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


def main():
    """Main execution"""
    AzureRMVirtualMachineScaleSets()


if __name__ == '__main__':
    main()
