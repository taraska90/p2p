# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import yaml
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import ipaddress
import os


template_dir = "templates"
template_end =  "end_router"
template_mpls = "mpls_router"
template_vlan = "vlans"
var_mpls = "data/mpls"  # Directory with data for generating templates
var_end = "data/end"
cnf = "cnf"  # Directory with rendered configurations
mpls_data = os.listdir(var_mpls)
end_data = os.listdir(var_end)

env = Environment(loader = FileSystemLoader(template_dir),
                  trim_blocks=True, lstrip_blocks=True)

#  Generating conf files for ned router
for end in end_data:
    template = env.get_template(template_end)
    templ_vl =  env.get_template(template_vlan)
    end = var_end + "/" + end
    vars_dict = yaml.load(open(end))
    network = vars_dict['network']
    net4 = ipaddress.ip_network(network.decode('utf-8'))
    mask = net4.netmask
    wildcard = net4.hostmask
    first_ip = net4[1]
    second_ip = net4[2]
    network_addr = net4.network_address
    result = template.render(vars_dict, mask=mask, wildcard=wildcard, first_ip=first_ip, second_ip=second_ip, network_addr=network_addr)
    cnf_end = cnf + "/" + vars_dict["hostname"]
    with open(cnf_end, 'w') as dest:
        for line in result:
            dest.write(line)
    result = ""
    result_vlan = templ_vl.render(vars_dict)
    cnf_vlan = cnf + "/" + vars_dict["vlan_name"]
    with open(cnf_vlan, 'w') as vlan_dest:
        for vlan_line in result_vlan:
            vlan_dest.write(vlan_line)

#  Genereating conf file for mpls router
for mpls in mpls_data:
    template = env.get_template(template_mpls)
    mpls = var_mpls + "/" + mpls
    vars_dict = yaml.load(open(mpls))
    network = vars_dict['network']
    net4 = ipaddress.ip_network(network.decode('utf-8'))
    mask = net4.netmask
    wildcard = net4.hostmask
    first_ip = net4[1]
    second_ip = net4[2]
    network_addr = net4.network_address
    result = template.render(vars_dict, mask=mask, wildcard=wildcard, first_ip=first_ip, second_ip=second_ip, network_addr=network_addr)
    cnf_mpls = cnf + "/" + vars_dict["hostname"]
    with open(cnf_mpls, 'w') as dest:
        for line in result:
            dest.write(line)
    result = ""

