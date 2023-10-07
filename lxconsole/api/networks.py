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

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')}) if request.form.get('name') else False
    data.update({'description': request.form.get('description')}) if request.form.get('description') else False
    data.update({'type': request.form.get('type')}) if request.form.get('type') else False
    data.update({'parent': request.form.get('parent')}) if request.form.get('parent') else False
    data.update({'network': request.form.get('network')}) if request.form.get('network') else False
    data.update({'mtu': request.form.get('mtu')}) if request.form.get('mtu') else False
    data.update({'vlan': request.form.get('vlan')}) if request.form.get('vlan') else False
    
    data.update({'bridge.driver': request.form.get('bridge.driver')}) if request.form.get('bridge.driver') else False
    data.update({'bridge.external.interfaces': request.form.get('bridge.external.interfaces')}) if request.form.get('bridge.external.interfaces') else False
    data.update({'bridge.hwaddr': request.form.get('bridge.hwaddr')}) if request.form.get('bridge.hwaddr') else False
    data.update({'bridge.mode': request.form.get('bridge.mode')}) if request.form.get('bridge.mode') else False
    data.update({'bridge.mtu': request.form.get('bridge.mtu')}) if request.form.get('bridge.mtu') else False

    data.update({'dns.domain': request.form.get('dns.domain')}) if request.form.get('dns.domain') else False
    data.update({'dns.mode': request.form.get('dns.mode')}) if request.form.get('dns.mode') else False
    data.update({'dns.nameservers': request.form.get('dns.nameservers')}) if request.form.get('dns.nameservers') else False
    data.update({'dns.search': request.form.get('dns.search')}) if request.form.get('dns.search') else False

    data.update({'fan.overlay.subnet': request.form.get('fan.overlay.subnet')}) if request.form.get('fan.overlay.subnet') else False
    data.update({'fan.type': request.form.get('fan.type')}) if request.form.get('fan.type') else False
    data.update({'fan.underlay.subnet': request.form.get('fan.underlay.subnet')}) if request.form.get('fan.underlay.subnet') else False

    data.update({'ipv4.address': request.form.get('ipv4.address')}) if request.form.get('ipv4.address') else False
    data.update({'ipv4.dhcp': request.form.get('ipv4.dhcp')}) if request.form.get('ipv4.dhcp') else False
    data.update({'ipv4.dhcp.expiry': request.form.get('ipv4.dhcp.expiry')}) if request.form.get('ipv4.dhcp.expiry') else False
    data.update({'ipv4.dhcp.gateway': request.form.get('ipv4.dhcp.gateway')}) if request.form.get('ipv4.dhcp.gateway') else False
    data.update({'ipv4.dhcp.ranges': request.form.get('ipv4.dhcp.ranges')}) if request.form.get('ipv4.dhcp.ranges') else False
    data.update({'ipv4.firewall': request.form.get('ipv4.firewall')}) if request.form.get('ipv4.firewall') else False
    data.update({'ipv4.nat.address': request.form.get('ipv4.nat.address')}) if request.form.get('ipv4.nat.address') else False
    data.update({'ipv4.nat': request.form.get('ipv4.nat')}) if request.form.get('ipv4.nat') else False
    data.update({'ipv4.nat.order': request.form.get('ipv4.nat.order')}) if request.form.get('ipv4.nat.order') else False
    data.update({'ipv4.ovn.ranges': request.form.get('ipv4.ovn.ranges')}) if request.form.get('ipv4.ovn.ranges') else False
    data.update({'ipv4.gateway': request.form.get('ipv4.gateway')}) if request.form.get('ipv4.gateway') else False
    data.update({'ipv4.routes.anycast': request.form.get('ipv4.routes.anycast')}) if request.form.get('ipv4.routes.anycast') else False
    data.update({'ipv4.routes': request.form.get('ipv4.routes')}) if request.form.get('ipv4.routes') else False
    data.update({'ipv4.routing': request.form.get('ipv4.routing')}) if request.form.get('ipv4.routing') else False

    data.update({'ipv6.address': request.form.get('ipv6.address')}) if request.form.get('ipv6.address') else False
    data.update({'ipv6.dhcp': request.form.get('ipv6.dhcp')}) if request.form.get('ipv6.dhcp') else False
    data.update({'ipv6.dhcp.expiry': request.form.get('ipv6.dhcp.expiry')}) if request.form.get('ipv6.dhcp.expiry') else False
    data.update({'ipv6.dhcp.ranges': request.form.get('ipv6.dhcp.ranges')}) if request.form.get('ipv6.dhcp.ranges') else False
    data.update({'ipv6.dhcp.stateful': request.form.get('ipv6.dhcp.stateful')}) if request.form.get('ipv6.dhcp.stateful') else False
    data.update({'ipv6.firewall': request.form.get('ipv6.firewall')}) if request.form.get('ipv6.firewall') else False
    data.update({'ipv6.nat.address': request.form.get('ipv6.nat.address')}) if request.form.get('ipv6.nat.address') else False
    data.update({'ipv6.nat': request.form.get('ipv6.nat')}) if request.form.get('ipv6.nat') else False
    data.update({'ipv6.nat.order': request.form.get('ipv6.nat.order')}) if request.form.get('ipv6.nat.order') else False
    data.update({'ipv6.ovn.ranges': request.form.get('ipv6.ovn.ranges')}) if request.form.get('ipv6.ovn.ranges') else False
    data.update({'ipv6.gateway': request.form.get('ipv6.gateway')}) if request.form.get('ipv6.gateway') else False
    data.update({'ipv6.routes.anycast': request.form.get('ipv6.routes.anycast')}) if request.form.get('ipv6.routes.anycast') else False
    data.update({'ipv6.routes': request.form.get('ipv6.routes')}) if request.form.get('ipv6.routes') else False
    data.update({'ipv6.routing': request.form.get('ipv6.routing')}) if request.form.get('ipv6.routing') else False

    data.update({'maas.subnet.ipv4': request.form.get('maas.subnet.ipv4')}) if request.form.get('maas.subnet.ipv4') else False
    data.update({'maas.subnet.ipv6': request.form.get('maas.subnet.ipv6')}) if request.form.get('maas.subnet.ipv6') else False

    data.update({'raw.dnsmasq': request.form.get('raw.dnsmasq')}) if request.form.get('raw.dnsmasq') else False
    data.update({'ovn.ingress.mode': request.form.get('ovn.ingress.mode')}) if request.form.get('ovn.ingress.mode') else False

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
