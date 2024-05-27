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
def api_instances_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    location = request.form.get('location')
    if location == 'none':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?target=' + location + '&project=' + project
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
    data.update({'type': request.form.get('type')})
    data.update({'instance_type': request.form.get('instance_type')})
    data.update({'profiles': request.form.getlist('profiles')})

    source = {}
    if request.form.get('image') == 'none':
      source.update({'type': request.form.get('image')})
      data.update({'source': source})
    else:
      source.update({'type': 'image'})
      source.update({'fingerprint': request.form.get('image')})
      data.update({'source': source})

    devices = {'root': {'path': '/', 'pool': request.form.get('pool'), 'type': 'disk'}}
    data.update({'devices': devices})
    
    config = {}
    #Options shared between containers and virtual machines
    config.update({'boot.autostart': request.form.get('boot.autostart')}) if request.form.get('boot.autostart') else False
    config.update({'boot.autostart.delay': request.form.get('boot.autostart.delay')}) if request.form.get('boot.autostart.delay') else False
    config.update({'boot.autostart.priority': request.form.get('boot.autostart.priority')}) if request.form.get('boot.autostart.priority') else False
    config.update({'boot.host_shutdown_timeout': request.form.get('boot.host_shutdown_timeout')}) if request.form.get('boot.host_shutdown_timeout') else False
    config.update({'boot.stop.priority': request.form.get('boot.stop.priority')}) if request.form.get('boot.stop.priority') else False
    config.update({'cloud-init.network-config': request.form.get('cloud-init.network-config')}) if request.form.get('cloud-init.network-config') else False
    config.update({'cloud-init.user-data': request.form.get('cloud-init.user-data')}) if request.form.get('cloud-init.user-data') else False
    config.update({'cloud-init.vendor-data': request.form.get('cloud-init.vendor-data')}) if request.form.get('cloud-init.vendor-data') else False
    config.update({'cluster.evacuate': request.form.get('cluster.evacuate')}) if request.form.get('cluster.evacuate') else False
    config.update({'limits.cpu': request.form.get('limits.cpu')}) if request.form.get('limits.cpu') else False
    config.update({'limits.disk.priority': request.form.get('limits.disk.priority')}) if request.form.get('limits.disk.priority') else False
    config.update({'limits.memory': request.form.get('limits.memory')}) if request.form.get('limits.memory') else False
    config.update({'limits.network.priority': request.form.get('limits.network.priority')}) if request.form.get('limits.network.priority') else False
    config.update({'raw.apparmor': request.form.get('raw.apparmor')}) if request.form.get('raw.apparmor') else False
    config.update({'security.devlxd': request.form.get('security.devlxd')}) if request.form.get('security.devlxd') else False
    config.update({'security.protection.shift': request.form.get('security.protection.shift')}) if request.form.get('security.protection.shift') else False
    config.update({'snapshots.schedule': request.form.get('snapshots.schedule')}) if request.form.get('snapshots.schedule') else False
    config.update({'snapshots.schedule.stopped': request.form.get('snapshots.schedule.stopped')}) if request.form.get('snapshots.schedule.stopped') else False
    config.update({'snapshots.pattern': request.form.get('snapshots.pattern')}) if request.form.get('snapshots.pattern') else False
    config.update({'snapshots.expiry': request.form.get('snapshots.expiry')}) if request.form.get('snapshots.expiry') else False

    #Container only options
    config.update({'limits.cpu.allowance': request.form.get('limits.cpu.allowance')}) if request.form.get('limits.cpu.allowance') else False
    config.update({'limits.cpu.priority': request.form.get('limits.cpu.priority')}) if request.form.get('limits.cpu.priority') else False
    config.update({'limits.hugepages.64KB': request.form.get('limits.hugepages.64KB')}) if request.form.get('limits.hugepages.64KB') else False
    config.update({'limits.hugepages.1MB': request.form.get('limits.hugepages.1MB')}) if request.form.get('limits.hugepages.1MB') else False
    config.update({'limits.hugepages.2MB': request.form.get('limits.hugepages.2MB')}) if request.form.get('limits.hugepages.2MB') else False
    config.update({'limits.hugepages.1GB': request.form.get('limits.hugepages.1GB')}) if request.form.get('limits.hugepages.1GB') else False
    config.update({'limits.memory.enforce': request.form.get('limits.memory.enforce')}) if request.form.get('limits.memory.enforce') else False
    config.update({'limits.memory.swap.priority': request.form.get('limits.memory.swap.priority')}) if request.form.get('limits.memory.swap.priority') else False
    config.update({'limits.memory.swap': request.form.get('limits.memory.swap')}) if request.form.get('limits.memory.swap') else False
    config.update({'limits.processes': request.form.get('limits.processes')}) if request.form.get('limits.processes') else False
    config.update({'linux.kernel_modules': request.form.get('linux.kernel_modules')}) if request.form.get('linux.kernel_modules') else False
    config.update({'migration.incremental.memory': request.form.get('migration.incremental.memory')}) if request.form.get('migration.incremental.memory') else False
    config.update({'migration.incremental.memory.goal': request.form.get('migration.incremental.memory.goal')}) if request.form.get('migration.incremental.memory.goal') else False
    config.update({'migration.incremental.memory.iterations': request.form.get('migration.incremental.memory.iterations')}) if request.form.get('migration.incremental.memory.iterations') else False
    config.update({'nvidia.driver.capabilities': request.form.get('nvidia.driver.capabilities')}) if request.form.get('nvidia.driver.capabilities') else False
    config.update({'nvidia.runtime': request.form.get('nvidia.runtime')}) if request.form.get('nvidia.runtime') else False
    config.update({'nvidia.require.cuda': request.form.get('nvidia.require.cuda')}) if request.form.get('nvidia.require.cuda') else False
    config.update({'nvidia.require.driver': request.form.get('nvidia.require.driver')}) if request.form.get('nvidia.require.driver') else False
    config.update({'raw.idmap': request.form.get('raw.idmap')}) if request.form.get('raw.idmap') else False
    config.update({'raw.lxc': request.form.get('raw.lxc')}) if request.form.get('raw.lxc') else False
    config.update({'raw.seccomp': request.form.get('raw.seccomp')}) if request.form.get('raw.seccomp') else False
    config.update({'security.devlxd': request.form.get('security.devlxd')}) if request.form.get('security.devlxd') else False
    config.update({'security.devlxd.images': request.form.get('security.devlxd.images')}) if request.form.get('security.devlxd.images') else False
    config.update({'security.idmap.base': request.form.get('security.idmap.base')}) if request.form.get('security.idmap.base') else False
    config.update({'security.idmap.isolated': request.form.get('security.idmap.isolated')}) if request.form.get('security.idmap.isolated') else False
    config.update({'security.idmap.size': request.form.get('security.idmap.size')}) if request.form.get('security.idmap.size') else False
    config.update({'security.nesting': request.form.get('security.nesting')}) if request.form.get('security.nesting') else False
    config.update({'security.privileged': request.form.get('security.privileged')}) if request.form.get('security.privileged') else False
    config.update({'security.protection.delete': request.form.get('security.protection.delete')}) if request.form.get('security.protection.delete') else False
    config.update({'security.protection.shift': request.form.get('security.protection.shift')}) if request.form.get('security.protection.shift') else False
    config.update({'security.syscalls.allow': request.form.get('security.syscalls.allow')}) if request.form.get('security.syscalls.allow') else False
    config.update({'security.syscalls.deny': request.form.get('security.syscalls.deny')}) if request.form.get('security.syscalls.deny') else False
    config.update({'security.syscalls.deny_compat': request.form.get('security.syscalls.deny_compat')}) if request.form.get('security.syscalls.deny_compat') else False
    config.update({'security.syscalls.deny_default': request.form.get('security.syscalls.deny_default')}) if request.form.get('security.syscalls.deny_default') else False
    config.update({'security.syscalls.intercept.bpf': request.form.get('security.syscalls.intercept.bpf')}) if request.form.get('security.syscalls.intercept.bpf') else False
    config.update({'security.syscalls.intercept.bpf.devices': request.form.get('security.syscalls.intercept.bpf.devices')}) if request.form.get('security.syscalls.intercept.bpf.devices') else False
    config.update({'security.syscalls.intercept.mknod': request.form.get('security.syscalls.intercept.mknod')}) if request.form.get('security.syscalls.intercept.mknod') else False
    config.update({'security.syscalls.intercept.mount': request.form.get('security.syscalls.intercept.mount')}) if request.form.get('security.syscalls.intercept.mount') else False
    config.update({'security.syscalls.intercept.mount.allowed': request.form.get('security.syscalls.intercept.mount.allowed')}) if request.form.get('security.syscalls.intercept.mount.allowed') else False
    config.update({'security.syscalls.intercept.mount.fuse': request.form.get('security.syscalls.intercept.mount.fuse')}) if request.form.get('security.syscalls.intercept.mount.fuse') else False
    config.update({'security.syscalls.intercept.mount.shift': request.form.get('security.syscalls.intercept.mount.shift')}) if request.form.get('security.syscalls.intercept.mount.shift') else False
    config.update({'security.syscalls.intercept.setxattr': request.form.get('security.syscalls.intercept.setxattr')}) if request.form.get('security.syscalls.intercept.setxattr') else False
  
    #Virtual Machine only options
    config.update({'limits.memory.hugepages': request.form.get('limits.memory.hugepages')}) if request.form.get('limits.memory.hugepages') else False
    config.update({'migration.stateful': request.form.get('migration.stateful')}) if request.form.get('migration.stateful') else False
    config.update({'raw.qemu': request.form.get('raw.qemu')}) if request.form.get('raw.qemu') else False
    config.update({'raw.qemu.conf': request.form.get('raw.qemu.conf')}) if request.form.get('raw.qemu.conf') else False
    config.update({'security.agent.metrics': request.form.get('security.agent.metrics')}) if request.form.get('security.agent.metrics') else False
    config.update({'security.secureboot': request.form.get('security.secureboot')}) if request.form.get('security.secureboot') else False

    data.update({'config': config})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_instances':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')

    if request.args.get('filter') == "container":
      filter = "type+eq+container"
    elif request.args.get('filter') == "virtual-machine":
      filter = "type+eq+virtual-machine"
    else:  
      filter = ""

    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?filter=' + filter + '&recursion=1&project=' + project
    elif recursion == '2':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?filter=' + filter + '&recursion=2&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?filter=' + filter + '&project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instances = json.dumps(results.json())
    instances = json.loads(instances)
    if recursion == '0' or recursion == '1':
      return jsonify(instances)
    i = 0
    for instance in instances['metadata']:
      instances['metadata'][i]['memory'] = ''
      instances['metadata'][i]['disk'] = ''
      instances['metadata'][i]['ipv4_addresses'] = []
      instances['metadata'][i]['ipv6_addresses'] = []

      if 'state' in instance.keys() and instance['state']:

        # Set memory information if exists
        if 'memory' in instance['state'].keys():
          if 'usage' in instance['state']['memory'].keys():
            memory = instance['state']['memory']['usage']
            if memory:
              instances['metadata'][i]['memory'] = memory

        # Set disk information if exists
        if 'disk' in instance['state'].keys():
          # instance['state']['disk'] may exists but have have any .keys()
          if instance['state']['disk'] and 'root' in instance['state']['disk'].keys():
            if 'usage' in instance['state']['disk']['root'].keys():
              disk = instance['state']['disk']['root']['usage']
              if disk:  
                instances['metadata'][i]['disk'] = disk

        # Set network information if exists
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
        instances['metadata'][i]['state'] = ''
      i += 1
    return jsonify(instances)
   

  if endpoint == 'load_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
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
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
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
