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
module: azure_rm_appgateway
version_added: "2.8"
short_description: Manage Azure Application Gateway instance.
description:
    - Create, update and delete instance of Azure Application Gateway.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the application gateway.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - SKU of the application gateway resource.
        suboptions:
            name:
                description:
                    - Name of an application gateway SKU.
                choices:
                    - 'standard_small'
                    - 'standard_medium'
                    - 'standard_large'
                    - 'waf_medium'
                    - 'waf_large'
            tier:
                description:
                    - Tier of an application gateway.
                choices:
                    - 'standard'
                    - 'waf'
            capacity:
                description:
                    - Capacity (instance count) of an application gateway.
    ssl_policy:
        description:
            - SSL policy of the application gateway resource.
        suboptions:
            disabled_ssl_protocols:
                description:
                    - Ssl protocols to be disabled on application gateway.
                type: list
            policy_type:
                description:
                    - Type of Ssl Policy.
                choices:
                    - 'predefined'
                    - 'custom'
            policy_name:
                description:
                    - Name of Ssl C(predefined) policy.
                choices:
                    - 'app_gw_ssl_policy20150501'
                    - 'app_gw_ssl_policy20170401'
                    - 'app_gw_ssl_policy20170401_s'
            cipher_suites:
                description:
                    - Ssl cipher suites to be enabled in the specified order to application gateway.
                type: list
            min_protocol_version:
                description:
                    - Minimum version of Ssl protocol to be supported on application gateway.
                choices:
                    - 'tl_sv1_0'
                    - 'tl_sv1_1'
                    - 'tl_sv1_2'
    gateway_ip_configurations:
        description:
            - Subnets of application the gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            subnet:
                description:
                    - Reference of the subnet resource. A subnet from where application gateway gets its private address.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    authentication_certificates:
        description:
            - Authentication certificates of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            data:
                description:
                    - Certificate public data.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    ssl_certificates:
        description:
            - SSL certificates of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            data:
                description:
                    - Base-64 encoded pfx certificate. Only applicable in PUT Request.
            password:
                description:
                    - Password for the pfx file specified in I(data). Only applicable in PUT request.
            public_cert_data:
                description:
                    - Base-64 encoded Public cert I(data) corresponding to pfx specified in I(data). Only applicable in GET request.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    frontend_ip_configurations:
        description:
            - Frontend IP addresses of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            private_ip_address:
                description:
                    - PrivateIPAddress of the network interface IP Configuration.
            private_ip_allocation_method:
                description:
                    - PrivateIP allocation method.
                choices:
                    - 'static'
                    - 'dynamic'
            subnet:
                description:
                    - Reference of the subnet resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            public_ip_address:
                description:
                    - Reference of the PublicIP resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    frontend_ports:
        description:
            - Frontend ports of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            port:
                description:
                    - Frontend port
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    probes:
        description:
            - Probes of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            protocol:
                description:
                    - Protocol.
                choices:
                    - 'http'
                    - 'https'
            host:
                description:
                    - Host name to send the probe to.
            path:
                description:
                    - "Relative path of probe. Valid path starts from '/'. Probe is sent to <I(protocol)>://<I(host)>:<port><path>"
            interval:
                description:
                    - "The probing interval in seconds. This is the time interval between two consecutive probes. Acceptable values are from 1 second to
                       86400 seconds."
            timeout:
                description:
                    - "the probe timeout in seconds. Probe marked as failed if valid response is not received with this timeout period. Acceptable values
                       are from 1 second to 86400 seconds."
            unhealthy_threshold:
                description:
                    - "The probe retry count. Backend server is marked down after consecutive probe failure count reaches UnhealthyThreshold. Acceptable
                       values are from 1 second to 20."
            pick_host_name_from_backend_http_settings:
                description:
                    - Whether the I(host) header should be picked from the backend C(http) settings. Default value is false.
            min_servers:
                description:
                    - Minimum number of servers that are always marked healthy. Default value is 0.
            match:
                description:
                    - Criterion for classifying a healthy probe response.
                suboptions:
                    body:
                        description:
                            - Body that must be contained in the health response. Default value is empty.
                    status_codes:
                        description:
                            - Allowed ranges of healthy status codes. Default range of healthy status codes is 200-399.
                        type: list
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    backend_address_pools:
        description:
            - Backend address pool of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            backend_ip_configurations:
                description:
                    - Collection of references to IPs defined in network interfaces.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    application_gateway_backend_address_pools:
                        description:
                            - The reference of ApplicationGatewayBackendAddressPool resource.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            backend_ip_configurations:
                                description:
                                    - Collection of references to IPs defined in network interfaces.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    application_gateway_backend_address_pools:
                                        description:
                                            - The reference of ApplicationGatewayBackendAddressPool resource.
                                        type: list
                                    load_balancer_backend_address_pools:
                                        description:
                                            - The reference of LoadBalancerBackendAddressPool resource.
                                        type: list
                                    load_balancer_inbound_nat_rules:
                                        description:
                                            - A list of references of LoadBalancerInboundNatRules.
                                        type: list
                                    private_ip_address:
                                        description:
                                            - Private IP address of the IP configuration.
                                    private_ip_allocation_method:
                                        description:
                                            - "Defines how a private IP address is assigned. Possible values are: 'C(static)' and 'C(dynamic)'."
                                        choices:
                                            - 'static'
                                            - 'dynamic'
                                    private_ip_address_version:
                                        description:
                                            - "Available from Api-Version 2016-03-30 onwards, it represents whether the specific ipconfiguration is C(ipv4)
                                               or C(ipv6). Default is taken as C(ipv4).  Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                                        choices:
                                            - 'ipv4'
                                            - 'ipv6'
                                    subnet:
                                        description:
                                            - Subnet bound to the IP configuration.
                                    primary:
                                        description:
                                            - Gets whether this is a primary customer address on the network interface.
                                    public_ip_address:
                                        description:
                                            - Public IP address bound to the IP configuration.
                                    application_security_groups:
                                        description:
                                            - Application security groups in which the IP configuration is included.
                                        type: list
                                    name:
                                        description:
                                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                            backend_addresses:
                                description:
                                    - Backend addresses
                                type: list
                                suboptions:
                                    fqdn:
                                        description:
                                            - Fully qualified domain name (FQDN).
                                    ip_address:
                                        description:
                                            - IP address
                            name:
                                description:
                                    - Resource that is unique within a resource group. This name can be used to access the resource.
                            type:
                                description:
                                    - Type of the resource.
                    load_balancer_backend_address_pools:
                        description:
                            - The reference of LoadBalancerBackendAddressPool resource.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            name:
                                description:
                                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                    load_balancer_inbound_nat_rules:
                        description:
                            - A list of references of LoadBalancerInboundNatRules.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            frontend_ip_configuration:
                                description:
                                    - A reference to frontend IP addresses.
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                            protocol:
                                description:
                                    - "Possible values include: 'C(udp)', 'C(tcp)', 'C(all)'"
                                choices:
                                    - 'udp'
                                    - 'tcp'
                                    - 'all'
                            frontend_port:
                                description:
                                    - "The port for the external endpoint. Port numbers for each rule must be unique within the Load Balancer. Acceptable
                                       values range from 1 to 65534."
                            backend_port:
                                description:
                                    - The port used for the internal endpoint. Acceptable values range from 1 to 65535.
                            idle_timeout_in_minutes:
                                description:
                                    - "The timeout for the C(tcp) idle connection. The value can be set between 4 and 30 minutes. The default value is 4
                                       minutes. This element is only used when the I(protocol) is set to C(tcp)."
                            enable_floating_ip:
                                description:
                                    - "Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn
                                       Availability Group. This setting is required when using the SQL AlwaysOn Availability Groups in SQL server. This
                                       setting can't be changed after you create the endpoint."
                            name:
                                description:
                                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                    private_ip_address:
                        description:
                            - Private IP address of the IP configuration.
                    private_ip_allocation_method:
                        description:
                            - "Defines how a private IP address is assigned. Possible values are: 'C(static)' and 'C(dynamic)'."
                        choices:
                            - 'static'
                            - 'dynamic'
                    private_ip_address_version:
                        description:
                            - "Available from Api-Version 2016-03-30 onwards, it represents whether the specific ipconfiguration is C(ipv4) or C(ipv6).
                               Default is taken as C(ipv4).  Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                        choices:
                            - 'ipv4'
                            - 'ipv6'
                    subnet:
                        description:
                            - Subnet bound to the IP configuration.
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            address_prefix:
                                description:
                                    - The address prefix for the subnet.
                            network_security_group:
                                description:
                                    - The reference of the NetworkSecurityGroup resource.
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                                    security_rules:
                                        description:
                                            - A collection of security rules of the network security group.
                                        type: list
                                    default_security_rules:
                                        description:
                                            - The default security rules of network security group.
                                        type: list
                                    resource_guid:
                                        description:
                                            - The resource GUID property of the network security group resource.
                            route_table:
                                description:
                                    - The reference of the RouteTable resource.
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                                    routes:
                                        description:
                                            - Collection of routes contained within a route table.
                                        type: list
                                    disable_bgp_route_propagation:
                                        description:
                                            - Gets or sets whether to disable the I(routes) learned by BGP on that route table. True means disable.
                            service_endpoints:
                                description:
                                    - An array of service endpoints.
                                type: list
                                suboptions:
                                    service:
                                        description:
                                            - The type of the endpoint service.
                                    locations:
                                        description:
                                            - A list of locations.
                                        type: list
                            resource_navigation_links:
                                description:
                                    - Gets an array of references to the external resources using subnet.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    linked_resource_type:
                                        description:
                                            - Resource type of the linked resource.
                                    link:
                                        description:
                                            - Link to the external resource
                                    name:
                                        description:
                                            - Name of the resource that is unique within a resource group. This name can be used to access the resource.
                            name:
                                description:
                                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                    primary:
                        description:
                            - Gets whether this is a primary customer address on the network interface.
                    public_ip_address:
                        description:
                            - Public IP address bound to the IP configuration.
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            location:
                                description:
                                    - Resource location.
                            sku:
                                description:
                                    - The public IP address SKU.
                                suboptions:
                                    name:
                                        description:
                                            - Name of a public IP address SKU.
                                        choices:
                                            - 'basic'
                                            - 'standard'
                            public_ip_allocation_method:
                                description:
                                    - "The public IP allocation method. Possible values are: 'C(static)' and 'C(dynamic)'."
                                choices:
                                    - 'static'
                                    - 'dynamic'
                            public_ip_address_version:
                                description:
                                    - "The public IP address version. Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                                choices:
                                    - 'ipv4'
                                    - 'ipv6'
                            dns_settings:
                                description:
                                    - The FQDN of the DNS record associated with the public IP address.
                                suboptions:
                                    domain_name_label:
                                        description:
                                            - "Gets or sets the Domain name label.The concatenation of the domain name label and the regionalized DNS zone
                                               make up the fully qualified domain name associated with the public IP address. If a domain name label is
                                               specified, an A DNS record is created for the public IP in the Microsoft Azure DNS system."
                                    fqdn:
                                        description:
                                            - "Gets the FQDN, Fully qualified domain name of the A DNS record associated with the public IP. This is the
                                               concatenation of the I(domain_name_label) and the regionalized DNS zone."
                                    reverse_fqdn:
                                        description:
                                            - "Gets or Sets the Reverse I(fqdn). A user-visible, fully qualified domain name that resolves to this public IP
                                               address. If the reverseFqdn is specified, then a PTR DNS record is created pointing from the IP address in
                                               the in-addr.arpa domain to the reverse I(fqdn). "
                            ip_address:
                                description:
                                    - The IP address associated with the public IP address resource.
                            idle_timeout_in_minutes:
                                description:
                                    - The idle timeout of the public IP address.
                            resource_guid:
                                description:
                                    - The resource GUID property of the public IP resource.
                            zones:
                                description:
                                    - A list of availability zones denoting the IP allocated for the resource needs to come from.
                                type: list
                    application_security_groups:
                        description:
                            - Application security groups in which the IP configuration is included.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            location:
                                description:
                                    - Resource location.
                    name:
                        description:
                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            backend_addresses:
                description:
                    - Backend addresses
                type: list
                suboptions:
                    fqdn:
                        description:
                            - Fully qualified domain name (FQDN).
                    ip_address:
                        description:
                            - IP address
            name:
                description:
                    - Resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    backend_http_settings_collection:
        description:
            - Backend http settings of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            port:
                description:
                    - Port
            protocol:
                description:
                    - Protocol.
                choices:
                    - 'http'
                    - 'https'
            cookie_based_affinity:
                description:
                    - "Cookie based affinity. Possible values include: 'Enabled', 'Disabled'"
                type: bool
            request_timeout:
                description:
                    - "Request timeout in seconds. Application Gateway will fail the request if response is not received within RequestTimeout. Acceptable
                       values are from 1 second to 86400 seconds."
            probe:
                description:
                    - Probe resource of an application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            authentication_certificates:
                description:
                    - Array of references to application gateway authentication certificates.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
            connection_draining:
                description:
                    - Connection draining of the backend C(http) settings resource.
                suboptions:
                    enabled:
                        description:
                            - Whether connection draining is enabled or not.
                            - Required when C(state) is I(present).
                    drain_timeout_in_sec:
                        description:
                            - The number of seconds connection draining is active. Acceptable values are from 1 second to 3600 seconds.
                            - Required when C(state) is I(present).
            host_name:
                description:
                    - Host header to be sent to the backend servers.
            pick_host_name_from_backend_address:
                description:
                    - Whether to pick host header should be picked from the host name of the backend server. Default value is false.
            affinity_cookie_name:
                description:
                    - Cookie name to use for the affinity cookie.
            probe_enabled:
                description:
                    - Whether the I(probe) is enabled. Default value is false.
            path:
                description:
                    - Path which should be used as a prefix for all C(http) requests. Null means no path will be prefixed. Default value is null.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    http_listeners:
        description:
            - Http listeners of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            frontend_ip_configuration:
                description:
                    - Frontend IP configuration resource of an application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            frontend_port:
                description:
                    - Frontend port resource of an application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            protocol:
                description:
                    - Protocol.
                choices:
                    - 'http'
                    - 'https'
            host_name:
                description:
                    - Host name of C(http) listener.
            ssl_certificate:
                description:
                    - SSL certificate resource of an application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            require_server_name_indication:
                description:
                    - Applicable only if I(protocol) is C(https). Enables SNI for multi-hosting.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    url_path_maps:
        description:
            - URL path map of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            default_backend_address_pool:
                description:
                    - Default backend address pool resource of URL path map.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            default_backend_http_settings:
                description:
                    - Default backend http settings resource of URL path map.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            default_redirect_configuration:
                description:
                    - Default redirect configuration resource of URL path map.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            path_rules:
                description:
                    - Path rule of URL path map resource.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    paths:
                        description:
                            - Path rules of URL path map.
                        type: list
                    backend_address_pool:
                        description:
                            - Backend address pool resource of URL path map path rule.
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                    backend_http_settings:
                        description:
                            - Backend http settings resource of URL path map path rule.
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                    redirect_configuration:
                        description:
                            - Redirect configuration resource of URL path map path rule.
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                    name:
                        description:
                            - Name of the resource that is unique within a resource group. This name can be used to access the resource.
                    type:
                        description:
                            - Type of the resource.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    request_routing_rules:
        description:
            - Request routing rules of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            rule_type:
                description:
                    - Rule I(type).
                choices:
                    - 'basic'
                    - 'path_based_routing'
            backend_address_pool:
                description:
                    - Backend address pool resource of the application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            backend_http_settings:
                description:
                    - Frontend port resource of the application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            http_listener:
                description:
                    - Http listener resource of the application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            url_path_map:
                description:
                    - URL path map resource of the application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            redirect_configuration:
                description:
                    - Redirect configuration resource of the application gateway.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    redirect_configurations:
        description:
            - Redirect configurations of the application gateway resource.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            redirect_type:
                description:
                    - Supported http redirection types - C(permanent), C(temporary), C(found), C(see_other).
                choices:
                    - 'permanent'
                    - 'found'
                    - 'see_other'
                    - 'temporary'
            target_listener:
                description:
                    - Reference to a listener to redirect the request to.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            target_url:
                description:
                    - Url to redirect the request to.
            include_path:
                description:
                    - Include path in the redirected url.
            include_query_string:
                description:
                    - Include query string in the redirected url.
            request_routing_rules:
                description:
                    - Request routing specifying redirect configuration.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
            url_path_maps:
                description:
                    - Url path maps specifying default redirect configuration.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
            path_rules:
                description:
                    - Path rules specifying redirect configuration.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
            name:
                description:
                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            type:
                description:
                    - Type of the resource.
    web_application_firewall_configuration:
        description:
            - Web application firewall configuration.
        suboptions:
            enabled:
                description:
                    - Whether the web application firewall is enabled or not.
                    - Required when C(state) is I(present).
            firewall_mode:
                description:
                    - Web application firewall mode.
                    - Required when C(state) is I(present).
                choices:
                    - 'detection'
                    - 'prevention'
            rule_set_type:
                description:
                    - "The type of the web application firewall rule set. Possible values are: 'OWASP'."
                    - Required when C(state) is I(present).
            rule_set_version:
                description:
                    - The version of the rule set type.
                    - Required when C(state) is I(present).
            disabled_rule_groups:
                description:
                    - The disabled rule groups.
                type: list
                suboptions:
                    rule_group_name:
                        description:
                            - The name of the rule group that will be disabled.
                            - Required when C(state) is I(present).
                    rules:
                        description:
                            - The list of rules that will be disabled. If null, all rules of the rule group will be disabled.
                        type: list
    enable_http2:
        description:
            - Whether HTTP2 is enabled on the application gateway resource.
    resource_guid:
        description:
            - Resource GUID property of the application gateway resource.
    state:
      description:
        - Assert the state of the Application Gateway.
        - Use 'present' to create or update an Application Gateway and 'absent' to delete it.
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
  - name: Create (or update) Application Gateway
    azure_rm_appgateway:
      resource_group: NOT FOUND
      name: NOT FOUND
      location: eastus
      backend_http_settings_collection:
        - cookie_based_affinity: cookie_based_affinity
