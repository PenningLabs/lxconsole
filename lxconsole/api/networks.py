from flask import jsonify, request
import json
import requests
from lxconsole import db
from lxconsole.models import Server
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


def get_client_crt():
  return 'certs/client.crt'

def get_client_key():
  return 'certs/client.key'

@login_required
def api_networks_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})

  if endpoint == 'add_network':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    
    # Check to see if host is part of a cluster, if so, each cluster member needs to be notified of pending network interface
    cluster_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster?project=' + project
    results = requests.get(cluster_url, verify=server.ssl_verify, cert=(client_cert, client_key))
    cluster = results.json()['metadata']

    if cluster['enabled']:
      # Get list of cluster members
      cluster_members_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/members?recursion=1&project=' + project
      results = requests.get(cluster_members_url, verify=server.ssl_verify, cert=(client_cert, client_key))
      cluster_members = results.json()['metadata']

      # If request sent json data, extract it
      if request.form.get('json'):
        json_data = request.form.get('json')
        json_data = json.loads(json_data)
        data = {}
        data.update({'name': json_data['name']}) if 'name' in json_data.keys() else False
        data.update({'description': json_data['description']}) if 'description' in json_data.keys() else False
        data.update({'type': json_data['type']}) if 'type' in json_data.keys() else False
        config = {}

        # Build configuration to send to notify cluster hosts
        if 'type' in json_data.keys():
          if 'config' in json_data.keys():

            if json_data['type'] == "bridge":
              config.update({'bridge.external.interfaces': json_data['config']['bridge.external.interfaces']}) if 'bridge.external.interfaces' in json_data['config'].keys() else False

            if json_data['type'] == "macvlan" or json_data['type'] == "sriov" or json_data['type'] == "physical":
              config.update({'parent': json_data['config']['parent']}) if 'parent' in json_data['parent'] else False
          
            data.update({'config': config})

          # Notify each cluster host of pending network interface
          for member in cluster_members:
            member_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks?project=' + project + '&target=' + member['server_name']
            results = requests.post(member_url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)

        # Build the configuration needed to create the network interface
        config = {}
        if 'type' in json_data.keys():
          if 'config' in json_data.keys():
            # Do not include bridge.external.interfaces as this is a target node specific setting
            if json_data['type'] == "bridge":
              config.update({'bridge.driver': json_data['config']['bridge.driver']}) if 'bridge.driver' in json_data['config'].keys() else False
              config.update({'bridge.hwaddr': json_data['config']['bridge.hwaddr']}) if 'bridge.hwaddr' in json_data['config'].keys() else False
              config.update({'bridge.mode': json_data['config']['bridge.mode']}) if 'bridge.mode' in json_data['config'].keys() else False
              config.update({'bridge.mtu': json_data['config']['bridge.mtu']}) if 'bridge.mtu' in json_data['config'].keys() else False
              config.update({'dns.domain': json_data['config']['dns.domain']}) if 'dns.domain' in json_data['config'].keys() else False
              config.update({'dns.mode': json_data['config']['dns.mode']}) if 'dns.mode' in json_data['config'].keys() else False
              config.update({'dns.search': json_data['config']['dns.search']}) if 'dns.search' in json_data['config'].keys() else False
              config.update({'fan.overlay.subnet': json_data['config']['fan.overlay.subnet']}) if 'fan.overlay.subnet' in json_data['config'].keys() else False
              config.update({'fan.type': json_data['config']['fan.type']}) if 'fan.type' in json_data['config'].keys() else False
              config.update({'fan.underlay.subnet': json_data['config']['fan.underlay.subnet']}) if 'fan.underlay.subnet' in json_data['config'].keys() else False
              config.update({'ipv4.address': json_data['config']['ipv4.address']}) if 'ipv4.address' in json_data['config'].keys() else False
              config.update({'ipv4.dhcp': json_data['config']['ipv4.dhcp']}) if 'ipv4.dhcp' in json_data['config'].keys() else False
              config.update({'ipv4.dhcp.expiry': json_data['config']['ipv4.dhcp.expiry']}) if 'ipv4.dhcp.expiry' in json_data['config'].keys() else False
              config.update({'ipv4.dhcp.gateway': json_data['config']['ipv4.dhcp.gateway']}) if 'ipv4.dhcp.gateway' in json_data['config'].keys() else False
              config.update({'ipv4.dhcp.ranges': json_data['config']['ipv4.dhcp.ranges']}) if 'ipv4.dhcp.ranges' in json_data['config'].keys() else False
              config.update({'ipv4.firewall': json_data['config']['ipv4.firewall']}) if 'ipv4.firewall' in json_data['config'].keys() else False
              config.update({'ipv4.nat.address': json_data['config']['ipv4.nat.address']}) if 'ipv4.nat.address' in json_data['config'].keys() else False
              config.update({'ipv4.nat': json_data['config']['ipv4.nat']}) if 'ipv4.nat' in json_data['config'].keys() else False
              config.update({'ipv4.nat.order': json_data['config']['ipv4.nat.order']}) if 'ipv4.nat.order' in json_data['config'].keys() else False
              config.update({'ipv4.ovn.ranges': json_data['config']['ipv4.ovn.ranges']}) if 'ipv4.ovn.ranges' in json_data['config'].keys() else False
              config.update({'ipv4.routes': json_data['config']['ipv4.routes']}) if 'ipv4.routes' in json_data['config'].keys() else False
              config.update({'ipv4.routing': json_data['config']['ipv4.routing']}) if 'ipv4.routing' in json_data['config'].keys() else False
              config.update({'ipv6.address': json_data['config']['ipv6.address']}) if 'ipv6.address' in json_data['config'].keys() else False
              config.update({'ipv6.dhcp': json_data['config']['ipv6.dhcp']}) if 'ipv6.dhcp' in json_data['config'].keys() else False
              config.update({'ipv6.dhcp.expiry': json_data['config']['ipv6.dhcp.expiry']}) if 'ipv6.dhcp.expiry' in json_data['config'].keys() else False
              config.update({'ipv6.dhcp.ranges': json_data['config']['ipv6.dhcp.ranges']}) if 'ipv6.dhcp.ranges' in json_data['config'].keys() else False
              config.update({'ipv6.dhcp.stateful': json_data['config']['ipv6.dhcp.stateful']}) if 'ipv6.dhcp.stateful' in json_data['config'].keys() else False
              config.update({'ipv6.firewall': json_data['config']['ipv6.firewall']}) if 'ipv6.firewall' in json_data['config'].keys() else False
              config.update({'ipv6.nat.address': json_data['config']['ipv6.nat.address']}) if 'ipv6.nat.address' in json_data['config'].keys() else False
              config.update({'ipv6.nat': json_data['config']['ipv6.nat']}) if 'ipv6.nat' in json_data['config'].keys() else False
              config.update({'ipv6.nat.order': json_data['config']['ipv6.nat.order']}) if 'ipv6.nat.order' in json_data['config'].keys() else False
              config.update({'ipv6.ovn.ranges': json_data['config']['ipv6.ovn.ranges']}) if 'ipv6.ovn.ranges' in json_data['config'].keys() else False
              config.update({'ipv6.routes': json_data['config']['ipv6.routes']}) if 'ipv6.routes' in json_data['config'].keys() else False
              config.update({'ipv6.routing': json_data['config']['ipv6.routing']}) if 'ipv6.routing' in json_data['config'].keys() else False
              config.update({'maas.subnet.ipv4': json_data['config']['maas.subnet.ipv4']}) if 'maas.subnet.ipv4' in json_data['config'].keys() else False
              config.update({'maas.subnet.ipv6': json_data['config']['maas.subnet.ipv6']}) if 'maas.subnet.ipv6' in json_data['config'].keys() else False
              config.update({'raw.dnsmasq': json_data['config']['raw.dnsmasq']}) if 'raw.dnsmasq' in json_data['config'].keys() else False

            # Do not include parent as this is a target node specific setting
            if json_data['type'] == "macvlan" or json_data['type'] == "sriov":
              config.update({'maas.subnet.ipv4': json_data['config']['maas.subnet.ipv4']}) if 'maas.subnet.ipv4' in json_data['config'].keys() else False
              config.update({'maas.subnet.ipv6': json_data['config']['maas.subnet.ipv6']}) if 'maas.subnet.ipv6' in json_data['config'].keys() else False
              config.update({'mtu': json_data['config']['mtu']}) if 'mtu' in json_data['config'].keys() else False
              config.update({'vlan': json_data['config']['vlan']}) if 'vlan' in json_data['config'].keys() else False

            if json_data['type'] == "ovn":
              config.update({'bridge.hwaddr': json_data['config']['bridge.hwaddr']}) if 'bridge.hwaddr' in json_data['config'].keys() else False
              config.update({'bridge.mtu': json_data['config']['bridge.mtu']}) if 'bridge.mtu' in json_data['config'].keys() else False
              config.update({'dns.domain': json_data['config']['dns.domain']}) if 'dns.domain' in json_data['config'].keys() else False
              config.update({'dns.search': json_data['config']['dns.search']}) if 'dns.search' in json_data['config'].keys() else False
              config.update({'ipv4.address': json_data['config']['ipv4.address']}) if 'ipv4.address' in json_data['config'].keys() else False
              config.update({'ipv4.dhcp': json_data['config']['ipv4.dhcp']}) if 'ipv4.dhcp' in json_data['config'].keys() else False
              config.update({'ipv4.nat': json_data['config']['ipv4.nat']}) if 'ipv4.nat' in json_data['config'].keys() else False
              config.update({'ipv6.address': json_data['config']['ipv6.address']}) if 'ipv6.address' in json_data['config'].keys() else False
              config.update({'ipv6.dhcp': json_data['config']['ipv6.dhcp']}) if 'ipv6.dhcp' in json_data['config'].keys() else False
              config.update({'ipv6.dhcp.stateful': json_data['config']['ipv6.dhcp.stateful']}) if 'ipv6.dhcp.stateful' in json_data['config'].keys() else False
              config.update({'ipv6.nat': json_data['config']['ipv6.nat']}) if 'ipv6.nat' in json_data['config'].keys() else False
              config.update({'network': json_data['config']['network']}) if 'network' in json_data['config'].keys() else False

            # Do not include parent as this is a target node specific setting
            if json_data['type'] == "physical":
              config.update({'maas.subnet.ipv4': json_data['config']['maas.subnet.ipv4']}) if 'maas.subnet.ipv4' in json_data['config'].keys() else False
              config.update({'maas.subnet.ipv6': json_data['config']['maas.subnet.ipv6']}) if 'maas.subnet.ipv6' in json_data['config'].keys() else False
              config.update({'mtu': json_data['config']['mtu']}) if 'mtu' in json_data['config'].keys() else False
              config.update({'vlan': json_data['config']['vlan']}) if 'vlan' in json_data['config'].keys() else False
              config.update({'ipv4.gateway': json_data['config']['ipv4.gateway']}) if 'ipv4.gateway' in json_data['config'].keys() else False
              config.update({'ipv4.ovn.ranges': json_data['config']['ipv4.ovn.ranges']}) if 'ipv4.ovn.ranges' in json_data['config'].keys() else False
              config.update({'ipv4.routes': json_data['config']['ipv4.routes']}) if 'ipv4.routes' in json_data['config'].keys() else False
              config.update({'ipv4.routes.anycast': json_data['config']['ipv4.routes.anycast']}) if 'ipv4.routes.anycast' in json_data['config'].keys() else False
              config.update({'ipv6.gateway': json_data['config']['ipv6.gateway']}) if 'ipv6.gateway' in json_data['config'].keys() else False
              config.update({'ipv6.ovn.ranges': json_data['config']['ipv6.ovn.ranges']}) if 'ipv6.ovn.ranges' in json_data['config'].keys() else False
              config.update({'ipv6.routes': json_data['config']['ipv6.routes']}) if 'ipv6.routes' in json_data['config'].keys() else False
              config.update({'ipv6.routes.anycast': json_data['config']['ipv6.routes.anycast']}) if 'ipv6.routes.anycast' in json_data['config'].keys() else False
              config.update({'dns.nameservers': json_data['config']['dns.nameservers']}) if 'dns.nameservers' in json_data['config'].keys() else False
              config.update({'ovn.ingress.mode': json_data['config']['ovn.ingress.mode']}) if 'ovn.ingress.mode' in json_data['config'].keys() else False
              
        data.update({'config': config})
        results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
        return jsonify(results.json())
      
      # If the request was sent using the form, process it
      data = {}
      data.update({'name': request.form.get('name')}) if request.form.get('name') else False
      data.update({'description': request.form.get('description')}) if request.form.get('description') else False
      data.update({'type': request.form.get('type')}) if request.form.get('type') else False
      config = {}

      # Build configuration to send to notify cluster hosts
      if request.form.get('type') == "bridge":
        config.update({'bridge.external.interfaces': request.form.get('bridge.external.interfaces')}) if request.form.get('bridge.external.interfaces') else False

      if request.form.get('type') == "macvlan" or request.form.get('type') == "sriov" or request.form.get('type') == "physical":
        config.update({'parent': request.form.get('parent')}) if request.form.get('parent') else False
      
      data.update({'config': config})

      for member in cluster_members:
        member_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks?project=' + project + '&target=' + member['server_name']
        results = requests.post(member_url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)

      # Now lets create the network without target config options, moving the pending status to created
      config = {}

      # Do not include bridge.external.interfaces as this is a target node specific setting
      if request.form.get('type') == "bridge":
        config.update({'bridge.driver': request.form.get('bridge.driver')}) if request.form.get('bridge.driver') else False
        config.update({'bridge.hwaddr': request.form.get('bridge.hwaddr')}) if request.form.get('bridge.hwaddr') else False
        config.update({'bridge.mode': request.form.get('bridge.mode')}) if request.form.get('bridge.mode') else False
        config.update({'bridge.mtu': request.form.get('bridge.mtu')}) if request.form.get('bridge.mtu') else False
        config.update({'dns.domain': request.form.get('dns.domain')}) if request.form.get('dns.domain') else False
        config.update({'dns.mode': request.form.get('dns.mode')}) if request.form.get('dns.mode') else False
        config.update({'dns.search': request.form.get('dns.search')}) if request.form.get('dns.search') else False
        config.update({'fan.overlay.subnet': request.form.get('fan.overlay.subnet')}) if request.form.get('fan.overlay.subnet') else False
        config.update({'fan.type': request.form.get('fan.type')}) if request.form.get('fan.type') else False
        config.update({'fan.underlay.subnet': request.form.get('fan.underlay.subnet')}) if request.form.get('fan.underlay.subnet') else False
        config.update({'ipv4.address': request.form.get('ipv4.address')}) if request.form.get('ipv4.address') else False
        config.update({'ipv4.dhcp': request.form.get('ipv4.dhcp')}) if request.form.get('ipv4.dhcp') else False
        config.update({'ipv4.dhcp.expiry': request.form.get('ipv4.dhcp.expiry')}) if request.form.get('ipv4.dhcp.expiry') else False
        config.update({'ipv4.dhcp.gateway': request.form.get('ipv4.dhcp.gateway')}) if request.form.get('ipv4.dhcp.gateway') else False
        config.update({'ipv4.dhcp.ranges': request.form.get('ipv4.dhcp.ranges')}) if request.form.get('ipv4.dhcp.ranges') else False
        config.update({'ipv4.firewall': request.form.get('ipv4.firewall')}) if request.form.get('ipv4.firewall') else False
        config.update({'ipv4.nat.address': request.form.get('ipv4.nat.address')}) if request.form.get('ipv4.nat.address') else False
        config.update({'ipv4.nat': request.form.get('ipv4.nat')}) if request.form.get('ipv4.nat') else False
        config.update({'ipv4.nat.order': request.form.get('ipv4.nat.order')}) if request.form.get('ipv4.nat.order') else False
        config.update({'ipv4.ovn.ranges': request.form.get('ipv4.ovn.ranges')}) if request.form.get('ipv4.ovn.ranges') else False
        config.update({'ipv4.routes': request.form.get('ipv4.routes')}) if request.form.get('ipv4.routes') else False
        config.update({'ipv4.routing': request.form.get('ipv4.routing')}) if request.form.get('ipv4.routing') else False
        config.update({'ipv6.address': request.form.get('ipv6.address')}) if request.form.get('ipv6.address') else False
        config.update({'ipv6.dhcp': request.form.get('ipv6.dhcp')}) if request.form.get('ipv6.dhcp') else False
        config.update({'ipv6.dhcp.expiry': request.form.get('ipv6.dhcp.expiry')}) if request.form.get('ipv6.dhcp.expiry') else False
        config.update({'ipv6.dhcp.ranges': request.form.get('ipv6.dhcp.ranges')}) if request.form.get('ipv6.dhcp.ranges') else False
        config.update({'ipv6.dhcp.stateful': request.form.get('ipv6.dhcp.stateful')}) if request.form.get('ipv6.dhcp.stateful') else False
        config.update({'ipv6.firewall': request.form.get('ipv6.firewall')}) if request.form.get('ipv6.firewall') else False
        config.update({'ipv6.nat.address': request.form.get('ipv6.nat.address')}) if request.form.get('ipv6.nat.address') else False
        config.update({'ipv6.nat': request.form.get('ipv6.nat')}) if request.form.get('ipv6.nat') else False
        config.update({'ipv6.nat.order': request.form.get('ipv6.nat.order')}) if request.form.get('ipv6.nat.order') else False
        config.update({'ipv6.ovn.ranges': request.form.get('ipv6.ovn.ranges')}) if request.form.get('ipv6.ovn.ranges') else False
        config.update({'ipv6.routes': request.form.get('ipv6.routes')}) if request.form.get('ipv6.routes') else False
        config.update({'ipv6.routing': request.form.get('ipv6.routing')}) if request.form.get('ipv6.routing') else False
        config.update({'maas.subnet.ipv4': request.form.get('maas.subnet.ipv4')}) if request.form.get('maas.subnet.ipv4') else False
        config.update({'maas.subnet.ipv6': request.form.get('maas.subnet.ipv6')}) if request.form.get('maas.subnet.ipv6') else False
        config.update({'raw.dnsmasq': request.form.get('raw.dnsmasq')}) if request.form.get('raw.dnsmasq') else False

      # Do not include parent as this is a target node specific setting
      if request.form.get('type') == "macvlan" or request.form.get('type') == "sriov":
        config.update({'maas.subnet.ipv4': request.form.get('maas.subnet.ipv4')}) if request.form.get('maas.subnet.ipv4') else False
        config.update({'maas.subnet.ipv6': request.form.get('maas.subnet.ipv6')}) if request.form.get('maas.subnet.ipv6') else False
        config.update({'mtu': request.form.get('mtu')}) if request.form.get('mtu') else False
        config.update({'vlan': request.form.get('vlan')}) if request.form.get('vlan') else False

      if request.form.get('type') == "ovn":
        config.update({'bridge.hwaddr': request.form.get('bridge.hwaddr')}) if request.form.get('bridge.hwaddr') else False
        config.update({'bridge.mtu': request.form.get('bridge.mtu')}) if request.form.get('bridge.mtu') else False
        config.update({'dns.domain': request.form.get('dns.domain')}) if request.form.get('dns.domain') else False
        config.update({'dns.search': request.form.get('dns.search')}) if request.form.get('dns.search') else False
        config.update({'ipv4.address': request.form.get('ipv4.address')}) if request.form.get('ipv4.address') else False
        config.update({'ipv4.dhcp': request.form.get('ipv4.dhcp')}) if request.form.get('ipv4.dhcp') else False
        config.update({'ipv4.nat': request.form.get('ipv4.nat')}) if request.form.get('ipv4.nat') else False
        config.update({'ipv6.address': request.form.get('ipv6.address')}) if request.form.get('ipv6.address') else False
        config.update({'ipv6.dhcp': request.form.get('ipv6.dhcp')}) if request.form.get('ipv6.dhcp') else False
        config.update({'ipv6.dhcp.stateful': request.form.get('ipv6.dhcp.stateful')}) if request.form.get('ipv6.dhcp.stateful') else False
        config.update({'ipv6.nat': request.form.get('ipv6.nat')}) if request.form.get('ipv6.nat') else False
        config.update({'network': request.form.get('network')}) if request.form.get('network') else False

      # Do not include parent as this is a target node specific setting
      if request.form.get('type') == "physical":
        config.update({'maas.subnet.ipv4': request.form.get('maas.subnet.ipv4')}) if request.form.get('maas.subnet.ipv4') else False
        config.update({'maas.subnet.ipv6': request.form.get('maas.subnet.ipv6')}) if request.form.get('maas.subnet.ipv6') else False
        config.update({'mtu': request.form.get('mtu')}) if request.form.get('mtu') else False
        config.update({'vlan': request.form.get('vlan')}) if request.form.get('vlan') else False
        config.update({'ipv4.gateway': request.form.get('ipv4.gateway')}) if request.form.get('ipv4.gateway') else False
        config.update({'ipv4.ovn.ranges': request.form.get('ipv4.ovn.ranges')}) if request.form.get('ipv4.ovn.ranges') else False
        config.update({'ipv4.routes': request.form.get('ipv4.routes')}) if request.form.get('ipv4.routes') else False
        config.update({'ipv4.routes.anycast': request.form.get('ipv4.routes.anycast')}) if request.form.get('ipv4.routes.anycast') else False
        config.update({'ipv6.gateway': request.form.get('ipv6.gateway')}) if request.form.get('ipv6.gateway') else False
        config.update({'ipv6.ovn.ranges': request.form.get('ipv6.ovn.ranges')}) if request.form.get('ipv6.ovn.ranges') else False
        config.update({'ipv6.routes': request.form.get('ipv6.routes')}) if request.form.get('ipv6.routes') else False
        config.update({'ipv6.routes.anycast': request.form.get('ipv6.routes.anycast')}) if request.form.get('ipv6.routes.anycast') else False
        config.update({'dns.nameservers': request.form.get('dns.nameservers')}) if request.form.get('dns.nameservers') else False
        config.update({'ovn.ingress.mode': request.form.get('ovn.ingress.mode')}) if request.form.get('ovn.ingress.mode') else False
        
      data.update({'config': config})
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
      return jsonify(results.json())

    # If non clustered host
    else:
      # If request sent json data, forward to host
      if request.form.get('json'):
        data = request.form.get('json')
        results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
        return jsonify(results.json())

      # If the request was sent using the form, process it
      data = {}
      data.update({'name': request.form.get('name')}) if request.form.get('name') else False
      data.update({'description': request.form.get('description')}) if request.form.get('description') else False
      data.update({'type': request.form.get('type')}) if request.form.get('type') else False
      config = {}

      if request.form.get('type') == "bridge":
        config.update({'bridge.external.interfaces': request.form.get('bridge.external.interfaces')}) if request.form.get('bridge.external.interfaces') else False
        config.update({'bridge.driver': request.form.get('bridge.driver')}) if request.form.get('bridge.driver') else False
        config.update({'bridge.hwaddr': request.form.get('bridge.hwaddr')}) if request.form.get('bridge.hwaddr') else False
        config.update({'bridge.mode': request.form.get('bridge.mode')}) if request.form.get('bridge.mode') else False
        config.update({'bridge.mtu': request.form.get('bridge.mtu')}) if request.form.get('bridge.mtu') else False
        config.update({'dns.domain': request.form.get('dns.domain')}) if request.form.get('dns.domain') else False
        config.update({'dns.mode': request.form.get('dns.mode')}) if request.form.get('dns.mode') else False
        config.update({'dns.search': request.form.get('dns.search')}) if request.form.get('dns.search') else False
        config.update({'fan.overlay.subnet': request.form.get('fan.overlay.subnet')}) if request.form.get('fan.overlay.subnet') else False
        config.update({'fan.type': request.form.get('fan.type')}) if request.form.get('fan.type') else False
        config.update({'fan.underlay.subnet': request.form.get('fan.underlay.subnet')}) if request.form.get('fan.underlay.subnet') else False
        config.update({'ipv4.address': request.form.get('ipv4.address')}) if request.form.get('ipv4.address') else False
        config.update({'ipv4.dhcp': request.form.get('ipv4.dhcp')}) if request.form.get('ipv4.dhcp') else False
        config.update({'ipv4.dhcp.expiry': request.form.get('ipv4.dhcp.expiry')}) if request.form.get('ipv4.dhcp.expiry') else False
        config.update({'ipv4.dhcp.gateway': request.form.get('ipv4.dhcp.gateway')}) if request.form.get('ipv4.dhcp.gateway') else False
        config.update({'ipv4.dhcp.ranges': request.form.get('ipv4.dhcp.ranges')}) if request.form.get('ipv4.dhcp.ranges') else False
        config.update({'ipv4.firewall': request.form.get('ipv4.firewall')}) if request.form.get('ipv4.firewall') else False
        config.update({'ipv4.nat.address': request.form.get('ipv4.nat.address')}) if request.form.get('ipv4.nat.address') else False
        config.update({'ipv4.nat': request.form.get('ipv4.nat')}) if request.form.get('ipv4.nat') else False
        config.update({'ipv4.nat.order': request.form.get('ipv4.nat.order')}) if request.form.get('ipv4.nat.order') else False
        config.update({'ipv4.ovn.ranges': request.form.get('ipv4.ovn.ranges')}) if request.form.get('ipv4.ovn.ranges') else False
        config.update({'ipv4.routes': request.form.get('ipv4.routes')}) if request.form.get('ipv4.routes') else False
        config.update({'ipv4.routing': request.form.get('ipv4.routing')}) if request.form.get('ipv4.routing') else False
        config.update({'ipv6.address': request.form.get('ipv6.address')}) if request.form.get('ipv6.address') else False
        config.update({'ipv6.dhcp': request.form.get('ipv6.dhcp')}) if request.form.get('ipv6.dhcp') else False
        config.update({'ipv6.dhcp.expiry': request.form.get('ipv6.dhcp.expiry')}) if request.form.get('ipv6.dhcp.expiry') else False
        config.update({'ipv6.dhcp.ranges': request.form.get('ipv6.dhcp.ranges')}) if request.form.get('ipv6.dhcp.ranges') else False
        config.update({'ipv6.dhcp.stateful': request.form.get('ipv6.dhcp.stateful')}) if request.form.get('ipv6.dhcp.stateful') else False
        config.update({'ipv6.firewall': request.form.get('ipv6.firewall')}) if request.form.get('ipv6.firewall') else False
        config.update({'ipv6.nat.address': request.form.get('ipv6.nat.address')}) if request.form.get('ipv6.nat.address') else False
        config.update({'ipv6.nat': request.form.get('ipv6.nat')}) if request.form.get('ipv6.nat') else False
        config.update({'ipv6.nat.order': request.form.get('ipv6.nat.order')}) if request.form.get('ipv6.nat.order') else False
        config.update({'ipv6.ovn.ranges': request.form.get('ipv6.ovn.ranges')}) if request.form.get('ipv6.ovn.ranges') else False
        config.update({'ipv6.routes': request.form.get('ipv6.routes')}) if request.form.get('ipv6.routes') else False
        config.update({'ipv6.routing': request.form.get('ipv6.routing')}) if request.form.get('ipv6.routing') else False
        config.update({'maas.subnet.ipv4': request.form.get('maas.subnet.ipv4')}) if request.form.get('maas.subnet.ipv4') else False
        config.update({'maas.subnet.ipv6': request.form.get('maas.subnet.ipv6')}) if request.form.get('maas.subnet.ipv6') else False
        config.update({'raw.dnsmasq': request.form.get('raw.dnsmasq')}) if request.form.get('raw.dnsmasq') else False

      if request.form.get('type') == "macvlan" or request.form.get('type') == "sriov":
        config.update({'maas.subnet.ipv4': request.form.get('maas.subnet.ipv4')}) if request.form.get('maas.subnet.ipv4') else False
        config.update({'maas.subnet.ipv6': request.form.get('maas.subnet.ipv6')}) if request.form.get('maas.subnet.ipv6') else False
        config.update({'mtu': request.form.get('mtu')}) if request.form.get('mtu') else False
        config.update({'parent': request.form.get('parent')}) if request.form.get('parent') else False
        config.update({'vlan': request.form.get('vlan')}) if request.form.get('vlan') else False

      if request.form.get('type') == "ovn":
        config.update({'bridge.hwaddr': request.form.get('bridge.hwaddr')}) if request.form.get('bridge.hwaddr') else False
        config.update({'bridge.mtu': request.form.get('bridge.mtu')}) if request.form.get('bridge.mtu') else False
        config.update({'dns.domain': request.form.get('dns.domain')}) if request.form.get('dns.domain') else False
        config.update({'dns.search': request.form.get('dns.search')}) if request.form.get('dns.search') else False
        config.update({'ipv4.address': request.form.get('ipv4.address')}) if request.form.get('ipv4.address') else False
        config.update({'ipv4.dhcp': request.form.get('ipv4.dhcp')}) if request.form.get('ipv4.dhcp') else False
        config.update({'ipv4.nat': request.form.get('ipv4.nat')}) if request.form.get('ipv4.nat') else False
        config.update({'ipv6.address': request.form.get('ipv6.address')}) if request.form.get('ipv6.address') else False
        config.update({'ipv6.dhcp': request.form.get('ipv6.dhcp')}) if request.form.get('ipv6.dhcp') else False
        config.update({'ipv6.dhcp.stateful': request.form.get('ipv6.dhcp.stateful')}) if request.form.get('ipv6.dhcp.stateful') else False
        config.update({'ipv6.nat': request.form.get('ipv6.nat')}) if request.form.get('ipv6.nat') else False
        config.update({'network': request.form.get('network')}) if request.form.get('network') else False

      if request.form.get('type') == "physical":
        config.update({'dns.nameservers': request.form.get('dns.nameservers')}) if request.form.get('dns.nameservers') else False
        config.update({'ipv4.gateway': request.form.get('ipv4.gateway')}) if request.form.get('ipv4.gateway') else False
        config.update({'ipv4.ovn.ranges': request.form.get('ipv4.ovn.ranges')}) if request.form.get('ipv4.ovn.ranges') else False
        config.update({'ipv4.routes': request.form.get('ipv4.routes')}) if request.form.get('ipv4.routes') else False
        config.update({'ipv4.routes.anycast': request.form.get('ipv4.routes.anycast')}) if request.form.get('ipv4.routes.anycast') else False
        config.update({'ipv6.gateway': request.form.get('ipv6.gateway')}) if request.form.get('ipv6.gateway') else False
        config.update({'ipv6.ovn.ranges': request.form.get('ipv6.ovn.ranges')}) if request.form.get('ipv6.ovn.ranges') else False
        config.update({'ipv6.routes': request.form.get('ipv6.routes')}) if request.form.get('ipv6.routes') else False
        config.update({'ipv6.routes.anycast': request.form.get('ipv6.routes.anycast')}) if request.form.get('ipv6.routes.anycast') else False
        config.update({'maas.subnet.ipv4': request.form.get('maas.subnet.ipv4')}) if request.form.get('maas.subnet.ipv4') else False
        config.update({'maas.subnet.ipv6': request.form.get('maas.subnet.ipv6')}) if request.form.get('maas.subnet.ipv6') else False
        config.update({'mtu': request.form.get('mtu')}) if request.form.get('mtu') else False
        config.update({'ovn.ingress.mode': request.form.get('ovn.ingress.mode')}) if request.form.get('ovn.ingress.mode') else False
        config.update({'parent': request.form.get('parent')}) if request.form.get('parent') else False
        config.update({'vlan': request.form.get('vlan')}) if request.form.get('vlan') else False
        
      data.update({'config': config})
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_network':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_networks':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_network_managed_devices':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks?recursion=1&project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))

    networks = json.dumps(results.json())
    networks = json.loads(networks)
    networks = networks['metadata']
    network_list = []
    for network in networks:
      if network['managed']:
        network_list.append(network['name'])
    return jsonify(network_list)


  if endpoint == 'load_network':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_network':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())
