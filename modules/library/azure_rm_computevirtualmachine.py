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
module: azure_rm_computevirtualmachine
version_added: "2.8"
short_description: Manage Virtual Machine instance.
description:
    - Create, update and delete instance of Virtual Machine.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    vm_name:
        description:
            - The name of the virtual machine.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
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
    hardware_profile:
        description:
            - Specifies the hardware settings for the virtual machine.
        suboptions:
            vm_size:
                description:
                    - "Specifies the size of the virtual machine. For more information about virtual machine sizes, see [Sizes for virtual
                       machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-sizes?toc=%2fazure%2fvirtual-machines%2fwindows%
                      2ftoc.json). <br><br> The available VM sizes depend on region and availability set. For a list of available sizes use these APIs:
                       <br><br> [List all available virtual machine sizes in an availability
                       set](https://docs.microsoft.com/rest/api/compute/availabilitysets/listavailablesizes) <br><br> [List all available virtual machine
                       sizes in a region](https://docs.microsoft.com/rest/api/compute/virtualmachinesizes/list) <br><br> [List all available virtual
                       machine sizes for resizing](https://docs.microsoft.com/rest/api/compute/virtualmachines/listavailablesizes)."
                choices:
                    - 'basic_a0'
                    - 'basic_a1'
                    - 'basic_a2'
                    - 'basic_a3'
                    - 'basic_a4'
                    - 'standard_a0'
                    - 'standard_a1'
                    - 'standard_a2'
                    - 'standard_a3'
                    - 'standard_a4'
                    - 'standard_a5'
                    - 'standard_a6'
                    - 'standard_a7'
                    - 'standard_a8'
                    - 'standard_a9'
                    - 'standard_a10'
                    - 'standard_a11'
                    - 'standard_a1_v2'
                    - 'standard_a2_v2'
                    - 'standard_a4_v2'
                    - 'standard_a8_v2'
                    - 'standard_a2m_v2'
                    - 'standard_a4m_v2'
                    - 'standard_a8m_v2'
                    - 'standard_b1s'
                    - 'standard_b1ms'
                    - 'standard_b2s'
                    - 'standard_b2ms'
                    - 'standard_b4ms'
                    - 'standard_b8ms'
                    - 'standard_d1'
                    - 'standard_d2'
                    - 'standard_d3'
                    - 'standard_d4'
                    - 'standard_d11'
                    - 'standard_d12'
                    - 'standard_d13'
                    - 'standard_d14'
                    - 'standard_d1_v2'
                    - 'standard_d2_v2'
                    - 'standard_d3_v2'
                    - 'standard_d4_v2'
                    - 'standard_d5_v2'
                    - 'standard_d2_v3'
                    - 'standard_d4_v3'
                    - 'standard_d8_v3'
                    - 'standard_d16_v3'
                    - 'standard_d32_v3'
                    - 'standard_d64_v3'
                    - 'standard_d2s_v3'
                    - 'standard_d4s_v3'
                    - 'standard_d8s_v3'
                    - 'standard_d16s_v3'
                    - 'standard_d32s_v3'
                    - 'standard_d64s_v3'
                    - 'standard_d11_v2'
                    - 'standard_d12_v2'
                    - 'standard_d13_v2'
                    - 'standard_d14_v2'
                    - 'standard_d15_v2'
                    - 'standard_ds1'
                    - 'standard_ds2'
                    - 'standard_ds3'
                    - 'standard_ds4'
                    - 'standard_ds11'
                    - 'standard_ds12'
                    - 'standard_ds13'
                    - 'standard_ds14'
                    - 'standard_ds1_v2'
                    - 'standard_ds2_v2'
                    - 'standard_ds3_v2'
                    - 'standard_ds4_v2'
                    - 'standard_ds5_v2'
                    - 'standard_ds11_v2'
                    - 'standard_ds12_v2'
                    - 'standard_ds13_v2'
                    - 'standard_ds14_v2'
                    - 'standard_ds15_v2'
                    - 'standard_ds13-4_v2'
                    - 'standard_ds13-2_v2'
                    - 'standard_ds14-8_v2'
                    - 'standard_ds14-4_v2'
                    - 'standard_e2_v3'
                    - 'standard_e4_v3'
                    - 'standard_e8_v3'
                    - 'standard_e16_v3'
                    - 'standard_e32_v3'
                    - 'standard_e64_v3'
                    - 'standard_e2s_v3'
                    - 'standard_e4s_v3'
                    - 'standard_e8s_v3'
                    - 'standard_e16s_v3'
                    - 'standard_e32s_v3'
                    - 'standard_e64s_v3'
                    - 'standard_e32-16_v3'
                    - 'standard_e32-8s_v3'
                    - 'standard_e64-32s_v3'
                    - 'standard_e64-16s_v3'
                    - 'standard_f1'
                    - 'standard_f2'
                    - 'standard_f4'
                    - 'standard_f8'
                    - 'standard_f16'
                    - 'standard_f1s'
                    - 'standard_f2s'
                    - 'standard_f4s'
                    - 'standard_f8s'
                    - 'standard_f16s'
                    - 'standard_f2s_v2'
                    - 'standard_f4s_v2'
                    - 'standard_f8s_v2'
                    - 'standard_f16s_v2'
                    - 'standard_f32s_v2'
                    - 'standard_f64s_v2'
                    - 'standard_f72s_v2'
                    - 'standard_g1'
                    - 'standard_g2'
                    - 'standard_g3'
                    - 'standard_g4'
                    - 'standard_g5'
                    - 'standard_gs1'
                    - 'standard_gs2'
                    - 'standard_gs3'
                    - 'standard_gs4'
                    - 'standard_gs5'
                    - 'standard_gs4-8'
                    - 'standard_gs4-4'
                    - 'standard_gs5-16'
                    - 'standard_gs5-8'
                    - 'standard_h8'
                    - 'standard_h16'
                    - 'standard_h8m'
                    - 'standard_h16m'
                    - 'standard_h16r'
                    - 'standard_h16mr'
                    - 'standard_l4s'
                    - 'standard_l8s'
                    - 'standard_l16s'
                    - 'standard_l32s'
                    - 'standard_m64s'
                    - 'standard_m64ms'
                    - 'standard_m128s'
                    - 'standard_m128ms'
                    - 'standard_m64-32ms'
                    - 'standard_m64-16ms'
                    - 'standard_m128-64ms'
                    - 'standard_m128-32ms'
                    - 'standard_nc6'
                    - 'standard_nc12'
                    - 'standard_nc24'
                    - 'standard_nc24r'
                    - 'standard_nc6s_v2'
                    - 'standard_nc12s_v2'
                    - 'standard_nc24s_v2'
                    - 'standard_nc24rs_v2'
                    - 'standard_nc6s_v3'
                    - 'standard_nc12s_v3'
                    - 'standard_nc24s_v3'
                    - 'standard_nc24rs_v3'
                    - 'standard_nd6s'
                    - 'standard_nd12s'
                    - 'standard_nd24s'
                    - 'standard_nd24rs'
                    - 'standard_nv6'
                    - 'standard_nv12'
                    - 'standard_nv24'
    storage_profile:
        description:
            - Specifies the storage settings for the virtual machine disks.
        suboptions:
            image_reference:
                description:
                    - "Specifies information about the image to use. You can specify information about platform images, marketplace images, or virtual
                       machine images. This element is required when you want to use a platform image, marketplace image, or virtual machine image, but is
                       not used in other creation operations."
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
                            - "Specifies the version of the platform image or marketplace image used to create the virtual machine. The allowed formats are
                               Major.Minor.Build or 'latest'. Major, Minor, and Build are decimal numbers. Specify 'latest' to use the latest version of an
                               image available at deploy time. Even if you use 'latest', the VM image will not automatically update after deploy time even
                               if a new version becomes available."
            os_disk:
                description:
                    - "Specifies information about the operating system disk used by the virtual machine. <br><br> For more information about disks, see
                       [About disks and VHDs for Azure virtual
                       machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-about-disks-vhds?toc=%2fazure%2fvirtual-machines
                      %2fwindows%2ftoc.json)."
                suboptions:
                    os_type:
                        description:
                            - "This property allows you to specify the type of the OS that is included in the disk if creating a VM from user-I(image) or a
                               specialized I(vhd). <br><br> Possible values are: <br><br> **C(windows)** <br><br> **C(linux)**."
                        choices:
                            - 'windows'
                            - 'linux'
                    encryption_settings:
                        description:
                            - "Specifies the encryption settings for the OS Disk. <br><br> Minimum api-version: 2015-06-15"
                        suboptions:
                            disk_encryption_key:
                                description:
                                    - Specifies the location of the disk encryption key, which is a Key Vault Secret.
                                suboptions:
                                    secret_url:
                                        description:
                                            - The URL referencing a secret in a Key Vault.
                                        required: True
                                    source_vault:
                                        description:
                                            - The relative URL of the Key Vault containing the secret.
                                        required: True
                            key_encryption_key:
                                description:
                                    - Specifies the location of the key encryption key in Key Vault.
                                suboptions:
                                    key_url:
                                        description:
                                            - The URL referencing a key encryption key in Key Vault.
                                        required: True
                                    source_vault:
                                        description:
                                            - The relative URL of the Key Vault containing the key.
                                        required: True
                            enabled:
                                description:
                                    - Specifies whether disk encryption should be enabled on the virtual machine.
                    name:
                        description:
                            - The disk name.
                    vhd:
                        description:
                            - The virtual hard disk.
                        suboptions:
                            uri:
                                description:
                                    - "Specifies the virtual hard disk's uri."
                    image:
                        description:
                            - "The source user image virtual hard disk. The virtual hard disk will be copied before being attached to the virtual machine.
                               If SourceImage is provided, the destination virtual hard drive must not exist."
                        suboptions:
                            uri:
                                description:
                                    - "Specifies the virtual hard disk's uri."
                    caching:
                        description:
                            - "Specifies the caching requirements. <br><br> Possible values are: <br><br> **C(none)** <br><br> **C(read_only)** <br><br>
                               **C(read_write)** <br><br> Default: **C(none) for Standard storage. C(read_only) for Premium storage**."
                        choices:
                            - 'none'
                            - 'read_only'
                            - 'read_write'
                    write_accelerator_enabled:
                        description:
                            - Specifies whether writeAccelerator should be enabled or disabled on the disk.
                    diff_disk_settings:
                        description:
                            - Specifies the differencing Disk Settings for the operating system disk used by the virtual machine.
                        suboptions:
                            option:
                                description:
                                    - Specifies the differencing disk settings for operating system disk.
                                choices:
                                    - 'local'
                    create_option:
                        description:
                            - "Specifies how the virtual machine should be created.<br><br> Possible values are:<br><br> **C(attach)** \u2013 This value is
                               used when you are using a specialized disk to create the virtual machine.<br><br> **C(from_image)** \u2013 This value is
                               used when you are using an I(image) to create the virtual machine. If you are using a platform I(image), you also use the
                               imageReference element described above. If you are using a marketplace I(image), you  also use the plan element previously
                               described."
                        required: True
                        choices:
                            - 'from_image'
                            - 'empty'
                            - 'attach'
                    disk_size_gb:
                        description:
                            - "Specifies the size of an C(empty) data disk in gigabytes. This element can be used to overwrite the size of the disk in a
                               virtual machine I(image). <br><br> This value cannot be larger than 1023 GB"
                    managed_disk:
                        description:
                            - The managed disk parameters.
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                            storage_account_type:
                                description:
                                    - "Specifies the storage account type for the managed disk. NOTE: C(ultra_ssd_lrs) can only be used with data disks, it
                                       cannot be used with OS Disk."
                                choices:
                                    - 'standard_lrs'
                                    - 'premium_lrs'
                                    - 'standard_ssd_lrs'
                                    - 'ultra_ssd_lrs'
            data_disks:
                description:
                    - "Specifies the parameters that are used to add a data disk to a virtual machine. <br><br> For more information about disks, see [About
                       disks and VHDs for Azure virtual
                       machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-about-disks-vhds?toc=%2fazure%2fvirtual-machines
                      %2fwindows%2ftoc.json)."
                type: list
                suboptions:
                    lun:
                        description:
                            - "Specifies the logical unit number of the data disk. This value is used to identify data disks within the VM and therefore
                               must be unique for each data disk attached to a VM."
                        required: True
                    name:
                        description:
                            - The disk name.
                    vhd:
                        description:
                            - The virtual hard disk.
                        suboptions:
                            uri:
                                description:
                                    - "Specifies the virtual hard disk's uri."
                    image:
                        description:
                            - "The source user image virtual hard disk. The virtual hard disk will be copied before being attached to the virtual machine.
                               If SourceImage is provided, the destination virtual hard drive must not exist."
                        suboptions:
                            uri:
                                description:
                                    - "Specifies the virtual hard disk's uri."
                    caching:
                        description:
                            - "Specifies the caching requirements. <br><br> Possible values are: <br><br> **C(none)** <br><br> **C(read_only)** <br><br>
                               **C(read_write)** <br><br> Default: **C(none) for Standard storage. C(read_only) for Premium storage**."
                        choices:
                            - 'none'
                            - 'read_only'
                            - 'read_write'
                    write_accelerator_enabled:
                        description:
                            - Specifies whether writeAccelerator should be enabled or disabled on the disk.
                    create_option:
                        description:
                            - "Specifies how the virtual machine should be created.<br><br> Possible values are:<br><br> **C(attach)** \u2013 This value is
                               used when you are using a specialized disk to create the virtual machine.<br><br> **C(from_image)** \u2013 This value is
                               used when you are using an I(image) to create the virtual machine. If you are using a platform I(image), you also use the
                               imageReference element described above. If you are using a marketplace I(image), you  also use the plan element previously
                               described."
                        required: True
                        choices:
                            - 'from_image'
                            - 'empty'
                            - 'attach'
                    disk_size_gb:
                        description:
                            - "Specifies the size of an C(empty) data disk in gigabytes. This element can be used to overwrite the size of the disk in a
                               virtual machine I(image). <br><br> This value cannot be larger than 1023 GB"
                    managed_disk:
                        description:
                            - The managed disk parameters.
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                            storage_account_type:
                                description:
                                    - "Specifies the storage account type for the managed disk. NOTE: C(ultra_ssd_lrs) can only be used with data disks, it
                                       cannot be used with OS Disk."
                                choices:
                                    - 'standard_lrs'
                                    - 'premium_lrs'
                                    - 'standard_ssd_lrs'
                                    - 'ultra_ssd_lrs'
    additional_capabilities:
        description:
            - Specifies additional capabilities enabled or disabled on the virtual machine.
        suboptions:
            ultra_ssd_enabled:
                description:
                    - "The flag that enables or disables a capability to have one or more managed data disks with UltraSSD_LRS storage account type on the
                       VM or VMSS. Managed disks with storage account type UltraSSD_LRS can be added to a virtual machine or virtual machine scale set only
                       if this property is enabled."
    os_profile:
        description:
            - Specifies the operating system settings for the virtual machine.
        suboptions:
            computer_name:
                description:
                    - "Specifies the host OS name of the virtual machine. <br><br> **Max-length (Windows):** 15 characters <br><br> **Max-length (Linux):**
                       64 characters. <br><br> For naming conventions and restrictions see [Azure infrastructure services implementation
                       guidelines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-infrastructure-subscription-accounts-guidelines?
                      toc=%2fazure%2fvirtual-machines%2flinux%2ftoc.json#1-naming-conventions)."
            admin_username:
                description:
                    - "Specifies the name of the administrator account. <br><br> **Windows-only restriction:** Cannot end in '.' <br><br> **Disallowed
                       values:** 'administrator', 'admin', 'user', 'user1', 'test', 'user2', 'test1', 'user3', 'admin1', '1', '123', 'a', 'actuser', 'adm',
                       'admin2', 'aspnet', 'backup', 'console', 'david', 'guest', 'john', 'owner', 'root', 'server', 'sql', 'support', 'support_388945a0',
                       'sys', 'test2', 'test3', 'user4', 'user5'. <br><br> **Minimum-length (Linux):** 1  character <br><br> **Max-length (Linux):** 64
                       characters <br><br> **Max-length (Windows):** 20 characters  <br><br><li> For root access to the Linux VM, see [Using root
                       privileges on Linux virtual machines in
                       Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-use-root-privileges?toc=%2fazure%2fvirtual-machines%2
                      flinux%2ftoc.json)<br><li> For a list of built-in system users on Linux that should not be used in this field, see [Selecting User
                       Names for Linux on
                       Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-usernames?toc=%2fazure%2fvirtual-machines%2flinux%2ft
                      oc.json)"
            admin_password:
                description:
                    - "Specifies the password of the administrator account. <br><br> **Minimum-length (Windows):** 8 characters <br><br> **Minimum-length
                       (Linux):** 6 characters <br><br> **Max-length (Windows):** 123 characters <br><br> **Max-length (Linux):** 72 characters <br><br>
                       **Complexity requirements:** 3 out of 4 conditions below need to be fulfilled <br> Has lower characters <br>Has upper characters
                       <br> Has a digit <br> Has a special character (Regex match [\W_]) <br><br> **Disallowed values:** 'abc@123', 'P@$$w0rd', 'P@ssw0rd',
                       'P@ssword123', 'Pa$$word', 'pass@word1', 'Password!', 'Password1', 'Password22', 'iloveyou!' <br><br> For resetting the password,
                       see [How to reset the Remote Desktop service or its login password in a Windows
                       VM](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-reset-rdp?toc=%2fazure%2fvirtual-machines%2fwindows%2f
                      toc.json) <br><br> For resetting root password, see [Manage users, SSH, and check or repair disks on Azure Linux VMs using the
                       VMAccess
                       Extension](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-using-vmaccess-extension?toc=%2fazure%2fvirtual-m
                      achines%2flinux%2ftoc.json#reset-root-password)"
            custom_data:
                description:
                    - "Specifies a base-64 encoded string of custom data. The base-64 encoded string is decoded to a binary array that is saved as a file on
                       the Virtual Machine. The maximum length of the binary array is 65535 bytes. <br><br> For using cloud-init for your VM, see [Using
                       cloud-init to customize a Linux VM during
                       creation](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-using-cloud-init?toc=%2fazure%2fvirtual-machines%2
                      flinux%2ftoc.json)"
            windows_configuration:
                description:
                    - Specifies Windows operating system settings on the virtual machine.
                suboptions:
                    provision_vm_agent:
                        description:
                            - "Indicates whether virtual machine agent should be provisioned on the virtual machine. <br><br> When this property is not
                               specified in the request body, default behavior is to set it to true.  This will ensure that VM Agent is installed on the VM
                               so that extensions can be added to the VM later."
                    enable_automatic_updates:
                        description:
                            - Indicates whether virtual machine is enabled for automatic updates.
                    time_zone:
                        description:
                            - "Specifies the time zone of the virtual machine. e.g. 'Pacific Standard Time'"
                    additional_unattend_content:
                        description:
                            - "Specifies additional base-64 encoded XML formatted information that can be included in the Unattend.xml file, which is used
                               by Windows Setup."
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
                                    - "Specifies the name of the setting to which the I(content) applies. Possible values are: C(first_logon_commands) and
                                       C(auto_logon)."
                                choices:
                                    - 'auto_logon'
                                    - 'first_logon_commands'
                            content:
                                description:
                                    - "Specifies the XML formatted content that is added to the unattend.xml file for the specified path and component. The
                                       XML must be less than 4KB and must include the root element for the setting or feature that is being inserted."
                    win_rm:
                        description:
                            - Specifies the Windows Remote Management listeners. This enables remote Windows PowerShell.
                        suboptions:
                            listeners:
                                description:
                                    - The list of Windows Remote Management listeners
                                type: list
                                suboptions:
                                    protocol:
                                        description:
                                            - "Specifies the protocol of listener. <br><br> Possible values are: <br>**C(http)** <br><br> **C(https)**."
                                        choices:
                                            - 'http'
                                            - 'https'
                                    certificate_url:
                                        description:
                                            - "This is the URL of a certificate that has been uploaded to Key Vault as a secret. For adding a secret to the
                                               Key Vault, see [Add a key or secret to the key
                                               vault](C(https)://docs.microsoft.com/azure/key-vault/key-vault-get-started/#add). In this case, your
                                               certificate needs to be It is the Base64 encoding of the following JSON Object which is encoded in UTF-8:
                                               <br><br> {<br>  'data':'<Base64-encoded-certificate>',<br>  'dataType':'pfx',<br>
                                               'password':'<pfx-file-password>'<br>}"
            linux_configuration:
                description:
                    - "Specifies the Linux operating system settings on the virtual machine. <br><br>For a list of supported Linux distributions, see [Linux
                       on Azure-Endorsed
                       Distributions](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-endorsed-distros?toc=%2fazure%2fvirtual-machi
                      nes%2flinux%2ftoc.json) <br><br> For running non-endorsed distributions, see [Information for Non-Endorsed
                       Distributions](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-create-upload-generic?toc=%2fazure%2fvirtual-
                      machines%2flinux%2ftoc.json)."
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
                                suboptions:
                                    path:
                                        description:
                                            - "Specifies the full path on the created VM where ssh public key is stored. If the file already exists, the
                                               specified key is appended to the file. Example: /home/user/.ssh/authorized_keys"
                                    key_data:
                                        description:
                                            - "SSH public key certificate used to authenticate with the VM through ssh. The key needs to be at least
                                               2048-bit and in ssh-rsa format. <br><br> For creating ssh keys, see [Create SSH keys on Linux and Mac for
                                               Linux VMs in
                                               Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-linux-mac-create-ssh-keys?toc=%2faz
                                              ure%2fvirtual-machines%2flinux%2ftoc.json)."
                    provision_vm_agent:
                        description:
                            - "Indicates whether virtual machine agent should be provisioned on the virtual machine. <br><br> When this property is not
                               specified in the request body, default behavior is to set it to true.  This will ensure that VM Agent is installed on the VM
                               so that extensions can be added to the VM later."
            secrets:
                description:
                    - Specifies set of certificates that should be installed onto the virtual machine.
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
                                    - "This is the URL of a certificate that has been uploaded to Key Vault as a secret. For adding a secret to the Key
                                       Vault, see [Add a key or secret to the key
                                       vault](https://docs.microsoft.com/azure/key-vault/key-vault-get-started/#add). In this case, your certificate needs
                                       to be It is the Base64 encoding of the following JSON Object which is encoded in UTF-8: <br><br> {<br>
                                       'data':'<Base64-encoded-certificate>',<br>  'dataType':'pfx',<br>  'password':'<pfx-file-password>'<br>}"
                            certificate_store:
                                description:
                                    - "For Windows VMs, specifies the certificate store on the Virtual Machine to which the certificate should be added. The
                                       specified certificate store is implicitly in the LocalMachine account. <br><br>For Linux VMs, the certificate file
                                       is placed under the /var/lib/waagent directory, with the file name <UppercaseThumbprint>.crt for the X509
                                       certificate file and <UppercaseThumbpring>.prv for private key. Both of these files are .pem formatted."
            allow_extension_operations:
                description:
                    - "Specifies whether extension operations should be allowed on the virtual machine. <br><br>This may only be set to False when no
                       extensions are present on the virtual machine."
    network_profile:
        description:
            - Specifies the network interfaces of the virtual machine.
        suboptions:
            network_interfaces:
                description:
                    - Specifies the list of resource Ids for the network interfaces associated with the virtual machine.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource Id
                    primary:
                        description:
                            - Specifies the primary network interface in case the virtual machine has more than 1 network interface.
    diagnostics_profile:
        description:
            - "Specifies the boot diagnostic settings state. <br><br>Minimum api-version: 2015-06-15."
        suboptions:
            boot_diagnostics:
                description:
                    - "Boot Diagnostics is a debugging feature which allows you to view Console Output and Screenshot to diagnose VM status. <br><br> You
                       can easily view the output of your console log. <br><br> Azure also enables you to see a screenshot of the VM from the hypervisor."
                suboptions:
                    enabled:
                        description:
                            - Whether boot diagnostics should be enabled on the Virtual Machine.
                    storage_uri:
                        description:
                            - Uri of the storage account to use for placing the console output and screenshot.
    availability_set:
        description:
            - "Specifies information about the availability set that the virtual machine should be assigned to. Virtual machines specified in the same
               availability set are allocated to different nodes to maximize availability. For more information about availability sets, see [Manage the
               availability of virtual
               machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-manage-availability?toc=%2fazure%2fvirtual-machines%2fwi
              ndows%2ftoc.json). <br><br> For more information on Azure planned maintainance, see [Planned maintenance for virtual machines in
               Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-planned-maintenance?toc=%2fazure%2fvirtual-machines%2fwindo
              ws%2ftoc.json) <br><br> Currently, a VM can only be added to availability set at creation time. An existing VM cannot be added to an
               availability set."
        suboptions:
            id:
                description:
                    - Resource Id
    license_type:
        description:
            - "Specifies that the image or disk that is being used was licensed on-premises. This element is only used for images that contain the Windows
               Server operating system. <br><br> Possible values are: <br><br> Windows_Client <br><br> Windows_Server <br><br> If this element is included
               in a request for an update, the value must match the initial value. This value cannot be updated. <br><br> For more information, see [Azure
               Hybrid Use Benefit for Windows
               Server](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-hybrid-use-benefit-licensing?toc=%2fazure%2fvirtual-machin
              es%2fwindows%2ftoc.json) <br><br> Minimum api-version: 2015-06-15"
    identity:
        description:
            - The identity of the virtual machine, if configured.
        suboptions:
            type:
                description:
                    - "The type of identity used for the virtual machine. The type 'C(system_assigned), C(user_assigned)' includes both an implicitly
                       created identity and a set of user assigned identities. The type 'C(none)' will remove any identities from the virtual machine."
                choices:
                    - 'system_assigned'
                    - 'user_assigned'
                    - 'system_assigned, _user_assigned'
                    - 'none'
            user_assigned_identities:
                description:
                    - "The list of user identities associated with the Virtual Machine. The user identity dictionary key references will be ARM resource ids
                       in the form:
                       '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{ident
                      ityName}'."
    zones:
        description:
            - The virtual machine zones.
        type: list
    state:
      description:
        - Assert the state of the Virtual Machine.
        - Use 'present' to create or update an Virtual Machine and 'absent' to delete it.
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
  - name: Create (or update) Virtual Machine
    azure_rm_computevirtualmachine:
      resource_group: myResourceGroup
      vm_name: myVM
      location: eastus
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


class AzureRMVirtualMachines(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Machine resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vm_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            plan=dict(
                type='dict'
            ),
            hardware_profile=dict(
                type='dict'
            ),
            storage_profile=dict(
                type='dict'
            ),
            additional_capabilities=dict(
                type='dict'
            ),
            os_profile=dict(
                type='dict'
            ),
            network_profile=dict(
                type='dict'
            ),
            diagnostics_profile=dict(
                type='dict'
            ),
            availability_set=dict(
                type='dict'
            ),
            license_type=dict(
                type='str'
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
        self.vm_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualMachines, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "plan":
                    self.parameters["plan"] = kwargs[key]
                elif key == "hardware_profile":
                    ev = kwargs[key]
                    if 'vm_size' in ev:
                        if ev['vm_size'] == 'basic_a0':
                            ev['vm_size'] = 'Basic_A0'
                        elif ev['vm_size'] == 'basic_a1':
                            ev['vm_size'] = 'Basic_A1'
                        elif ev['vm_size'] == 'basic_a2':
                            ev['vm_size'] = 'Basic_A2'
                        elif ev['vm_size'] == 'basic_a3':
                            ev['vm_size'] = 'Basic_A3'
                        elif ev['vm_size'] == 'basic_a4':
                            ev['vm_size'] = 'Basic_A4'
                        elif ev['vm_size'] == 'standard_a0':
                            ev['vm_size'] = 'Standard_A0'
                        elif ev['vm_size'] == 'standard_a1':
                            ev['vm_size'] = 'Standard_A1'
                        elif ev['vm_size'] == 'standard_a2':
                            ev['vm_size'] = 'Standard_A2'
                        elif ev['vm_size'] == 'standard_a3':
                            ev['vm_size'] = 'Standard_A3'
                        elif ev['vm_size'] == 'standard_a4':
                            ev['vm_size'] = 'Standard_A4'
                        elif ev['vm_size'] == 'standard_a5':
                            ev['vm_size'] = 'Standard_A5'
                        elif ev['vm_size'] == 'standard_a6':
                            ev['vm_size'] = 'Standard_A6'
                        elif ev['vm_size'] == 'standard_a7':
                            ev['vm_size'] = 'Standard_A7'
                        elif ev['vm_size'] == 'standard_a8':
                            ev['vm_size'] = 'Standard_A8'
                        elif ev['vm_size'] == 'standard_a9':
                            ev['vm_size'] = 'Standard_A9'
                        elif ev['vm_size'] == 'standard_a10':
                            ev['vm_size'] = 'Standard_A10'
                        elif ev['vm_size'] == 'standard_a11':
                            ev['vm_size'] = 'Standard_A11'
                        elif ev['vm_size'] == 'standard_a1_v2':
                            ev['vm_size'] = 'Standard_A1_v2'
                        elif ev['vm_size'] == 'standard_a2_v2':
                            ev['vm_size'] = 'Standard_A2_v2'
                        elif ev['vm_size'] == 'standard_a4_v2':
                            ev['vm_size'] = 'Standard_A4_v2'
                        elif ev['vm_size'] == 'standard_a8_v2':
                            ev['vm_size'] = 'Standard_A8_v2'
                        elif ev['vm_size'] == 'standard_a2m_v2':
                            ev['vm_size'] = 'Standard_A2m_v2'
                        elif ev['vm_size'] == 'standard_a4m_v2':
                            ev['vm_size'] = 'Standard_A4m_v2'
                        elif ev['vm_size'] == 'standard_a8m_v2':
                            ev['vm_size'] = 'Standard_A8m_v2'
                        elif ev['vm_size'] == 'standard_b1s':
                            ev['vm_size'] = 'Standard_B1s'
                        elif ev['vm_size'] == 'standard_b1ms':
                            ev['vm_size'] = 'Standard_B1ms'
                        elif ev['vm_size'] == 'standard_b2s':
                            ev['vm_size'] = 'Standard_B2s'
                        elif ev['vm_size'] == 'standard_b2ms':
                            ev['vm_size'] = 'Standard_B2ms'
                        elif ev['vm_size'] == 'standard_b4ms':
                            ev['vm_size'] = 'Standard_B4ms'
                        elif ev['vm_size'] == 'standard_b8ms':
                            ev['vm_size'] = 'Standard_B8ms'
                        elif ev['vm_size'] == 'standard_d1':
                            ev['vm_size'] = 'Standard_D1'
                        elif ev['vm_size'] == 'standard_d2':
                            ev['vm_size'] = 'Standard_D2'
                        elif ev['vm_size'] == 'standard_d3':
                            ev['vm_size'] = 'Standard_D3'
                        elif ev['vm_size'] == 'standard_d4':
                            ev['vm_size'] = 'Standard_D4'
                        elif ev['vm_size'] == 'standard_d11':
                            ev['vm_size'] = 'Standard_D11'
                        elif ev['vm_size'] == 'standard_d12':
                            ev['vm_size'] = 'Standard_D12'
                        elif ev['vm_size'] == 'standard_d13':
                            ev['vm_size'] = 'Standard_D13'
                        elif ev['vm_size'] == 'standard_d14':
                            ev['vm_size'] = 'Standard_D14'
                        elif ev['vm_size'] == 'standard_d1_v2':
                            ev['vm_size'] = 'Standard_D1_v2'
                        elif ev['vm_size'] == 'standard_d2_v2':
                            ev['vm_size'] = 'Standard_D2_v2'
                        elif ev['vm_size'] == 'standard_d3_v2':
                            ev['vm_size'] = 'Standard_D3_v2'
                        elif ev['vm_size'] == 'standard_d4_v2':
                            ev['vm_size'] = 'Standard_D4_v2'
                        elif ev['vm_size'] == 'standard_d5_v2':
                            ev['vm_size'] = 'Standard_D5_v2'
                        elif ev['vm_size'] == 'standard_d2_v3':
                            ev['vm_size'] = 'Standard_D2_v3'
                        elif ev['vm_size'] == 'standard_d4_v3':
                            ev['vm_size'] = 'Standard_D4_v3'
                        elif ev['vm_size'] == 'standard_d8_v3':
                            ev['vm_size'] = 'Standard_D8_v3'
                        elif ev['vm_size'] == 'standard_d16_v3':
                            ev['vm_size'] = 'Standard_D16_v3'
                        elif ev['vm_size'] == 'standard_d32_v3':
                            ev['vm_size'] = 'Standard_D32_v3'
                        elif ev['vm_size'] == 'standard_d64_v3':
                            ev['vm_size'] = 'Standard_D64_v3'
                        elif ev['vm_size'] == 'standard_d2s_v3':
                            ev['vm_size'] = 'Standard_D2s_v3'
                        elif ev['vm_size'] == 'standard_d4s_v3':
                            ev['vm_size'] = 'Standard_D4s_v3'
                        elif ev['vm_size'] == 'standard_d8s_v3':
                            ev['vm_size'] = 'Standard_D8s_v3'
                        elif ev['vm_size'] == 'standard_d16s_v3':
                            ev['vm_size'] = 'Standard_D16s_v3'
                        elif ev['vm_size'] == 'standard_d32s_v3':
                            ev['vm_size'] = 'Standard_D32s_v3'
                        elif ev['vm_size'] == 'standard_d64s_v3':
                            ev['vm_size'] = 'Standard_D64s_v3'
                        elif ev['vm_size'] == 'standard_d11_v2':
                            ev['vm_size'] = 'Standard_D11_v2'
                        elif ev['vm_size'] == 'standard_d12_v2':
                            ev['vm_size'] = 'Standard_D12_v2'
                        elif ev['vm_size'] == 'standard_d13_v2':
                            ev['vm_size'] = 'Standard_D13_v2'
                        elif ev['vm_size'] == 'standard_d14_v2':
                            ev['vm_size'] = 'Standard_D14_v2'
                        elif ev['vm_size'] == 'standard_d15_v2':
                            ev['vm_size'] = 'Standard_D15_v2'
                        elif ev['vm_size'] == 'standard_ds1':
                            ev['vm_size'] = 'Standard_DS1'
                        elif ev['vm_size'] == 'standard_ds2':
                            ev['vm_size'] = 'Standard_DS2'
                        elif ev['vm_size'] == 'standard_ds3':
                            ev['vm_size'] = 'Standard_DS3'
                        elif ev['vm_size'] == 'standard_ds4':
                            ev['vm_size'] = 'Standard_DS4'
                        elif ev['vm_size'] == 'standard_ds11':
                            ev['vm_size'] = 'Standard_DS11'
                        elif ev['vm_size'] == 'standard_ds12':
                            ev['vm_size'] = 'Standard_DS12'
                        elif ev['vm_size'] == 'standard_ds13':
                            ev['vm_size'] = 'Standard_DS13'
                        elif ev['vm_size'] == 'standard_ds14':
                            ev['vm_size'] = 'Standard_DS14'
                        elif ev['vm_size'] == 'standard_ds1_v2':
                            ev['vm_size'] = 'Standard_DS1_v2'
                        elif ev['vm_size'] == 'standard_ds2_v2':
                            ev['vm_size'] = 'Standard_DS2_v2'
                        elif ev['vm_size'] == 'standard_ds3_v2':
                            ev['vm_size'] = 'Standard_DS3_v2'
                        elif ev['vm_size'] == 'standard_ds4_v2':
                            ev['vm_size'] = 'Standard_DS4_v2'
                        elif ev['vm_size'] == 'standard_ds5_v2':
                            ev['vm_size'] = 'Standard_DS5_v2'
                        elif ev['vm_size'] == 'standard_ds11_v2':
                            ev['vm_size'] = 'Standard_DS11_v2'
                        elif ev['vm_size'] == 'standard_ds12_v2':
                            ev['vm_size'] = 'Standard_DS12_v2'
                        elif ev['vm_size'] == 'standard_ds13_v2':
                            ev['vm_size'] = 'Standard_DS13_v2'
                        elif ev['vm_size'] == 'standard_ds14_v2':
                            ev['vm_size'] = 'Standard_DS14_v2'
                        elif ev['vm_size'] == 'standard_ds15_v2':
                            ev['vm_size'] = 'Standard_DS15_v2'
                        elif ev['vm_size'] == 'standard_ds13-4_v2':
                            ev['vm_size'] = 'Standard_DS13-4_v2'
                        elif ev['vm_size'] == 'standard_ds13-2_v2':
                            ev['vm_size'] = 'Standard_DS13-2_v2'
                        elif ev['vm_size'] == 'standard_ds14-8_v2':
                            ev['vm_size'] = 'Standard_DS14-8_v2'
                        elif ev['vm_size'] == 'standard_ds14-4_v2':
                            ev['vm_size'] = 'Standard_DS14-4_v2'
                        elif ev['vm_size'] == 'standard_e2_v3':
                            ev['vm_size'] = 'Standard_E2_v3'
                        elif ev['vm_size'] == 'standard_e4_v3':
                            ev['vm_size'] = 'Standard_E4_v3'
                        elif ev['vm_size'] == 'standard_e8_v3':
                            ev['vm_size'] = 'Standard_E8_v3'
                        elif ev['vm_size'] == 'standard_e16_v3':
                            ev['vm_size'] = 'Standard_E16_v3'
                        elif ev['vm_size'] == 'standard_e32_v3':
                            ev['vm_size'] = 'Standard_E32_v3'
                        elif ev['vm_size'] == 'standard_e64_v3':
                            ev['vm_size'] = 'Standard_E64_v3'
                        elif ev['vm_size'] == 'standard_e2s_v3':
                            ev['vm_size'] = 'Standard_E2s_v3'
                        elif ev['vm_size'] == 'standard_e4s_v3':
                            ev['vm_size'] = 'Standard_E4s_v3'
                        elif ev['vm_size'] == 'standard_e8s_v3':
                            ev['vm_size'] = 'Standard_E8s_v3'
                        elif ev['vm_size'] == 'standard_e16s_v3':
                            ev['vm_size'] = 'Standard_E16s_v3'
                        elif ev['vm_size'] == 'standard_e32s_v3':
                            ev['vm_size'] = 'Standard_E32s_v3'
                        elif ev['vm_size'] == 'standard_e64s_v3':
                            ev['vm_size'] = 'Standard_E64s_v3'
                        elif ev['vm_size'] == 'standard_e32-16_v3':
                            ev['vm_size'] = 'Standard_E32-16_v3'
                        elif ev['vm_size'] == 'standard_e32-8s_v3':
                            ev['vm_size'] = 'Standard_E32-8s_v3'
                        elif ev['vm_size'] == 'standard_e64-32s_v3':
                            ev['vm_size'] = 'Standard_E64-32s_v3'
                        elif ev['vm_size'] == 'standard_e64-16s_v3':
                            ev['vm_size'] = 'Standard_E64-16s_v3'
                        elif ev['vm_size'] == 'standard_f1':
                            ev['vm_size'] = 'Standard_F1'
                        elif ev['vm_size'] == 'standard_f2':
                            ev['vm_size'] = 'Standard_F2'
                        elif ev['vm_size'] == 'standard_f4':
                            ev['vm_size'] = 'Standard_F4'
                        elif ev['vm_size'] == 'standard_f8':
                            ev['vm_size'] = 'Standard_F8'
                        elif ev['vm_size'] == 'standard_f16':
                            ev['vm_size'] = 'Standard_F16'
                        elif ev['vm_size'] == 'standard_f1s':
                            ev['vm_size'] = 'Standard_F1s'
                        elif ev['vm_size'] == 'standard_f2s':
                            ev['vm_size'] = 'Standard_F2s'
                        elif ev['vm_size'] == 'standard_f4s':
                            ev['vm_size'] = 'Standard_F4s'
                        elif ev['vm_size'] == 'standard_f8s':
                            ev['vm_size'] = 'Standard_F8s'
                        elif ev['vm_size'] == 'standard_f16s':
                            ev['vm_size'] = 'Standard_F16s'
                        elif ev['vm_size'] == 'standard_f2s_v2':
                            ev['vm_size'] = 'Standard_F2s_v2'
                        elif ev['vm_size'] == 'standard_f4s_v2':
                            ev['vm_size'] = 'Standard_F4s_v2'
                        elif ev['vm_size'] == 'standard_f8s_v2':
                            ev['vm_size'] = 'Standard_F8s_v2'
                        elif ev['vm_size'] == 'standard_f16s_v2':
                            ev['vm_size'] = 'Standard_F16s_v2'
                        elif ev['vm_size'] == 'standard_f32s_v2':
                            ev['vm_size'] = 'Standard_F32s_v2'
                        elif ev['vm_size'] == 'standard_f64s_v2':
                            ev['vm_size'] = 'Standard_F64s_v2'
                        elif ev['vm_size'] == 'standard_f72s_v2':
                            ev['vm_size'] = 'Standard_F72s_v2'
                        elif ev['vm_size'] == 'standard_g1':
                            ev['vm_size'] = 'Standard_G1'
                        elif ev['vm_size'] == 'standard_g2':
                            ev['vm_size'] = 'Standard_G2'
                        elif ev['vm_size'] == 'standard_g3':
                            ev['vm_size'] = 'Standard_G3'
                        elif ev['vm_size'] == 'standard_g4':
                            ev['vm_size'] = 'Standard_G4'
                        elif ev['vm_size'] == 'standard_g5':
                            ev['vm_size'] = 'Standard_G5'
                        elif ev['vm_size'] == 'standard_gs1':
                            ev['vm_size'] = 'Standard_GS1'
                        elif ev['vm_size'] == 'standard_gs2':
                            ev['vm_size'] = 'Standard_GS2'
                        elif ev['vm_size'] == 'standard_gs3':
                            ev['vm_size'] = 'Standard_GS3'
                        elif ev['vm_size'] == 'standard_gs4':
                            ev['vm_size'] = 'Standard_GS4'
                        elif ev['vm_size'] == 'standard_gs5':
                            ev['vm_size'] = 'Standard_GS5'
                        elif ev['vm_size'] == 'standard_gs4-8':
                            ev['vm_size'] = 'Standard_GS4-8'
                        elif ev['vm_size'] == 'standard_gs4-4':
                            ev['vm_size'] = 'Standard_GS4-4'
                        elif ev['vm_size'] == 'standard_gs5-16':
                            ev['vm_size'] = 'Standard_GS5-16'
                        elif ev['vm_size'] == 'standard_gs5-8':
                            ev['vm_size'] = 'Standard_GS5-8'
                        elif ev['vm_size'] == 'standard_h8':
                            ev['vm_size'] = 'Standard_H8'
                        elif ev['vm_size'] == 'standard_h16':
                            ev['vm_size'] = 'Standard_H16'
                        elif ev['vm_size'] == 'standard_h8m':
                            ev['vm_size'] = 'Standard_H8m'
                        elif ev['vm_size'] == 'standard_h16m':
                            ev['vm_size'] = 'Standard_H16m'
                        elif ev['vm_size'] == 'standard_h16r':
                            ev['vm_size'] = 'Standard_H16r'
                        elif ev['vm_size'] == 'standard_h16mr':
                            ev['vm_size'] = 'Standard_H16mr'
                        elif ev['vm_size'] == 'standard_l4s':
                            ev['vm_size'] = 'Standard_L4s'
                        elif ev['vm_size'] == 'standard_l8s':
                            ev['vm_size'] = 'Standard_L8s'
                        elif ev['vm_size'] == 'standard_l16s':
                            ev['vm_size'] = 'Standard_L16s'
                        elif ev['vm_size'] == 'standard_l32s':
                            ev['vm_size'] = 'Standard_L32s'
                        elif ev['vm_size'] == 'standard_m64s':
                            ev['vm_size'] = 'Standard_M64s'
                        elif ev['vm_size'] == 'standard_m64ms':
                            ev['vm_size'] = 'Standard_M64ms'
                        elif ev['vm_size'] == 'standard_m128s':
                            ev['vm_size'] = 'Standard_M128s'
                        elif ev['vm_size'] == 'standard_m128ms':
                            ev['vm_size'] = 'Standard_M128ms'
                        elif ev['vm_size'] == 'standard_m64-32ms':
                            ev['vm_size'] = 'Standard_M64-32ms'
                        elif ev['vm_size'] == 'standard_m64-16ms':
                            ev['vm_size'] = 'Standard_M64-16ms'
                        elif ev['vm_size'] == 'standard_m128-64ms':
                            ev['vm_size'] = 'Standard_M128-64ms'
                        elif ev['vm_size'] == 'standard_m128-32ms':
                            ev['vm_size'] = 'Standard_M128-32ms'
                        elif ev['vm_size'] == 'standard_nc6':
                            ev['vm_size'] = 'Standard_NC6'
                        elif ev['vm_size'] == 'standard_nc12':
                            ev['vm_size'] = 'Standard_NC12'
                        elif ev['vm_size'] == 'standard_nc24':
                            ev['vm_size'] = 'Standard_NC24'
                        elif ev['vm_size'] == 'standard_nc24r':
                            ev['vm_size'] = 'Standard_NC24r'
                        elif ev['vm_size'] == 'standard_nc6s_v2':
                            ev['vm_size'] = 'Standard_NC6s_v2'
                        elif ev['vm_size'] == 'standard_nc12s_v2':
                            ev['vm_size'] = 'Standard_NC12s_v2'
                        elif ev['vm_size'] == 'standard_nc24s_v2':
                            ev['vm_size'] = 'Standard_NC24s_v2'
                        elif ev['vm_size'] == 'standard_nc24rs_v2':
                            ev['vm_size'] = 'Standard_NC24rs_v2'
                        elif ev['vm_size'] == 'standard_nc6s_v3':
                            ev['vm_size'] = 'Standard_NC6s_v3'
                        elif ev['vm_size'] == 'standard_nc12s_v3':
                            ev['vm_size'] = 'Standard_NC12s_v3'
                        elif ev['vm_size'] == 'standard_nc24s_v3':
                            ev['vm_size'] = 'Standard_NC24s_v3'
                        elif ev['vm_size'] == 'standard_nc24rs_v3':
                            ev['vm_size'] = 'Standard_NC24rs_v3'
                        elif ev['vm_size'] == 'standard_nd6s':
                            ev['vm_size'] = 'Standard_ND6s'
                        elif ev['vm_size'] == 'standard_nd12s':
                            ev['vm_size'] = 'Standard_ND12s'
                        elif ev['vm_size'] == 'standard_nd24s':
                            ev['vm_size'] = 'Standard_ND24s'
                        elif ev['vm_size'] == 'standard_nd24rs':
                            ev['vm_size'] = 'Standard_ND24rs'
                        elif ev['vm_size'] == 'standard_nv6':
                            ev['vm_size'] = 'Standard_NV6'
                        elif ev['vm_size'] == 'standard_nv12':
                            ev['vm_size'] = 'Standard_NV12'
                        elif ev['vm_size'] == 'standard_nv24':
                            ev['vm_size'] = 'Standard_NV24'
                    self.parameters["hardware_profile"] = ev
                elif key == "storage_profile":
                    self.parameters["storage_profile"] = kwargs[key]
                elif key == "additional_capabilities":
                    self.parameters["additional_capabilities"] = kwargs[key]
                elif key == "os_profile":
                    self.parameters["os_profile"] = kwargs[key]
                elif key == "network_profile":
                    self.parameters["network_profile"] = kwargs[key]
                elif key == "diagnostics_profile":
                    self.parameters["diagnostics_profile"] = kwargs[key]
                elif key == "availability_set":
                    self.parameters["availability_set"] = kwargs[key]
                elif key == "license_type":
                    self.parameters["license_type"] = kwargs[key]
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

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_virtualmachine()

        if not old_response:
            self.log("Virtual Machine instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Machine instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Virtual Machine instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Machine instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualmachine()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Machine instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualmachine()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_virtualmachine():
                time.sleep(20)
        else:
            self.log("Virtual Machine instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_virtualmachine(self):
        '''
        Creates or updates Virtual Machine with the specified configuration.

        :return: deserialized Virtual Machine instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Machine instance {0}".format(self.vm_name))

        try:
            response = self.mgmt_client.virtual_machines.create_or_update(resource_group_name=self.resource_group,
                                                                          vm_name=self.vm_name,
                                                                          parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Machine instance.')
            self.fail("Error creating the Virtual Machine instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualmachine(self):
        '''
        Deletes specified Virtual Machine instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Machine instance {0}".format(self.vm_name))
        try:
            response = self.mgmt_client.virtual_machines.delete(resource_group_name=self.resource_group,
                                                                vm_name=self.vm_name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Machine instance.')
            self.fail("Error deleting the Virtual Machine instance: {0}".format(str(e)))

        return True

    def get_virtualmachine(self):
        '''
        Gets the properties of the specified Virtual Machine.

        :return: deserialized Virtual Machine instance state dictionary
        '''
        self.log("Checking if the Virtual Machine instance {0} is present".format(self.vm_name))
        found = False
        try:
            response = self.mgmt_client.virtual_machines.get(resource_group_name=self.resource_group,
                                                             vm_name=self.vm_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Machine instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Machine instance.')
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
    AzureRMVirtualMachines()


if __name__ == '__main__':
    main()
