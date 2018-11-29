# Complete Azure support for Ansible

This repository contains all my work related to Ansible and Azure.

## Azure Modules

Complete set of more that 1000 Azure Resource Manager modules is available in

**modules/library**

Modules here cover entire Azure API. Not all of them are tested.

Any help will be appreciated.

If you think that particular module should be available in Ansible release, add your name, and submit your PRs to one or both of these repositories:

- https://github.com/ansible/ansible
- https://github.com/Azure/azure_preview_modules

## Examples

Playbook samples are placed in the root folder.

In order to use the examples you need to:

(1) Install Ansible

(2) Install dependencies

  TBD - provide dependencies file

## REST Examples

Full collection of REST API examples is available in:

**/examples-rest**

These examples are generated from REST API examples that can be found in Azure REST API specifications here:

https://github.com/Azure/azure-rest-api-specs

## Documentation

All Ansible related documentation is placed here:

**/docs**

I am trying to document as many scenarions as possible using Ansible.