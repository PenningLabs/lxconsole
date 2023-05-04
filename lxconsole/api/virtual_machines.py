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
def api_virtual_machines_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    location = request.form.get('location')
    if location == 'none':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines?project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines?target=' + location + '&project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    data.update({'description': request.form.get('description')})
    data.update({'location': request.form.get('location')})
    #data.update({'type': request.form.get('type')})
    data.update({'instance_type': request.form.get('instance_type')})
    profiles = []
    profiles.append(request.form.get('profiles'))
    data.update({'profiles': profiles})

    source = {}
    if request.form.get('image') == 'none':
      source.update({'type': request.form.get('image')})
      data.update({'source': source})
    else:
      source.update({'type': 'image'})
      source.update({'fingerprint': request.form.get('image')})
      data.update({'source': source})

    config = {}
    config.update({'boot.autostart': request.form.get('boot.autostart')}) if request.form.get('boot.autostart') else False
    config.update({'boot.autostart.delay': request.form.get('boot.autostart.delay')}) if request.form.get('boot.autostart.delay') else False
    config.update({'boot.autostart.priority': request.form.get('boot.autostart.priority')}) if request.form.get('boot.autostart.priority') else False
    config.update({'boot.host_shutdown_timeout': request.form.get('boot.host_shutdown_timeout')}) if request.form.get('boot.host_shutdown_timeout') else False
    config.update({'boot.stop.priority': request.form.get('boot.stop.priority')}) if request.form.get('boot.stop.priority') else False

    config.update({'cloud-init.network-config': request.form.get('cloud-init.network-config')}) if request.form.get('cloud-init.network-config') else False
    config.update({'cloud-init.user-data': request.form.get('cloud-init.user-data')}) if request.form.get('cloud-init.user-data') else False
    config.update({'cloud-init.vendor-data': request.form.get('cloud-init.vendor-data')}) if request.form.get('cloud-init.vendor-data') else False

    config.update({'limits.cpu': request.form.get('limits.cpu')}) if request.form.get('limits.cpu') else False
    config.update({'limits.disk.priority': request.form.get('limits.disk.priority')}) if request.form.get('limits.disk.priority') else False
    config.update({'limits.memory': request.form.get('limits.memory')}) if request.form.get('limits.memory') else False
    config.update({'limits.memory.hugepages': request.form.get('limits.memory.hugepages')}) if request.form.get('limits.memory.hugepages') else False
    config.update({'limits.network.priority': request.form.get('limits.network.priority')}) if request.form.get('limits.network.priority') else False

    config.update({'migration.stateful': request.form.get('migration.stateful')}) if request.form.get('migration.stateful') else False

    config.update({'cluster.evacuate': request.form.get('cluster.evacuate')}) if request.form.get('cluster.evacuate') else False

    config.update({'raw.apparmor': request.form.get('raw.apparmor')}) if request.form.get('raw.apparmor') else False
    config.update({'raw.qemu': request.form.get('raw.qemu')}) if request.form.get('raw.qemu') else False
    config.update({'raw.qemu.conf': request.form.get('raw.qemu.conf')}) if request.form.get('raw.qemu.conf') else False

    config.update({'security.devlxd': request.form.get('security.devlxd')}) if request.form.get('security.devlxd') else False
    config.update({'security.protection.shift': request.form.get('security.protection.shift')}) if request.form.get('security.protection.shift') else False
    config.update({'security.agent.metrics': request.form.get('security.agent.metrics')}) if request.form.get('security.agent.metrics') else False
    config.update({'security.secureboot': request.form.get('security.secureboot')}) if request.form.get('security.secureboot') else False

    config.update({'snapshots.schedule': request.form.get('snapshots.schedule')}) if request.form.get('snapshots.schedule') else False
    config.update({'snapshots.schedule.stopped': request.form.get('snapshots.schedule.stopped')}) if request.form.get('snapshots.schedule.stopped') else False
    config.update({'snapshots.pattern': request.form.get('snapshots.pattern')}) if request.form.get('snapshots.pattern') else False
    config.update({'snapshots.expiry': request.form.get('snapshots.expiry')}) if request.form.get('snapshots.expiry') else False
  
    data.update({'config': config})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_instances':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines?recursion=1&project=' + project
    elif recursion == '2':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines?recursion=2&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instances = json.dumps(results.json())
    instances = json.loads(instances)
    if recursion == '0' or recursion == '1':
      return jsonify(instances)
    i = 0
    for instance in instances['metadata']:
      if 'state' in instance.keys():
        if 'memory' in instance['state'].keys():
          if 'usage' in instance['state']['memory'].keys():
            memory = instance['state']['memory']['usage']
        if memory:
          instances['metadata'][i]['memory'] = memory
        else:
          instances['metadata'][i]['memory'] = ""

        if 'disk' in instance['state'].keys():
          if 'root' in instance['state']['disk'].keys():
            if 'usage' in instance['state']['disk']['root'].keys():
              disk = instance['state']['disk']['root']['usage']
        if disk:  
          instances['metadata'][i]['disk'] = disk
        else:
          instances['metadata'][i]['disk'] = ''

        if 'network' in instance['state'].keys():
          networks = instance['state']['network']
        if networks:
          instances['metadata'][i]['ipv4_addresses'] = []
          for network in networks.keys():
            addresses = networks[network]['addresses']
            for address in addresses:
              if address['family'] == 'inet' and address['scope'] == 'global':
                instances['metadata'][i]['ipv4_addresses'] += [ address['address'] + ' (' + network + ')' ]
          instances['metadata'][i]['ipv6_addresses'] = []
          for network in networks.keys():
            addresses = networks[network]['addresses']
            for address in addresses:
              if address['family'] == 'inet6' and address['scope'] == 'global':
                instances['metadata'][i]['ipv6_addresses'] += [ address['address'] + ' (' + network + ')' ]
        else:
          instances['metadata'][i]['ipv4_addresses'] = []
          instances['metadata'][i]['ipv6_addresses'] = []
      i += 1
    return jsonify(instances)


  if endpoint == 'load_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'change_instance_state':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    action = request.form.get('action')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/state?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = { 'action': action }
    results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'update_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/virtual-machines/' + name + '?project=' + project
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