'''

RETURN = '''
id:
    description:
        - Resource ID.
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
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApplicationGateway(AzureRMModuleBase):
    """Configuration class for an Azure RM Application Gateway resource"""

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
            id=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['standard_small',
                                 'standard_medium',
                                 'standard_large',
                                 'waf_medium',
                                 'waf_large']
                    ),
                    tier=dict(
                        type='str',
                        choices=['standard',
                                 'waf']
                    ),
                    capacity=dict(
                        type='int'
                    )
                )
            ),
            ssl_policy=dict(
                type='dict',
                options=dict(
                    disabled_ssl_protocols=dict(
                        type='list'
                    ),
                    policy_type=dict(
                        type='str',
                        choices=['predefined',
                                 'custom']
                    ),
                    policy_name=dict(
                        type='str',
                        choices=['app_gw_ssl_policy20150501',
                                 'app_gw_ssl_policy20170401',
                                 'app_gw_ssl_policy20170401_s']
                    ),
                    cipher_suites=dict(
                        type='list'
                    ),
                    min_protocol_version=dict(
                        type='str',
                        choices=['tl_sv1_0',
                                 'tl_sv1_1',
                                 'tl_sv1_2']
                    )
                )
            ),
            gateway_ip_configurations=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    subnet=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            authentication_certificates=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    data=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            ssl_certificates=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    data=dict(
                        type='str'
                    ),
                    password=dict(
                        type='str',
                        no_log=True
                    ),
                    public_cert_data=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            frontend_ip_configurations=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    private_ip_address=dict(
                        type='str'
                    ),
                    private_ip_allocation_method=dict(
                        type='str',
                        choices=['static',
                                 'dynamic']
                    ),
                    subnet=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    public_ip_address=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            frontend_ports=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    port=dict(
                        type='int'
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            probes=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    protocol=dict(
                        type='str',
                        choices=['http',
                                 'https']
                    ),
                    host=dict(
                        type='str'
                    ),
                    path=dict(
                        type='str'
                    ),
                    interval=dict(
                        type='int'
                    ),
                    timeout=dict(
                        type='int'
                    ),
                    unhealthy_threshold=dict(
                        type='int'
                    ),
                    pick_host_name_from_backend_http_settings=dict(
                        type='str'
                    ),
                    min_servers=dict(
                        type='int'
                    ),
                    match=dict(
                        type='dict',
                        options=dict(
                            body=dict(
                                type='str'
                            ),
                            status_codes=dict(
                                type='list'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            backend_address_pools=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    backend_ip_configurations=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            application_gateway_backend_address_pools=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    backend_ip_configurations=dict(
                                        type='list',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            application_gateway_backend_address_pools=dict(
                                                type='list'
                                            ),
                                            load_balancer_backend_address_pools=dict(
                                                type='list'
                                            ),
                                            load_balancer_inbound_nat_rules=dict(
                                                type='list'
                                            ),
                                            private_ip_address=dict(
                                                type='str'
                                            ),
                                            private_ip_allocation_method=dict(
                                                type='str',
                                                choices=['static',
                                                         'dynamic']
                                            ),
                                            private_ip_address_version=dict(
                                                type='str',
                                                choices=['ipv4',
                                                         'ipv6']
                                            ),
                                            subnet=dict(
                                                type='dict'
                                            ),
                                            primary=dict(
                                                type='str'
                                            ),
                                            public_ip_address=dict(
                                                type='dict'
                                            ),
                                            application_security_groups=dict(
                                                type='list'
                                            ),
                                            name=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    backend_addresses=dict(
                                        type='list',
                                        options=dict(
                                            fqdn=dict(
                                                type='str'
                                            ),
                                            ip_address=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    name=dict(
                                        type='str'
                                    ),
                                    type=dict(
                                        type='str'
                                    )
                                )
                            ),
                            load_balancer_backend_address_pools=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            load_balancer_inbound_nat_rules=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    frontend_ip_configuration=dict(
                                        type='dict',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    protocol=dict(
                                        type='str',
                                        choices=['udp',
                                                 'tcp',
                                                 'all']
                                    ),
                                    frontend_port=dict(
                                        type='int'
                                    ),
                                    backend_port=dict(
                                        type='int'
                                    ),
                                    idle_timeout_in_minutes=dict(
                                        type='int'
                                    ),
                                    enable_floating_ip=dict(
                                        type='str'
                                    ),
                                    name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            private_ip_address=dict(
                                type='str'
                            ),
                            private_ip_allocation_method=dict(
                                type='str',
                                choices=['static',
                                         'dynamic']
                            ),
                            private_ip_address_version=dict(
                                type='str',
                                choices=['ipv4',
                                         'ipv6']
                            ),
                            subnet=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    address_prefix=dict(
                                        type='str'
                                    ),
                                    network_security_group=dict(
                                        type='dict',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            ),
                                            security_rules=dict(
                                                type='list'
                                            ),
                                            default_security_rules=dict(
                                                type='list'
                                            ),
                                            resource_guid=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    route_table=dict(
                                        type='dict',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            ),
                                            routes=dict(
                                                type='list'
                                            ),
                                            disable_bgp_route_propagation=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    service_endpoints=dict(
                                        type='list',
                                        options=dict(
                                            service=dict(
                                                type='str'
                                            ),
                                            locations=dict(
                                                type='list'
                                            )
                                        )
                                    ),
                                    resource_navigation_links=dict(
                                        type='list',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            linked_resource_type=dict(
                                                type='str'
                                            ),
                                            link=dict(
                                                type='str'
                                            ),
                                            name=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            primary=dict(
                                type='str'
                            ),
                            public_ip_address=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    location=dict(
                                        type='str'
                                    ),
                                    sku=dict(
                                        type='dict',
                                        options=dict(
                                            name=dict(
                                                type='str',
                                                choices=['basic',
                                                         'standard']
                                            )
                                        )
                                    ),
                                    public_ip_allocation_method=dict(
                                        type='str',
                                        choices=['static',
                                                 'dynamic']
                                    ),
                                    public_ip_address_version=dict(
                                        type='str',
                                        choices=['ipv4',
                                                 'ipv6']
                                    ),
                                    dns_settings=dict(
                                        type='dict',
                                        options=dict(
                                            domain_name_label=dict(
                                                type='str'
                                            ),
                                            fqdn=dict(
                                                type='str'
                                            ),
                                            reverse_fqdn=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    ip_address=dict(
                                        type='str'
                                    ),
                                    idle_timeout_in_minutes=dict(
                                        type='int'
                                    ),
                                    resource_guid=dict(
                                        type='str'
                                    ),
                                    zones=dict(
                                        type='list'
                                    )
                                )
                            ),
                            application_security_groups=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    location=dict(
                                        type='str'
                                    )
                                )
                            ),
                            name=dict(
                                type='str'
                            )
                        )
                    ),
                    backend_addresses=dict(
                        type='list',
                        options=dict(
                            fqdn=dict(
                                type='str'
                            ),
                            ip_address=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            backend_http_settings_collection=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    port=dict(
                        type='int'
                    ),
                    protocol=dict(
                        type='str',
                        choices=['http',
                                 'https']
                    ),
                    cookie_based_affinity=dict(
                        type='bool'
                    ),
                    request_timeout=dict(
                        type='int'
                    ),
                    probe=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    authentication_certificates=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    connection_draining=dict(
                        type='dict',
                        options=dict(
                            enabled=dict(
                                type='str'
                            ),
                            drain_timeout_in_sec=dict(
                                type='int'
                            )
                        )
                    ),
                    host_name=dict(
                        type='str'
                    ),
                    pick_host_name_from_backend_address=dict(
                        type='str'
                    ),
                    affinity_cookie_name=dict(
                        type='str'
                    ),
                    probe_enabled=dict(
                        type='str'
                    ),
                    path=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            http_listeners=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    frontend_ip_configuration=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    frontend_port=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    protocol=dict(
                        type='str',
                        choices=['http',
                                 'https']
                    ),
                    host_name=dict(
                        type='str'
                    ),
                    ssl_certificate=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    require_server_name_indication=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            url_path_maps=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    default_backend_address_pool=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    default_backend_http_settings=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    default_redirect_configuration=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    path_rules=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            paths=dict(
                                type='list'
                            ),
                            backend_address_pool=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            backend_http_settings=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            redirect_configuration=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            name=dict(
                                type='str'
                            ),
                            type=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            request_routing_rules=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    rule_type=dict(
                        type='str',
                        choices=['basic',
                                 'path_based_routing']
                    ),
                    backend_address_pool=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    backend_http_settings=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    http_listener=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    url_path_map=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    redirect_configuration=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            redirect_configurations=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    redirect_type=dict(
                        type='str',
                        choices=['permanent',
                                 'found',
                                 'see_other',
                                 'temporary']
                    ),
                    target_listener=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    target_url=dict(
                        type='str'
                    ),
                    include_path=dict(
                        type='str'
                    ),
                    include_query_string=dict(
                        type='str'
                    ),
                    request_routing_rules=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    url_path_maps=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    path_rules=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            web_application_firewall_configuration=dict(
                type='dict',
                options=dict(
                    enabled=dict(
                        type='str'
                    ),
                    firewall_mode=dict(
                        type='str',
                        choices=['detection',
                                 'prevention']
                    ),
                    rule_set_type=dict(
                        type='str'
                    ),
                    rule_set_version=dict(
                        type='str'
                    ),
                    disabled_rule_groups=dict(
                        type='list',
                        options=dict(
                            rule_group_name=dict(
                                type='str'
                            ),
                            rules=dict(
                                type='list'
                            )
                        )
                    )
                )
            ),
            enable_http2=dict(
                type='str'
            ),
            resource_guid=dict(
                type='str'
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

        super(AzureRMApplicationGateway, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_map(self.parameters, ['sku', 'name'], {'standard_small': 'Standard_Small', 'standard_medium': 'Standard_Medium', 'standard_large': 'Standard_Large', 'waf_medium': 'WAF_Medium', 'waf_large': 'WAF_Large'})
        dict_camelize(self.parameters, ['sku', 'tier'], True)
        dict_map(self.parameters, ['sku', 'tier'], {'waf': 'WAF'})
        dict_camelize(self.parameters, ['ssl_policy', 'policy_type'], True)
        dict_camelize(self.parameters, ['ssl_policy', 'policy_name'], True)
        dict_camelize(self.parameters, ['ssl_policy', 'min_protocol_version'], True)
        dict_map(self.parameters, ['ssl_policy', 'min_protocol_version'], {'tl_sv1_0': 'TLSv1_0', 'tl_sv1_1': 'TLSv1_1', 'tl_sv1_2': 'TLSv1_2'})
        dict_resource_id(self.parameters, ['gateway_ip_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['gateway_ip_configurations', 'subnet', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['authentication_certificates', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['ssl_certificates', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'private_ip_allocation_method'], True)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'public_ip_address', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['frontend_ports', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['probes', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['probes', 'protocol'], True)
        dict_resource_id(self.parameters, ['backend_address_pools', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'application_gateway_backend_address_pools', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'private_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'private_ip_address_version'], True)
        dict_map(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'private_ip_address_version'], {'ipv4': 'IPv4', 'ipv6': 'IPv6'})
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'load_balancer_backend_address_pools', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'load_balancer_inbound_nat_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'load_balancer_inbound_nat_rules', 'frontend_ip_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'load_balancer_inbound_nat_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'private_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'private_ip_address_version'], True)
        dict_map(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'private_ip_address_version'], {'ipv4': 'IPv4', 'ipv6': 'IPv6'})
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'subnet', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'subnet', 'network_security_group', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'subnet', 'route_table', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'subnet', 'resource_navigation_links', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'sku', 'name'], True)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'public_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'public_ip_address_version'], True)
        dict_map(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'public_ip_address_version'], {'ipv4': 'IPv4', 'ipv6': 'IPv6'})
        dict_resource_id(self.parameters, ['backend_address_pools', 'backend_ip_configurations', 'application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_http_settings_collection', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['backend_http_settings_collection', 'protocol'], True)
        dict_map(self.parameters, ['backend_http_settings_collection', 'cookie_based_affinity'], {True: 'Enabled', False: 'Disabled'})
        dict_resource_id(self.parameters, ['backend_http_settings_collection', 'probe', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['backend_http_settings_collection', 'authentication_certificates', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['http_listeners', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['http_listeners', 'frontend_ip_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['http_listeners', 'frontend_port', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['http_listeners', 'protocol'], True)
        dict_resource_id(self.parameters, ['http_listeners', 'ssl_certificate', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'default_backend_address_pool', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'default_backend_http_settings', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'default_redirect_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'path_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'path_rules', 'backend_address_pool', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'path_rules', 'backend_http_settings', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['url_path_maps', 'path_rules', 'redirect_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['request_routing_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['request_routing_rules', 'rule_type'], True)
        dict_resource_id(self.parameters, ['request_routing_rules', 'backend_address_pool', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['request_routing_rules', 'backend_http_settings', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['request_routing_rules', 'http_listener', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['request_routing_rules', 'url_path_map', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['request_routing_rules', 'redirect_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['redirect_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['redirect_configurations', 'redirect_type'], True)
        dict_resource_id(self.parameters, ['redirect_configurations', 'target_listener', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['redirect_configurations', 'request_routing_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['redirect_configurations', 'url_path_maps', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['redirect_configurations', 'path_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['web_application_firewall_configuration', 'firewall_mode'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_applicationgateway()

        if not old_response:
            self.log("Application Gateway instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Application Gateway instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Application Gateway instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_applicationgateway()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Application Gateway instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_applicationgateway()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Application Gateway instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_applicationgateway(self):
        '''
        Creates or updates Application Gateway with the specified configuration.

        :return: deserialized Application Gateway instance state dictionary
        '''
        self.log("Creating / Updating the Application Gateway instance {0}".format(self.name))

        try:
            response = self.mgmt_client.application_gateways.create_or_update(resource_group_name=self.resource_group,
                                                                              application_gateway_name=self.name,
                                                                              parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Application Gateway instance.')
            self.fail("Error creating the Application Gateway instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_applicationgateway(self):
        '''
        Deletes specified Application Gateway instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Application Gateway instance {0}".format(self.name))
        try:
            response = self.mgmt_client.application_gateways.delete(resource_group_name=self.resource_group,
                                                                    application_gateway_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Application Gateway instance.')
            self.fail("Error deleting the Application Gateway instance: {0}".format(str(e)))

        return True

    def get_applicationgateway(self):
        '''
        Gets the properties of the specified Application Gateway.

        :return: deserialized Application Gateway instance state dictionary
        '''
        self.log("Checking if the Application Gateway instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.application_gateways.get(resource_group_name=self.resource_group,
                                                                 application_gateway_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Application Gateway instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Application Gateway instance.')
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
    AzureRMApplicationGateway()


if __name__ == '__main__':
    main()
