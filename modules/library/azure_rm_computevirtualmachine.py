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
short_description: Manage Azure Virtual Machine instance.
description:
    - Create, update and delete instance of Azure Virtual Machine.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
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
                                            - Required when C(state) is I(present).
                                    source_vault:
                                        description:
                                            - The relative URL of the Key Vault containing the secret.
                                            - Required when C(state) is I(present).
                            key_encryption_key:
                                description:
                                    - Specifies the location of the key encryption key in Key Vault.
                                suboptions:
                                    key_url:
                                        description:
                                            - The URL referencing a key encryption key in Key Vault.
                                            - Required when C(state) is I(present).
                                    source_vault:
                                        description:
                                            - The relative URL of the Key Vault containing the key.
                                            - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
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
      name: myVM
      location: eastus
      hardware_profile:
        vm_size: Standard_D1_v2
      storage_profile:
        image_reference:
          publisher: MicrosoftWindowsServer
          offer: WindowsServer
          sku: 2016-Datacenter
          version: latest
        os_disk:
          name: myVMosdisk
          caching: ReadWrite
          create_option: FromImage
          managed_disk:
            storage_account_type: Standard_LRS
      os_profile:
        computer_name: myVM
        admin_username: {your-username}
        admin_password: {your-password}
      network_profile:
        network_interfaces:
          - id: /subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/{existing-nic-name}
            primary: True
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMVirtualMachine(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Machine resource"""

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
            plan=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    publisher=dict(
                        type='str'
                    ),
                    product=dict(
                        type='str'
                    ),
                    promotion_code=dict(
                        type='str'
                    )
                )
            ),
            hardware_profile=dict(
                type='dict',
                options=dict(
                    vm_size=dict(
                        type='str',
                        choices=['basic_a0',
                                 'basic_a1',
                                 'basic_a2',
                                 'basic_a3',
                                 'basic_a4',
                                 'standard_a0',
                                 'standard_a1',
                                 'standard_a2',
                                 'standard_a3',
                                 'standard_a4',
                                 'standard_a5',
                                 'standard_a6',
                                 'standard_a7',
                                 'standard_a8',
                                 'standard_a9',
                                 'standard_a10',
                                 'standard_a11',
                                 'standard_a1_v2',
                                 'standard_a2_v2',
                                 'standard_a4_v2',
                                 'standard_a8_v2',
                                 'standard_a2m_v2',
                                 'standard_a4m_v2',
                                 'standard_a8m_v2',
                                 'standard_b1s',
                                 'standard_b1ms',
                                 'standard_b2s',
                                 'standard_b2ms',
                                 'standard_b4ms',
                                 'standard_b8ms',
                                 'standard_d1',
                                 'standard_d2',
                                 'standard_d3',
                                 'standard_d4',
                                 'standard_d11',
                                 'standard_d12',
                                 'standard_d13',
                                 'standard_d14',
                                 'standard_d1_v2',
                                 'standard_d2_v2',
                                 'standard_d3_v2',
                                 'standard_d4_v2',
                                 'standard_d5_v2',
                                 'standard_d2_v3',
                                 'standard_d4_v3',
                                 'standard_d8_v3',
                                 'standard_d16_v3',
                                 'standard_d32_v3',
                                 'standard_d64_v3',
                                 'standard_d2s_v3',
                                 'standard_d4s_v3',
                                 'standard_d8s_v3',
                                 'standard_d16s_v3',
                                 'standard_d32s_v3',
                                 'standard_d64s_v3',
                                 'standard_d11_v2',
                                 'standard_d12_v2',
                                 'standard_d13_v2',
                                 'standard_d14_v2',
                                 'standard_d15_v2',
                                 'standard_ds1',
                                 'standard_ds2',
                                 'standard_ds3',
                                 'standard_ds4',
                                 'standard_ds11',
                                 'standard_ds12',
                                 'standard_ds13',
                                 'standard_ds14',
                                 'standard_ds1_v2',
                                 'standard_ds2_v2',
                                 'standard_ds3_v2',
                                 'standard_ds4_v2',
                                 'standard_ds5_v2',
                                 'standard_ds11_v2',
                                 'standard_ds12_v2',
                                 'standard_ds13_v2',
                                 'standard_ds14_v2',
                                 'standard_ds15_v2',
                                 'standard_ds13-4_v2',
                                 'standard_ds13-2_v2',
                                 'standard_ds14-8_v2',
                                 'standard_ds14-4_v2',
                                 'standard_e2_v3',
                                 'standard_e4_v3',
                                 'standard_e8_v3',
                                 'standard_e16_v3',
                                 'standard_e32_v3',
                                 'standard_e64_v3',
                                 'standard_e2s_v3',
                                 'standard_e4s_v3',
                                 'standard_e8s_v3',
                                 'standard_e16s_v3',
                                 'standard_e32s_v3',
                                 'standard_e64s_v3',
                                 'standard_e32-16_v3',
                                 'standard_e32-8s_v3',
                                 'standard_e64-32s_v3',
                                 'standard_e64-16s_v3',
                                 'standard_f1',
                                 'standard_f2',
                                 'standard_f4',
                                 'standard_f8',
                                 'standard_f16',
                                 'standard_f1s',
                                 'standard_f2s',
                                 'standard_f4s',
                                 'standard_f8s',
                                 'standard_f16s',
                                 'standard_f2s_v2',
                                 'standard_f4s_v2',
                                 'standard_f8s_v2',
                                 'standard_f16s_v2',
                                 'standard_f32s_v2',
                                 'standard_f64s_v2',
                                 'standard_f72s_v2',
                                 'standard_g1',
                                 'standard_g2',
                                 'standard_g3',
                                 'standard_g4',
                                 'standard_g5',
                                 'standard_gs1',
                                 'standard_gs2',
                                 'standard_gs3',
                                 'standard_gs4',
                                 'standard_gs5',
                                 'standard_gs4-8',
                                 'standard_gs4-4',
                                 'standard_gs5-16',
                                 'standard_gs5-8',
                                 'standard_h8',
                                 'standard_h16',
                                 'standard_h8m',
                                 'standard_h16m',
                                 'standard_h16r',
                                 'standard_h16mr',
                                 'standard_l4s',
                                 'standard_l8s',
                                 'standard_l16s',
                                 'standard_l32s',
                                 'standard_m64s',
                                 'standard_m64ms',
                                 'standard_m128s',
                                 'standard_m128ms',
                                 'standard_m64-32ms',
                                 'standard_m64-16ms',
                                 'standard_m128-64ms',
                                 'standard_m128-32ms',
                                 'standard_nc6',
                                 'standard_nc12',
                                 'standard_nc24',
                                 'standard_nc24r',
                                 'standard_nc6s_v2',
                                 'standard_nc12s_v2',
                                 'standard_nc24s_v2',
                                 'standard_nc24rs_v2',
                                 'standard_nc6s_v3',
                                 'standard_nc12s_v3',
                                 'standard_nc24s_v3',
                                 'standard_nc24rs_v3',
                                 'standard_nd6s',
                                 'standard_nd12s',
                                 'standard_nd24s',
                                 'standard_nd24rs',
                                 'standard_nv6',
                                 'standard_nv12',
                                 'standard_nv24']
                    )
                )
            ),
            storage_profile=dict(
                type='dict',
                options=dict(
                    image_reference=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            publisher=dict(
                                type='str'
                            ),
                            offer=dict(
                                type='str'
                            ),
                            sku=dict(
                                type='str'
                            ),
                            version=dict(
                                type='str'
                            )
                        )
                    ),
                    os_disk=dict(
                        type='dict',
                        options=dict(
                            os_type=dict(
                                type='str',
                                choices=['windows',
                                         'linux']
                            ),
                            encryption_settings=dict(
                                type='dict',
                                options=dict(
                                    disk_encryption_key=dict(
                                        type='dict',
                                        options=dict(
                                            secret_url=dict(
                                                type='str'
                                            ),
                                            source_vault=dict(
                                                type='dict'
                                            )
                                        )
                                    ),
                                    key_encryption_key=dict(
                                        type='dict',
                                        options=dict(
                                            key_url=dict(
                                                type='str'
                                            ),
                                            source_vault=dict(
                                                type='dict'
                                            )
                                        )
                                    ),
                                    enabled=dict(
                                        type='str'
                                    )
                                )
                            ),
                            name=dict(
                                type='str'
                            ),
                            vhd=dict(
                                type='dict',
                                options=dict(
                                    uri=dict(
                                        type='str'
                                    )
                                )
                            ),
                            image=dict(
                                type='dict',
                                options=dict(
                                    uri=dict(
                                        type='str'
                                    )
                                )
                            ),
                            caching=dict(
                                type='str',
                                choices=['none',
                                         'read_only',
                                         'read_write']
                            ),
                            write_accelerator_enabled=dict(
                                type='str'
                            ),
                            diff_disk_settings=dict(
                                type='dict',
                                options=dict(
                                    option=dict(
                                        type='str',
                                        choices=['local']
                                    )
                                )
                            ),
                            create_option=dict(
                                type='str',
                                choices=['from_image',
                                         'empty',
                                         'attach']
                            ),
                            disk_size_gb=dict(
                                type='int'
                            ),
                            managed_disk=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    storage_account_type=dict(
                                        type='str',
                                        choices=['standard_lrs',
                                                 'premium_lrs',
                                                 'standard_ssd_lrs',
                                                 'ultra_ssd_lrs']
                                    )
                                )
                            )
                        )
                    ),
                    data_disks=dict(
                        type='list',
                        options=dict(
                            lun=dict(
                                type='int'
                            ),
                            name=dict(
                                type='str'
                            ),
                            vhd=dict(
                                type='dict',
                                options=dict(
                                    uri=dict(
                                        type='str'
                                    )
                                )
                            ),
                            image=dict(
                                type='dict',
                                options=dict(
                                    uri=dict(
                                        type='str'
                                    )
                                )
                            ),
                            caching=dict(
                                type='str',
                                choices=['none',
                                         'read_only',
                                         'read_write']
                            ),
                            write_accelerator_enabled=dict(
                                type='str'
                            ),
                            create_option=dict(
                                type='str',
                                choices=['from_image',
                                         'empty',
                                         'attach']
                            ),
                            disk_size_gb=dict(
                                type='int'
                            ),
                            managed_disk=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    storage_account_type=dict(
                                        type='str',
                                        choices=['standard_lrs',
                                                 'premium_lrs',
                                                 'standard_ssd_lrs',
                                                 'ultra_ssd_lrs']
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            additional_capabilities=dict(
                type='dict',
                options=dict(
                    ultra_ssd_enabled=dict(
                        type='str'
                    )
                )
            ),
            os_profile=dict(
                type='dict',
                options=dict(
                    computer_name=dict(
                        type='str'
                    ),
                    admin_username=dict(
                        type='str'
                    ),
                    admin_password=dict(
                        type='str',
                        no_log=True
                    ),
                    custom_data=dict(
                        type='str'
                    ),
                    windows_configuration=dict(
                        type='dict',
                        options=dict(
                            provision_vm_agent=dict(
                                type='str'
                            ),
                            enable_automatic_updates=dict(
                                type='str'
                            ),
                            time_zone=dict(
                                type='str'
                            ),
                            additional_unattend_content=dict(
                                type='list',
                                options=dict(
                                    pass_name=dict(
                                        type='str',
                                        choices=['oobe_system']
                                    ),
                                    component_name=dict(
                                        type='str',
                                        choices=['microsoft-_windows-_shell-_setup']
                                    ),
                                    setting_name=dict(
                                        type='str',
                                        choices=['auto_logon',
                                                 'first_logon_commands']
                                    ),
                                    content=dict(
                                        type='str'
                                    )
                                )
                            ),
                            win_rm=dict(
                                type='dict',
                                options=dict(
                                    listeners=dict(
                                        type='list',
                                        options=dict(
                                            protocol=dict(
                                                type='str',
                                                choices=['http',
                                                         'https']
                                            ),
                                            certificate_url=dict(
                                                type='str'
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    linux_configuration=dict(
                        type='dict',
                        options=dict(
                            disable_password_authentication=dict(
                                type='str',
                                no_log=True
                            ),
                            ssh=dict(
                                type='dict',
                                options=dict(
                                    public_keys=dict(
                                        type='list',
                                        options=dict(
                                            path=dict(
                                                type='str'
                                            ),
                                            key_data=dict(
                                                type='str'
                                            )
                                        )
                                    )
                                )
                            ),
                            provision_vm_agent=dict(
                                type='str'
                            )
                        )
                    ),
                    secrets=dict(
                        type='list',
                        options=dict(
                            source_vault=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            vault_certificates=dict(
                                type='list',
                                options=dict(
                                    certificate_url=dict(
                                        type='str'
                                    ),
                                    certificate_store=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    allow_extension_operations=dict(
                        type='str'
                    )
                )
            ),
            network_profile=dict(
                type='dict',
                options=dict(
                    network_interfaces=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            primary=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            diagnostics_profile=dict(
                type='dict',
                options=dict(
                    boot_diagnostics=dict(
                        type='dict',
                        options=dict(
                            enabled=dict(
                                type='str'
                            ),
                            storage_uri=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            availability_set=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            license_type=dict(
                type='str'
            ),
            identity=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str',
                        choices=['system_assigned',
                                 'user_assigned',
                                 'system_assigned, _user_assigned',
                                 'none']
                    ),
                    user_assigned_identities=dict(
                        type='dict'
                    )
                )
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

        super(AzureRMVirtualMachine, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['hardware_profile', 'vm_size'], True)
        dict_map(self.parameters, ['hardware_profile', 'vm_size'], {'basic_a0': 'Basic_A0', 'basic_a1': 'Basic_A1', 'basic_a2': 'Basic_A2', 'basic_a3': 'Basic_A3', 'basic_a4': 'Basic_A4', 'standard_a0': 'Standard_A0', 'standard_a1': 'Standard_A1', 'standard_a2': 'Standard_A2', 'standard_a3': 'Standard_A3', 'standard_a4': 'Standard_A4', 'standard_a5': 'Standard_A5', 'standard_a6': 'Standard_A6', 'standard_a7': 'Standard_A7', 'standard_a8': 'Standard_A8', 'standard_a9': 'Standard_A9', 'standard_a10': 'Standard_A10', 'standard_a11': 'Standard_A11', 'standard_a1_v2': 'Standard_A1_v2', 'standard_a2_v2': 'Standard_A2_v2', 'standard_a4_v2': 'Standard_A4_v2', 'standard_a8_v2': 'Standard_A8_v2', 'standard_a2m_v2': 'Standard_A2m_v2', 'standard_a4m_v2': 'Standard_A4m_v2', 'standard_a8m_v2': 'Standard_A8m_v2', 'standard_b1s': 'Standard_B1s', 'standard_b1ms': 'Standard_B1ms', 'standard_b2s': 'Standard_B2s', 'standard_b2ms': 'Standard_B2ms', 'standard_b4ms': 'Standard_B4ms', 'standard_b8ms': 'Standard_B8ms', 'standard_d1': 'Standard_D1', 'standard_d2': 'Standard_D2', 'standard_d3': 'Standard_D3', 'standard_d4': 'Standard_D4', 'standard_d11': 'Standard_D11', 'standard_d12': 'Standard_D12', 'standard_d13': 'Standard_D13', 'standard_d14': 'Standard_D14', 'standard_d1_v2': 'Standard_D1_v2', 'standard_d2_v2': 'Standard_D2_v2', 'standard_d3_v2': 'Standard_D3_v2', 'standard_d4_v2': 'Standard_D4_v2', 'standard_d5_v2': 'Standard_D5_v2', 'standard_d2_v3': 'Standard_D2_v3', 'standard_d4_v3': 'Standard_D4_v3', 'standard_d8_v3': 'Standard_D8_v3', 'standard_d16_v3': 'Standard_D16_v3', 'standard_d32_v3': 'Standard_D32_v3', 'standard_d64_v3': 'Standard_D64_v3', 'standard_d2s_v3': 'Standard_D2s_v3', 'standard_d4s_v3': 'Standard_D4s_v3', 'standard_d8s_v3': 'Standard_D8s_v3', 'standard_d16s_v3': 'Standard_D16s_v3', 'standard_d32s_v3': 'Standard_D32s_v3', 'standard_d64s_v3': 'Standard_D64s_v3', 'standard_d11_v2': 'Standard_D11_v2', 'standard_d12_v2': 'Standard_D12_v2', 'standard_d13_v2': 'Standard_D13_v2', 'standard_d14_v2': 'Standard_D14_v2', 'standard_d15_v2': 'Standard_D15_v2', 'standard_ds1': 'Standard_DS1', 'standard_ds2': 'Standard_DS2', 'standard_ds3': 'Standard_DS3', 'standard_ds4': 'Standard_DS4', 'standard_ds11': 'Standard_DS11', 'standard_ds12': 'Standard_DS12', 'standard_ds13': 'Standard_DS13', 'standard_ds14': 'Standard_DS14', 'standard_ds1_v2': 'Standard_DS1_v2', 'standard_ds2_v2': 'Standard_DS2_v2', 'standard_ds3_v2': 'Standard_DS3_v2', 'standard_ds4_v2': 'Standard_DS4_v2', 'standard_ds5_v2': 'Standard_DS5_v2', 'standard_ds11_v2': 'Standard_DS11_v2', 'standard_ds12_v2': 'Standard_DS12_v2', 'standard_ds13_v2': 'Standard_DS13_v2', 'standard_ds14_v2': 'Standard_DS14_v2', 'standard_ds15_v2': 'Standard_DS15_v2', 'standard_ds13-4_v2': 'Standard_DS13-4_v2', 'standard_ds13-2_v2': 'Standard_DS13-2_v2', 'standard_ds14-8_v2': 'Standard_DS14-8_v2', 'standard_ds14-4_v2': 'Standard_DS14-4_v2', 'standard_e2_v3': 'Standard_E2_v3', 'standard_e4_v3': 'Standard_E4_v3', 'standard_e8_v3': 'Standard_E8_v3', 'standard_e16_v3': 'Standard_E16_v3', 'standard_e32_v3': 'Standard_E32_v3', 'standard_e64_v3': 'Standard_E64_v3', 'standard_e2s_v3': 'Standard_E2s_v3', 'standard_e4s_v3': 'Standard_E4s_v3', 'standard_e8s_v3': 'Standard_E8s_v3', 'standard_e16s_v3': 'Standard_E16s_v3', 'standard_e32s_v3': 'Standard_E32s_v3', 'standard_e64s_v3': 'Standard_E64s_v3', 'standard_e32-16_v3': 'Standard_E32-16_v3', 'standard_e32-8s_v3': 'Standard_E32-8s_v3', 'standard_e64-32s_v3': 'Standard_E64-32s_v3', 'standard_e64-16s_v3': 'Standard_E64-16s_v3', 'standard_f1': 'Standard_F1', 'standard_f2': 'Standard_F2', 'standard_f4': 'Standard_F4', 'standard_f8': 'Standard_F8', 'standard_f16': 'Standard_F16', 'standard_f1s': 'Standard_F1s', 'standard_f2s': 'Standard_F2s', 'standard_f4s': 'Standard_F4s', 'standard_f8s': 'Standard_F8s', 'standard_f16s': 'Standard_F16s', 'standard_f2s_v2': 'Standard_F2s_v2', 'standard_f4s_v2': 'Standard_F4s_v2', 'standard_f8s_v2': 'Standard_F8s_v2', 'standard_f16s_v2': 'Standard_F16s_v2', 'standard_f32s_v2': 'Standard_F32s_v2', 'standard_f64s_v2': 'Standard_F64s_v2', 'standard_f72s_v2': 'Standard_F72s_v2', 'standard_g1': 'Standard_G1', 'standard_g2': 'Standard_G2', 'standard_g3': 'Standard_G3', 'standard_g4': 'Standard_G4', 'standard_g5': 'Standard_G5', 'standard_gs1': 'Standard_GS1', 'standard_gs2': 'Standard_GS2', 'standard_gs3': 'Standard_GS3', 'standard_gs4': 'Standard_GS4', 'standard_gs5': 'Standard_GS5', 'standard_gs4-8': 'Standard_GS4-8', 'standard_gs4-4': 'Standard_GS4-4', 'standard_gs5-16': 'Standard_GS5-16', 'standard_gs5-8': 'Standard_GS5-8', 'standard_h8': 'Standard_H8', 'standard_h16': 'Standard_H16', 'standard_h8m': 'Standard_H8m', 'standard_h16m': 'Standard_H16m', 'standard_h16r': 'Standard_H16r', 'standard_h16mr': 'Standard_H16mr', 'standard_l4s': 'Standard_L4s', 'standard_l8s': 'Standard_L8s', 'standard_l16s': 'Standard_L16s', 'standard_l32s': 'Standard_L32s', 'standard_m64s': 'Standard_M64s', 'standard_m64ms': 'Standard_M64ms', 'standard_m128s': 'Standard_M128s', 'standard_m128ms': 'Standard_M128ms', 'standard_m64-32ms': 'Standard_M64-32ms', 'standard_m64-16ms': 'Standard_M64-16ms', 'standard_m128-64ms': 'Standard_M128-64ms', 'standard_m128-32ms': 'Standard_M128-32ms', 'standard_nc6': 'Standard_NC6', 'standard_nc12': 'Standard_NC12', 'standard_nc24': 'Standard_NC24', 'standard_nc24r': 'Standard_NC24r', 'standard_nc6s_v2': 'Standard_NC6s_v2', 'standard_nc12s_v2': 'Standard_NC12s_v2', 'standard_nc24s_v2': 'Standard_NC24s_v2', 'standard_nc24rs_v2': 'Standard_NC24rs_v2', 'standard_nc6s_v3': 'Standard_NC6s_v3', 'standard_nc12s_v3': 'Standard_NC12s_v3', 'standard_nc24s_v3': 'Standard_NC24s_v3', 'standard_nc24rs_v3': 'Standard_NC24rs_v3', 'standard_nd6s': 'Standard_ND6s', 'standard_nd12s': 'Standard_ND12s', 'standard_nd24s': 'Standard_ND24s', 'standard_nd24rs': 'Standard_ND24rs', 'standard_nv6': 'Standard_NV6', 'standard_nv12': 'Standard_NV12', 'standard_nv24': 'Standard_NV24'})
        dict_resource_id(self.parameters, ['storage_profile', 'image_reference', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'os_type'], True)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'caching'], True)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'diff_disk_settings', 'option'], True)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'create_option'], True)
        dict_resource_id(self.parameters, ['storage_profile', 'os_disk', 'managed_disk', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'managed_disk', 'storage_account_type'], True)
        dict_map(self.parameters, ['storage_profile', 'os_disk', 'managed_disk', 'storage_account_type'], {'standard_lrs': 'Standard_LRS', 'premium_lrs': 'Premium_LRS', 'standard_ssd_lrs': 'StandardSSD_LRS', 'ultra_ssd_lrs': 'UltraSSD_LRS'})
        dict_camelize(self.parameters, ['storage_profile', 'data_disks', 'caching'], True)
        dict_camelize(self.parameters, ['storage_profile', 'data_disks', 'create_option'], True)
        dict_resource_id(self.parameters, ['storage_profile', 'data_disks', 'managed_disk', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['storage_profile', 'data_disks', 'managed_disk', 'storage_account_type'], True)
        dict_map(self.parameters, ['storage_profile', 'data_disks', 'managed_disk', 'storage_account_type'], {'standard_lrs': 'Standard_LRS', 'premium_lrs': 'Premium_LRS', 'standard_ssd_lrs': 'StandardSSD_LRS', 'ultra_ssd_lrs': 'UltraSSD_LRS'})
        dict_camelize(self.parameters, ['os_profile', 'windows_configuration', 'additional_unattend_content', 'pass_name'], True)
        dict_camelize(self.parameters, ['os_profile', 'windows_configuration', 'additional_unattend_content', 'component_name'], True)
        dict_map(self.parameters, ['os_profile', 'windows_configuration', 'additional_unattend_content', 'component_name'], {'microsoft-_windows-_shell-_setup': 'Microsoft-Windows-Shell-Setup'})
        dict_camelize(self.parameters, ['os_profile', 'windows_configuration', 'additional_unattend_content', 'setting_name'], True)
        dict_camelize(self.parameters, ['os_profile', 'windows_configuration', 'win_rm', 'listeners', 'protocol'], True)
        dict_resource_id(self.parameters, ['os_profile', 'secrets', 'source_vault', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['network_profile', 'network_interfaces', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['availability_set', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['identity', 'type'], True)
        dict_map(self.parameters, ['identity', 'type'], {'system_assigned, _user_assigned': 'SystemAssigned, UserAssigned'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Machine instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualmachine()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Machine instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualmachine()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Machine instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_virtualmachine(self):
        '''
        Creates or updates Virtual Machine with the specified configuration.

        :return: deserialized Virtual Machine instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Machine instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_machines.create_or_update(resource_group_name=self.resource_group,
                                                                          vm_name=self.name,
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
        self.log("Deleting the Virtual Machine instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_machines.delete(resource_group_name=self.resource_group,
                                                                vm_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Machine instance.')
            self.fail("Error deleting the Virtual Machine instance: {0}".format(str(e)))

        return True

    def get_virtualmachine(self):
        '''
        Gets the properties of the specified Virtual Machine.

        :return: deserialized Virtual Machine instance state dictionary
        '''
        self.log("Checking if the Virtual Machine instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_machines.get(resource_group_name=self.resource_group,
                                                             vm_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Machine instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Machine instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMVirtualMachine()


if __name__ == '__main__':
    main()
