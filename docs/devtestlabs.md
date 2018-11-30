# Azure DevTest Labs

## Additional Documentation

https://docs.microsoft.com/en-us/azure/lab-services/


## Prerequisites

- Ansible 2.7
- Azure service principal

## How to run example?

Copy **vars.example.yml** to **vars.yml**
Change appropriate values in **vars.yml**

The only value which is required is **github_token**. Others can be default.


Go to **examples** folder and run:

```
ansible-playbook devtestlabs-basic.yml -e @vars.yml
```

## What the example will create?

- Storage Account
- Lab
- Virtual Network
- Artifacts Source
- Virtual Machine

## Creating DevTest Lab

```
- name: Create instance of Lab
  azure_rm_devtestlabslab:
    resource_group: "{{ resource_group }}"
    name: "lab{{ rpfx}}"
    location: eastus
    lab_storage_type: standard
    premium_data_disks: no
```

## Creating Virtual Network

Virtual Network can be created without specifying any parameters:

```
- name: Create instance of dev test labs virtual network
  azure_rm_devtestlabsvirtualnetwork:
    resource_group: "{{ resource_group }}"
    lab_name: "lab{{ rpfx}}"
    name: "vn{{ rpfx }}"
    location: eastus
  register: output_vn
```

By default following is created:

```
"virtual_networks": [
    {
        "allowed_subnets": [
            {
                "allow_public_ip": "Allow",
                "lab_subnet_name": "vnabcxyzSubnet",
                "resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrg/providers/Microsoft.Network/virtualNetworks/vnabcxyz/subnets/vnabcxyzSubnet"
            }
        ],
        "created_date": "2018-11-30T02:04:32.946506Z",
        "external_provider_resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrg/providers/Microsoft.Network/virtualNetworks/vnabcxyz",
        "id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourcegroups/zimsmainrg/providers/microsoft.devtestlab/labs/lababcxyz/virtualnetworks/vnabcxyz",
        "name": "vnabcxyz",
        "provisioning_state": "Succeeded",
        "subnet_overrides": [
            {
                "lab_subnet_name": "vnabcxyzSubnet",
                "resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrg/providers/Microsoft.Network/virtualNetworks/vnabcxyz/subnets/vnabcxyzSubnet",
                "shared_public_ip_address_configuration": {
                    "allowed_ports": [
                        {
                            "backend_port": 3389,
                            "transport_protocol": "Tcp"
                        },
                        {
                            "backend_port": 22,
                            "transport_protocol": "Tcp"
                        }
                    ]
                },
                "use_in_vm_creation_permission": "Allow",
                "use_public_ip_address_permission": "Allow"
            }
        ],
        "type": "Microsoft.DevTestLab/labs/virtualNetworks",
        "unique_identifier": "3df219b6-3780-43e3-b0c7-9cb4f7e04f9a"
    }
],
```

## Can I assign my own Virtual Network?

Virtual Network can be assigned externally:

```
    - name: Create a virtual network
      azure_rm_virtualnetwork:
        name: vnet{{ rpfx }}
        resource_group: "{{ resource_group }}"
        location: eastus
        address_prefixes_cidr:
            - 10.1.0.0/16
            - 172.100.0.0/16
        dns_servers:
            - 127.0.0.1
            - 127.0.0.2
      register: vn_output
    - name: Create a subnet A
      azure_rm_subnet:
        name: subnet{{ rpfx }}a
        virtual_network_name: vnet{{ rpfx }}
        resource_group: "{{ resource_group }}"
        address_prefix_cidr: 10.1.0.0/24
      register: subnet_a_output

    - name: Create a subnet B
      azure_rm_subnet:
        name: subnet{{ rpfx }}b
        virtual_network_name: vnet{{ rpfx }}
        resource_group: "{{ resource_group }}"
        address_prefix_cidr: 172.100.0.0/24
      register: subnet_b_output

    - name: Create instance of dev test labs virtual network
      azure_rm_devtestlabsvirtualnetwork:
        resource_group: "{{ resource_group }}"
        lab_name: "lab{{ rpfx}}"
        name: "vn{{ rpfx }}"
        location: eastus
        external_provider_resource_id: "{{ vn_output.state.id }}"
```

