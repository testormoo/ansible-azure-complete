# Azure DevTest Labs

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

Virtual Network can be created without specifying any parameters

```
- name: Create instance of dev test labs virtual network
  azure_rm_devtestlabsvirtualnetwork:
    resource_group: "{{ resource_group }}"
    lab_name: "lab{{ rpfx}}"
    name: "vn{{ rpfx }}"
    location: eastus
  register: output_vn
```

