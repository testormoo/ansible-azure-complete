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
module: azure_rm_computevirtualmachineruncommand_facts
version_added: "2.8"
short_description: Get Azure Virtual Machine Run Command facts.
description:
    - Get facts of Azure Virtual Machine Run Command.

options:
    location:
        description:
            - The location upon which run commands is queried.
        required: True
    command_id:
        description:
            - The command id.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Virtual Machine Run Command
    azure_rm_computevirtualmachineruncommand_facts:
      location: location
      command_id: command_id
'''

RETURN = '''
virtual_machine_run_commands:
    description: A list of dictionaries containing facts for Virtual Machine Run Command.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The VM run command id.
            returned: always
            type: str
            sample: RunPowerShellScript
        label:
            description:
                - The VM run command label.
            returned: always
            type: str
            sample: Executes a PowerShell script
        description:
            description:
                - The VM run command description.
            returned: always
            type: str
            sample: Custom multiline PowerShell script should be defined in script property. Optional parameters can be set in parameters property.
        script:
            description:
                - The script to be executed.
            returned: always
            type: str
            sample: "[\n  'param(',\n  '    [string]$arg1,',\n  '    [string]$arg2',\n  ')',\n  'Write-Host This is a sample script with parameters $arg1
                     $arg2'\n]"
        parameters:
            description:
                - The parameters used by the script.
            returned: always
            type: complex
            sample: parameters
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualMachineRunCommandsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            location=dict(
                type='str',
                required=True
            ),
            command_id=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.location = None
        self.command_id = None
        super(AzureRMVirtualMachineRunCommandsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['virtual_machine_run_commands'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.virtual_machine_run_commands.get(location=self.location,
                                                                         command_id=self.command_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for VirtualMachineRunCommands.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'label': d.get('label', None),
            'description': d.get('description', None),
            'script': d.get('script', None),
            'parameters': {
            }
        }
        return d


def main():
    AzureRMVirtualMachineRunCommandsFacts()


if __name__ == '__main__':
    main()
