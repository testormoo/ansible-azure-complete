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
module: azure_rm_webapp
version_added: "2.8"
short_description: Manage Web App instance.
description:
    - Create, update and delete instance of Web App.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Unique name of the app to create or update. To create or update a deployment slot, use the {slot} parameter.
        required: True
    site_envelope:
        description:
            - A JSON representation of the app properties. See example.
        required: True
        suboptions:
            kind:
                description:
                    - Kind of resource.
            location:
                description:
                    - Resource Location.
                required: True
            enabled:
                description:
                    - "<code>true</code> if the app is enabled; otherwise, <code>false</code>. Setting this value to false disables the app (takes the app
                       offline)."
            host_name_ssl_states:
                description:
                    - "Hostname SSL states are used to manage the SSL bindings for app's hostnames."
                type: list
                suboptions:
                    name:
                        description:
                            - Hostname.
                    ssl_state:
                        description:
                            - SSL type.
                        choices:
                            - 'disabled'
                            - 'sni_enabled'
                            - 'ip_based_enabled'
                    virtual_ip:
                        description:
                            - Virtual IP address assigned to the hostname if IP based SSL is enabled.
                    thumbprint:
                        description:
                            - SSL certificate thumbprint.
                    to_update:
                        description:
                            - Set to <code>true</code> to update existing hostname.
                    host_type:
                        description:
                            - Indicates whether the hostname is a C(standard) or C(repository) hostname.
                        choices:
                            - 'standard'
                            - 'repository'
            server_farm_id:
                description:
                    - "Resource ID of the associated App Service plan, formatted as:
                       '/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}'."
            reserved:
                description:
                    - <code>true</code> if reserved; otherwise, <code>false</code>.
            site_config:
                description:
                    - Configuration of the app.
                suboptions:
                    number_of_workers:
                        description:
                            - Number of workers.
                    default_documents:
                        description:
                            - Default documents.
                        type: list
                    net_framework_version:
                        description:
                            - .NET Framework version.
                    php_version:
                        description:
                            - Version of PHP.
                    python_version:
                        description:
                            - Version of Python.
                    node_version:
                        description:
                            - Version of Node.js.
                    linux_fx_version:
                        description:
                            - Linux App Framework and version
                    request_tracing_enabled:
                        description:
                            - <code>true</code> if request tracing is enabled; otherwise, <code>false</code>.
                    request_tracing_expiration_time:
                        description:
                            - Request tracing expiration time.
                    remote_debugging_enabled:
                        description:
                            - <code>true</code> if remote debugging is enabled; otherwise, <code>false</code>.
                    remote_debugging_version:
                        description:
                            - Remote debugging version.
                    http_logging_enabled:
                        description:
                            - <code>true</code> if HTTP logging is enabled; otherwise, <code>false</code>.
                    logs_directory_size_limit:
                        description:
                            - HTTP logs directory size limit.
                    detailed_error_logging_enabled:
                        description:
                            - <code>true</code> if detailed error logging is enabled; otherwise, <code>false</code>.
                    publishing_username:
                        description:
                            - Publishing user name.
                    app_settings:
                        description:
                            - Application settings.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Pair name.
                            value:
                                description:
                                    - Pair value.
                    connection_strings:
                        description:
                            - Connection strings.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Name of connection string.
                            connection_string:
                                description:
                                    - Connection string value.
                            type:
                                description:
                                    - Type of database.
                                choices:
                                    - 'my_sql'
                                    - 'sql_server'
                                    - 'sql_azure'
                                    - 'custom'
                                    - 'notification_hub'
                                    - 'service_bus'
                                    - 'event_hub'
                                    - 'api_hub'
                                    - 'doc_db'
                                    - 'redis_cache'
                                    - 'postgre_sql'
                    handler_mappings:
                        description:
                            - Handler mappings.
                        type: list
                        suboptions:
                            extension:
                                description:
                                    - Requests with this extension will be handled using the specified FastCGI application.
                            script_processor:
                                description:
                                    - The absolute path to the FastCGI application.
                            arguments:
                                description:
                                    - Command-line arguments to be passed to the script processor.
                    document_root:
                        description:
                            - Document root.
                    scm_type:
                        description:
                            - SCM type.
                        choices:
                            - 'none'
                            - 'dropbox'
                            - 'tfs'
                            - 'local_git'
                            - 'git_hub'
                            - 'code_plex_git'
                            - 'code_plex_hg'
                            - 'bitbucket_git'
                            - 'bitbucket_hg'
                            - 'external_git'
                            - 'external_hg'
                            - 'one_drive'
                            - 'vso'
                    use32_bit_worker_process:
                        description:
                            - <code>true</code> to use 32-bit worker process; otherwise, <code>false</code>.
                    web_sockets_enabled:
                        description:
                            - <code>true</code> if WebSocket is enabled; otherwise, <code>false</code>.
                    always_on:
                        description:
                            - <code>true</code> if Always On is enabled; otherwise, <code>false</code>.
                    java_version:
                        description:
                            - Java version.
                    java_container:
                        description:
                            - Java container.
                    java_container_version:
                        description:
                            - Java container version.
                    app_command_line:
                        description:
                            - App command line to launch.
                    managed_pipeline_mode:
                        description:
                            - Managed pipeline mode.
                        choices:
                            - 'integrated'
                            - 'classic'
                    virtual_applications:
                        description:
                            - Virtual applications.
                        type: list
                        suboptions:
                            virtual_path:
                                description:
                                    - Virtual path.
                            physical_path:
                                description:
                                    - Physical path.
                            preload_enabled:
                                description:
                                    - <code>true</code> if preloading is enabled; otherwise, <code>false</code>.
                            virtual_directories:
                                description:
                                    - Virtual directories for virtual application.
                                type: list
                                suboptions:
                                    virtual_path:
                                        description:
                                            - Path to virtual application.
                                    physical_path:
                                        description:
                                            - Physical path.
                    load_balancing:
                        description:
                            - Site load balancing.
                        choices:
                            - 'weighted_round_robin'
                            - 'least_requests'
                            - 'least_response_time'
                            - 'weighted_total_traffic'
                            - 'request_hash'
                    experiments:
                        description:
                            - This is work around for polymophic types.
                        suboptions:
                            ramp_up_rules:
                                description:
                                    - List of ramp-up rules.
                                type: list
                                suboptions:
                                    action_host_name:
                                        description:
                                            - Hostname of a slot to which the traffic will be redirected if decided to. E.g. myapp-stage.azurewebsites.net.
                                    reroute_percentage:
                                        description:
                                            - Percentage of the traffic which will be redirected to <code>I(action_host_name)</code>.
                                    change_step:
                                        description:
                                            - "In auto ramp up scenario this is the step to to add/remove from <code>I(reroute_percentage)</code> until it
                                               reaches "
                                            - "<code>I(min_reroute_percentage)</code> or <code>I(max_reroute_percentage)</code>. Site metrics are checked
                                               every N minutes specificed in <code>I(change_interval_in_minutes)</code>."
                                            - "Custom decision algorithm can be provided in TiPCallback site extension which URL can be specified in
                                               <code>I(change_decision_callback_url)</code>."
                                    change_interval_in_minutes:
                                        description:
                                            - Specifies interval in mimuntes to reevaluate I(reroute_percentage).
                                    min_reroute_percentage:
                                        description:
                                            - Specifies lower boundary above which I(reroute_percentage) will stay.
                                    max_reroute_percentage:
                                        description:
                                            - Specifies upper boundary below which I(reroute_percentage) will stay.
                                    change_decision_callback_url:
                                        description:
                                            - "Custom decision algorithm can be provided in TiPCallback site extension which URL can be specified. See
                                               TiPCallback site extension for the scaffold and contracts."
                                            - "https://www.siteextensions.net/packages/TiPCallback/"
                                    name:
                                        description:
                                            - "Name of the routing rule. The recommended name would be to point to the slot which will receive the traffic
                                               in the experiment."
                    limits:
                        description:
                            - Site limits.
                        suboptions:
                            max_percentage_cpu:
                                description:
                                    - Maximum allowed CPU usage percentage.
                            max_memory_in_mb:
                                description:
                                    - Maximum allowed memory usage in MB.
                            max_disk_size_in_mb:
                                description:
                                    - Maximum allowed disk size usage in MB.
                    auto_heal_enabled:
                        description:
                            - <code>true</code> if Auto Heal is enabled; otherwise, <code>false</code>.
                    auto_heal_rules:
                        description:
                            - Auto Heal rules.
                        suboptions:
                            triggers:
                                description:
                                    - Conditions that describe when to execute the auto-heal I(actions).
                                suboptions:
                                    requests:
                                        description:
                                            - A rule based on total requests.
                                        suboptions:
                                            count:
                                                description:
                                                    - Request Count.
                                            time_interval:
                                                description:
                                                    - Time interval.
                                    private_bytes_in_kb:
                                        description:
                                            - A rule based on private bytes.
                                    status_codes:
                                        description:
                                            - A rule based on status codes.
                                        type: list
                                        suboptions:
                                            status:
                                                description:
                                                    - HTTP status code.
                                            sub_status:
                                                description:
                                                    - Request Sub I(status).
                                            win32_status:
                                                description:
                                                    - Win32 error code.
                                            count:
                                                description:
                                                    - Request Count.
                                            time_interval:
                                                description:
                                                    - Time interval.
                                    slow_requests:
                                        description:
                                            - A rule based on request execution time.
                                        suboptions:
                                            time_taken:
                                                description:
                                                    - Time taken.
                                            count:
                                                description:
                                                    - Request Count.
                                            time_interval:
                                                description:
                                                    - Time interval.
                            actions:
                                description:
                                    - Actions to be executed when a rule is triggered.
                                suboptions:
                                    action_type:
                                        description:
                                            - Predefined action to be taken.
                                        choices:
                                            - 'recycle'
                                            - 'log_event'
                                            - 'custom_action'
                                    custom_action:
                                        description:
                                            - Custom action to be taken.
                                        suboptions:
                                            exe:
                                                description:
                                                    - Executable to be run.
                                            parameters:
                                                description:
                                                    - Parameters for the executable.
                                    min_process_execution_time:
                                        description:
                                            - Minimum time the process must execute
                                            - before taking the action
                    tracing_options:
                        description:
                            - Tracing options.
                    vnet_name:
                        description:
                            - Virtual Network name.
                    cors:
                        description:
                            - Cross-Origin Resource Sharing (CORS) settings.
                        suboptions:
                            allowed_origins:
                                description:
                                    - Gets or sets the list of origins that should be allowed to make cross-origin
                                    - "calls (for example: http://example.com:12345). Use '*' to allow all."
                                type: list
                    push:
                        description:
                            - Push endpoint settings.
                        suboptions:
                            kind:
                                description:
                                    - Kind of resource.
                            is_push_enabled:
                                description:
                                    - Gets or sets a flag indicating whether the Push endpoint is enabled.
                            tag_whitelist_json:
                                description:
                                    - Gets or sets a JSON string containing a list of tags that are whitelisted for use by the push registration endpoint.
                            tags_requiring_auth:
                                description:
                                    - "Gets or sets a JSON string containing a list of tags that require user authentication to be used in the push
                                       registration endpoint."
                                    - "Tags can consist of alphanumeric characters and the following:"
                                    - "'_', '@', '#', '.', ':', '-'. "
                                    - Validation should be performed at the PushRequestHandler.
                            dynamic_tags_json:
                                description:
                                    - "Gets or sets a JSON string containing a list of dynamic tags that will be evaluated from user claims in the push
                                       registration endpoint."
                    api_definition:
                        description:
                            - Information about the formal API definition for the app.
                        suboptions:
                            url:
                                description:
                                    - The URL of the API definition.
                    auto_swap_slot_name:
                        description:
                            - Auto-swap slot name.
                    local_my_sql_enabled:
                        description:
                            - <code>true</code> to enable local MySQL; otherwise, <code>false</code>.
                    ip_security_restrictions:
                        description:
                            - IP security restrictions.
                        type: list
                        suboptions:
                            ip_address:
                                description:
                                    - IP address the security restriction is valid for.
                                required: True
                            subnet_mask:
                                description:
                                    - Subnet mask for the range of IP addresses the restriction is valid for.
                    http20_enabled:
                        description:
                            - "Http20Enabled: configures a web site to allow clients to connect over http2.0"
                    min_tls_version:
                        description:
                            - "MinTlsVersion: configures the minimum version of TLS required for SSL requests."
                        choices:
                            - '1.0'
                            - '1.1'
                            - '1.2'
            scm_site_also_stopped:
                description:
                    - <code>true</code> to stop SCM (KUDU) site when the app is stopped; otherwise, <code>false</code>. The default is <code>false</code>.
            hosting_environment_profile:
                description:
                    - App Service Environment to use for the app.
                suboptions:
                    id:
                        description:
                            - Resource ID of the App Service Environment.
            client_affinity_enabled:
                description:
                    - "<code>true</code> to enable client affinity; <code>false</code> to stop sending session affinity cookies, which route client requests
                       in the same session to the same instance. Default is <code>true</code>."
            client_cert_enabled:
                description:
                    - "<code>true</code> to enable client certificate authentication (TLS mutual authentication); otherwise, <code>false</code>. Default is
                       <code>false</code>."
            host_names_disabled:
                description:
                    - <code>true</code> to disable the public hostnames of the app; otherwise, <code>false</code>.
                    -  If <code>true</code>, the app is only accessible via API management process.
            container_size:
                description:
                    - Size of the function container.
            daily_memory_time_quota:
                description:
                    - Maximum allowed daily memory-time quota (applicable on dynamic apps only).
            cloning_info:
                description:
                    - If specified during app creation, the app is cloned from a source app.
                suboptions:
                    correlation_id:
                        description:
                            - Correlation ID of cloning operation. This ID ties multiple cloning operations
                            - together to use the same snapshot.
                    overwrite:
                        description:
                            - <code>true</code> to overwrite destination app; otherwise, <code>false</code>.
                    clone_custom_host_names:
                        description:
                            - <code>true</code> to clone custom hostnames from source app; otherwise, <code>false</code>.
                    clone_source_control:
                        description:
                            - <code>true</code> to clone source control from source app; otherwise, <code>false</code>.
                    source_web_app_id:
                        description:
                            - ARM resource ID of the source app. App resource ID is of the form
                            - /subscriptions/{subId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{siteName} for production slots and
                            - "/subscriptions/{subId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{siteName}/slots/{slotName} for other
                               slots."
                        required: True
                    hosting_environment:
                        description:
                            - App Service Environment.
                    app_settings_overrides:
                        description:
                            - Application setting overrides for cloned app. If specified, these settings override the settings cloned
                            - from source app. Otherwise, application settings from source app are retained.
                    configure_load_balancing:
                        description:
                            - <code>true</code> to configure load balancing for source and destination app.
                    traffic_manager_profile_id:
                        description:
                            - ARM resource ID of the Traffic Manager profile to use, if it exists. Traffic Manager resource ID is of the form
                            - /subscriptions/{subId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{profileName}.
                    traffic_manager_profile_name:
                        description:
                            - Name of Traffic Manager profile to create. This is only needed if Traffic Manager profile does not already exist.
                    ignore_quotas:
                        description:
                            - <code>true</code> if quotas should be ignored; otherwise, <code>false</code>.
            snapshot_info:
                description:
                    - If specified during app creation, the app is created from a previous snapshot.
                suboptions:
                    kind:
                        description:
                            - Kind of resource.
                    snapshot_time:
                        description:
                            - Point in time in which the app recovery should be attempted, formatted as a DateTime string.
                    recovery_target:
                        description:
                            - Specifies the web app that snapshot contents will be written to.
                        suboptions:
                            location:
                                description:
                                    - Geographical location of the target web app, e.g. SouthEastAsia, SouthCentralUS
                            id:
                                description:
                                    - ARM resource ID of the target app.
                                    - "/subscriptions/{subId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{siteName} for production
                                       slots and "
                                    - "/subscriptions/{subId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{siteName}/slots/{slotName}
                                       for other slots."
                    overwrite:
                        description:
                            - If <code>true</code> the recovery operation can overwrite source app; otherwise, <code>false</code>.
                    recover_configuration:
                        description:
                            - If true, site configuration, in addition to content, will be reverted.
                    ignore_conflicting_host_names:
                        description:
                            - If true, custom hostname conflicts will be ignored when recovering to a target web app.
                            - This setting is only necessary when I(recover_configuration) is enabled.
            https_only:
                description:
                    - "HttpsOnly: configures a web site to accept only https requests. Issues redirect for"
                    - http requests
            identity:
                description:
                suboptions:
                    type:
                        description:
                            - Type of managed service identity.
                        choices:
                            - 'system_assigned'
    state:
      description:
        - Assert the state of the Web App.
        - Use 'present' to create or update an Web App and 'absent' to delete it.
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
  - name: Create (or update) Web App
    azure_rm_webapp:
      resource_group: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: id
state:
    description:
        - Current state of the app.
    returned: always
    type: str
    sample: state
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.web import WebSiteManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWebApps(AzureRMModuleBase):
    """Configuration class for an Azure RM Web App resource"""

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
            site_envelope=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.site_envelope = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWebApps, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "kind":
                    self.site_envelope["kind"] = kwargs[key]
                elif key == "location":
                    self.site_envelope["location"] = kwargs[key]
                elif key == "enabled":
                    self.site_envelope["enabled"] = kwargs[key]
                elif key == "host_name_ssl_states":
                    ev = kwargs[key]
                    if 'ssl_state' in ev:
                        if ev['ssl_state'] == 'disabled':
                            ev['ssl_state'] = 'Disabled'
                        elif ev['ssl_state'] == 'sni_enabled':
                            ev['ssl_state'] = 'SniEnabled'
                        elif ev['ssl_state'] == 'ip_based_enabled':
                            ev['ssl_state'] = 'IpBasedEnabled'
                    if 'host_type' in ev:
                        if ev['host_type'] == 'standard':
                            ev['host_type'] = 'Standard'
                        elif ev['host_type'] == 'repository':
                            ev['host_type'] = 'Repository'
                    self.site_envelope["host_name_ssl_states"] = ev
                elif key == "server_farm_id":
                    self.site_envelope["server_farm_id"] = kwargs[key]
                elif key == "reserved":
                    self.site_envelope["reserved"] = kwargs[key]
                elif key == "site_config":
                    ev = kwargs[key]
                    if 'scm_type' in ev:
                        if ev['scm_type'] == 'none':
                            ev['scm_type'] = 'None'
                        elif ev['scm_type'] == 'dropbox':
                            ev['scm_type'] = 'Dropbox'
                        elif ev['scm_type'] == 'tfs':
                            ev['scm_type'] = 'Tfs'
                        elif ev['scm_type'] == 'local_git':
                            ev['scm_type'] = 'LocalGit'
                        elif ev['scm_type'] == 'git_hub':
                            ev['scm_type'] = 'GitHub'
                        elif ev['scm_type'] == 'code_plex_git':
                            ev['scm_type'] = 'CodePlexGit'
                        elif ev['scm_type'] == 'code_plex_hg':
                            ev['scm_type'] = 'CodePlexHg'
                        elif ev['scm_type'] == 'bitbucket_git':
                            ev['scm_type'] = 'BitbucketGit'
                        elif ev['scm_type'] == 'bitbucket_hg':
                            ev['scm_type'] = 'BitbucketHg'
                        elif ev['scm_type'] == 'external_git':
                            ev['scm_type'] = 'ExternalGit'
                        elif ev['scm_type'] == 'external_hg':
                            ev['scm_type'] = 'ExternalHg'
                        elif ev['scm_type'] == 'one_drive':
                            ev['scm_type'] = 'OneDrive'
                        elif ev['scm_type'] == 'vso':
                            ev['scm_type'] = 'VSO'
                    if 'managed_pipeline_mode' in ev:
                        if ev['managed_pipeline_mode'] == 'integrated':
                            ev['managed_pipeline_mode'] = 'Integrated'
                        elif ev['managed_pipeline_mode'] == 'classic':
                            ev['managed_pipeline_mode'] = 'Classic'
                    if 'load_balancing' in ev:
                        if ev['load_balancing'] == 'weighted_round_robin':
                            ev['load_balancing'] = 'WeightedRoundRobin'
                        elif ev['load_balancing'] == 'least_requests':
                            ev['load_balancing'] = 'LeastRequests'
                        elif ev['load_balancing'] == 'least_response_time':
                            ev['load_balancing'] = 'LeastResponseTime'
                        elif ev['load_balancing'] == 'weighted_total_traffic':
                            ev['load_balancing'] = 'WeightedTotalTraffic'
                        elif ev['load_balancing'] == 'request_hash':
                            ev['load_balancing'] = 'RequestHash'
                    self.site_envelope["site_config"] = ev
                elif key == "scm_site_also_stopped":
                    self.site_envelope["scm_site_also_stopped"] = kwargs[key]
                elif key == "hosting_environment_profile":
                    self.site_envelope["hosting_environment_profile"] = kwargs[key]
                elif key == "client_affinity_enabled":
                    self.site_envelope["client_affinity_enabled"] = kwargs[key]
                elif key == "client_cert_enabled":
                    self.site_envelope["client_cert_enabled"] = kwargs[key]
                elif key == "host_names_disabled":
                    self.site_envelope["host_names_disabled"] = kwargs[key]
                elif key == "container_size":
                    self.site_envelope["container_size"] = kwargs[key]
                elif key == "daily_memory_time_quota":
                    self.site_envelope["daily_memory_time_quota"] = kwargs[key]
                elif key == "cloning_info":
                    self.site_envelope["cloning_info"] = kwargs[key]
                elif key == "snapshot_info":
                    self.site_envelope["snapshot_info"] = kwargs[key]
                elif key == "https_only":
                    self.site_envelope["https_only"] = kwargs[key]
                elif key == "identity":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'system_assigned':
                            ev['type'] = 'SystemAssigned'
                    self.site_envelope["identity"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(WebSiteManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_webapp()

        if not old_response:
            self.log("Web App instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Web App instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Web App instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Web App instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_webapp()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Web App instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_webapp()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_webapp():
                time.sleep(20)
        else:
            self.log("Web App instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_webapp(self):
        '''
        Creates or updates Web App with the specified configuration.

        :return: deserialized Web App instance state dictionary
        '''
        self.log("Creating / Updating the Web App instance {0}".format(self.name))

        try:
            response = self.mgmt_client.web_apps.create_or_update(resource_group_name=self.resource_group,
                                                                  name=self.name,
                                                                  site_envelope=self.site_envelope)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Web App instance.')
            self.fail("Error creating the Web App instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_webapp(self):
        '''
        Deletes specified Web App instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Web App instance {0}".format(self.name))
        try:
            response = self.mgmt_client.web_apps.delete(resource_group_name=self.resource_group,
                                                        name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Web App instance.')
            self.fail("Error deleting the Web App instance: {0}".format(str(e)))

        return True

    def get_webapp(self):
        '''
        Gets the properties of the specified Web App.

        :return: deserialized Web App instance state dictionary
        '''
        self.log("Checking if the Web App instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.web_apps.get(resource_group_name=self.resource_group,
                                                     name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Web App instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Web App instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMWebApps()


if __name__ == '__main__':
    main()