In such case, nothing else will be created by default:

```
        "virtual_networks": [
            {
                "allowed_subnets": [],
                "created_date": "2018-11-30T07:04:53.628887Z",
                "external_provider_resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrgxx/providers/Microsoft.Network/virtualNetworks/vnetabcxyz",
                "id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourcegroups/zimsmainrgxx/providers/microsoft.devtestlab/labs/lababcxyz/virtualnetworks/vnabcxyz",
                "name": "vnabcxyz",
                "provisioning_state": "Succeeded",
                "type": "Microsoft.DevTestLab/labs/virtualNetworks",
                "unique_identifier": "e016ce14-da50-4a50-ab10-b86e1f9373c8"
            }
        ]
```


## Creating Virtual Machine

Following playbook creates Virtual Machine using Ubunty 16.04 and installs Mongo DB on it.

```
    - name: Create instance of dev test labs virtual machine
      azure_rm_devtestlabsvirtualmachine:
        resource_group: "{{ resource_group }}"
        lab_name: "lab{{ rpfx}}"
        name: "vm{{ rpfx }}"
        location: eastus
        notes: Virtual machine notes, just something....
        created_by_user: zikalino@microsoft.com
        os_type: linux
        size: Standard_A2_v2
        user_name: zim
        password: ZSuppas$$21!
        lab_subnet_name: "vn{{ rpfx }}Subnet"
        lab_virtual_network_id: "{{ output_vn.id }}"
        disallow_public_ip_address: yes
        gallery_image_reference:
          offer: UbuntuServer
          publisher: Canonical
          sku: 16.04-LTS
          os_type: Linux
          version: latest
        artifacts:
          - artifact_id: "{{ artifacts_output.id }}/Artifacts/linux-install-mongodb"
```



Raw output from DevTest Lab Virtual Machine looks as follows:

```
"virtual_machines": [
    {
        "allow_claim": false,
        "artifact_deployment_status": {
            "artifacts_applied": 1,
            "deployment_status": "Succeeded",
            "total_artifacts": 1
        },
        "compute_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/lababcxyz-vmabcxyz-354876/providers/Microsoft.Compute/virtualMachines/vmabcxyz",
        "created_by_user": "",
        "created_by_user_id": "",
        "created_date": "2018-11-30T02:05:35.94768Z",
        "disallow_public_ip_address": true,
        "gallery_image_reference": {
            "offer": "UbuntuServer",
            "os_type": "Linux",
            "publisher": "Canonical",
            "sku": "16.04-LTS",
            "version": "latest"
        },
        "id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourcegroups/zimsmainrg/providers/microsoft.devtestlab/labs/lababcxyz/virtualmachines/vmabcxyz",
        "location": "eastus",
        "name": "vmabcxyz",
        "network_interface": {},
        "notes": "Virtual machine notes, just something....",
        "os_type": "Linux",
        "owner_object_id": "20d81029-94cd-4923-a766-994415ff73bd",
        "owner_user_principal_name": "",
        "provisioning_state": "Succeeded",
        "size": "Standard_A2_v2",
        "storage_type": "Standard",
        "type": "Microsoft.DevTestLab/labs/virtualMachines",
        "unique_identifier": "fb8b15fb-5c29-43e1-aa8e-259f05785ff5",
        "user_name": "zim",
        "virtual_machine_creation_source": "FromGalleryImage"
    }
],
```

## Known Issues

**Artifacts source can only be assigned to VM only if its name is the same as lab name**. Otherwise following error occurs:

“Error creating the Virtual Machine instance: Azure Error: UnknownArtifactSourceUsed\nMessage: Artifact source lababcxyz is not present in lab lababcxyz.”

**security_token needed even if GitHub repo is public**

Security token should be optional.

