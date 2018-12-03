# Azure DevTest Labs - Virtual Network Note

## Creating DevTest Lab

I have created Virtual Network with 2 subnets first:

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
```

and then trying to create dev test labs as follows:


```
    - name: Create instance of dev test labs virtual network
      azure_rm_devtestlabsvirtualnetwork:
        resource_group: "{{ resource_group }}"
        lab_name: "lab{{ rpfx}}"
        name: "vn{{ rpfx }}"
        location: eastus
        external_provider_resource_id: "{{ vn_output.state.id }}"
        allowed_subnets:
          - resource_id: "{{ subnet_a_output.state.id }}"
            lab_subnet_name: abc
            allow_public_ip: deny
          - resource_id: "{{ subnet_b_output.state.id }}"
            lab_subnet_name: def
            allow_public_ip: deny
        description: My Lab Virtual Network
        subnet_overrides:
          - resource_id: "{{ subnet_a_output.state.id }}"
            lab_subnet_name: ghi
            use_in_vm_creation_permission: allow
            use_public_ip_address_permission: allow
          - resource_id: "{{ subnet_b_output.state.id }}"
            lab_subnet_name: klm
            use_in_vm_creation_permission: deny
            use_public_ip_address_permission: deny
      register: output_vn
```

What I am getting is:

```
        "virtual_networks": [
            {
                "allowed_subnets": [
                    {
                        "allow_public_ip": "Allow",
                        "lab_subnet_name": "ghi",
                        "resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrgxx/providers/Microsoft.Network/virtualNetworks/vnetabcxyz/subnets/subnetabcxyza"
                    }
                ],
                "created_date": "2018-12-03T01:51:07.772065Z",
                "description": "My Lab Virtual Network",
                "external_provider_resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrgxx/providers/Microsoft.Network/virtualNetworks/vnetabcxyz",
                "id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourcegroups/zimsmainrgxx/providers/microsoft.devtestlab/labs/lababcxyz/virtualnetworks/vnabcxyz",
                "name": "vnabcxyz",
                "provisioning_state": "Succeeded",
                "subnet_overrides": [
                    {
                        "lab_subnet_name": "ghi",
                        "resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrgxx/providers/Microsoft.Network/virtualNetworks/vnetabcxyz/subnets/subnetabcxyza",
                        "use_in_vm_creation_permission": "Allow",
                        "use_public_ip_address_permission": "Allow"
                    },
                    {
                        "lab_subnet_name": "klm",
                        "resource_id": "/subscriptions/685ba005-af8d-4b04-8f16-a7bf38b2eb5a/resourceGroups/zimsmainrgxx/providers/Microsoft.Network/virtualNetworks/vnetabcxyz/subnets/subnetabcxyzb",
                        "use_in_vm_creation_permission": "Deny",
                        "use_public_ip_address_permission": "Deny"
                    }
                ],
                "type": "Microsoft.DevTestLab/labs/virtualNetworks",
                "unique_identifier": "59270d81-2e84-413a-8c6f-24f701dbb054"
            }
        ]```
