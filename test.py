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
var_mpls = "data/mpls"  # Directory with data for generating templates
var_end = "data/end"
vars_file = "data-167"
cnf = "cnf"  # Directory with rendered configurations
mpls_data = os.listdir(var_mpls)
end_data = os.listdir(var_end)

env = Environment(loader = FileSystemLoader(template_dir),
                  trim_blocks=True, lstrip_blocks=True)

#  Generating conf files for ned router
vars_dict = yaml.load(open('data/end/ps167-cgr2010-2'))
network = vars_dict['network']
net4 = ipaddress.ip_network(network.decode('utf-8'))

network_key = ['first_ip', 'second_ip', 'network_addr', 'mask', 'wildcard']
network_value = [net4[1], net4[2], net4.network_address, net4.netmask, net4.hostmask]
net_param = dict(zip(network_key, network_value))
template = env.get_template(template_end)
vars_dict = yaml.load(open('data/end/ps167-cgr2010-2'))
result = template.render(vars_dict, net_param=net_param)
cnf_end = cnf + "/" + vars_dict["hostname"]
with open(cnf_end, 'w') as dest:
    for line in result:
        dest.write(line)



