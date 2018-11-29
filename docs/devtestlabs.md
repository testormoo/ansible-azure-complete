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
