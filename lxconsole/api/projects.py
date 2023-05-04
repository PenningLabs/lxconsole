from flask import jsonify, request
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
def api_projects_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_project':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/projects?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    
    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    data.update({'description': request.form.get('description')})
    config = {}
    config.update({'features.images': request.form.get('features.images')}) if request.form.get('features.images') else False
    config.update({'features.networks': request.form.get('features.networks')}) if request.form.get('features.networks') else False
    config.update({'features.profiles': request.form.get('features.profiles')}) if request.form.get('features.profiles') else False
    config.update({'features.storage.volumes': request.form.get('features.storage.volumes')}) if request.form.get('features.storage.volumes') else False
    config.update({'features.storage.buckets': request.form.get('features.storage.buckets')}) if request.form.get('features.storage.buckets') else False

    config.update({'features.backups.compression_algorithm': request.form.get('features.backups.compression_algorithm')}) if request.form.get('features.backups.compression_algorithm') else False
    config.update({'features.images.auto_update_cached': request.form.get('features.images.auto_update_cached')}) if request.form.get('features.images.auto_update_cached') else False
    config.update({'features.images.auto_update_interval': request.form.get('features.images.auto_update_interval')}) if request.form.get('features.images.auto_update_interval') else False
    config.update({'features.images.compression_algorithm': request.form.get('features.images.compression_algorithm')}) if request.form.get('features.images.compression_algorithm') else False
    config.update({'features.images.default_architecture': request.form.get('features.images.default_architecture')}) if request.form.get('features.images.default_architecture') else False
    config.update({'features.images.remote_cache_expiry': request.form.get('features.images.remote_cache_expiry')}) if request.form.get('features.images.remote_cache_expiry') else False
    config.update({'features.limits.containers': request.form.get('features.limits.containers')}) if request.form.get('features.limits.containers') else False
    config.update({'features.limits.cpu': request.form.get('features.limits.cpu')}) if request.form.get('features.limits.cpu') else False
    config.update({'features.limits.disk': request.form.get('features.limits.disk')}) if request.form.get('features.limits.disk') else False
    config.update({'features.limits.instances': request.form.get('features.limits.instances')}) if request.form.get('features.limits.instances') else False
    config.update({'features.limits.memory': request.form.get('features.limits.memory')}) if request.form.get('features.limits.memory') else False
    config.update({'features.limits.networks': request.form.get('features.limits.networks')}) if request.form.get('features.limits.networks') else False
    config.update({'features.limits.processes': request.form.get('features.limits.processes')}) if request.form.get('features.limits.processes') else False
    config.update({'features.limits.virtual-machines': request.form.get('features.limits.virtual-machines')}) if request.form.get('features.limits.virtual-machines') else False

    restricted = config.update({'restricted': request.form.get('restricted')}) if request.form.get('restricted') else False
    if restricted:
      config.update({'restricted.backups': request.form.get('restricted.backups')}) if request.form.get('restricted.backups') else False
      config.update({'restricted.cluster.target': request.form.get('restricted.cluster.target')}) if request.form.get('restricted.cluster.target') else False
      config.update({'restricted.containers.lowlevel': request.form.get('restricted.containers.lowlevel')}) if request.form.get('restricted.containers.lowlevel') else False
      config.update({'restricted.containers.nesting': request.form.get('restricted.containers.nesting')}) if request.form.get('restricted.containers.nesting') else False
      config.update({'restricted.containers.privilege': request.form.get('restricted.containers.privilege')}) if request.form.get('restricted.containers.privilege') else False
      config.update({'restricted.devices.disk': request.form.get('restricted.devices.disk')}) if request.form.get('restricted.devices.disk') else False
      config.update({'restricted.devices.gpu': request.form.get('restricted.devices.gpu')}) if request.form.get('restricted.devices.gpu') else False
      config.update({'restricted.devices.infiniband': request.form.get('restricted.devices.infiniband')}) if request.form.get('restricted.devices.infiniband') else False
      config.update({'restricted.devices.nic': request.form.get('restricted.devices.nic')}) if request.form.get('restricted.devices.nic') else False
      config.update({'restricted.devices.pci': request.form.get('restricted.devices.pci')}) if request.form.get('restricted.devices.pci') else False
      config.update({'restricted.devices.proxy': request.form.get('restricted.devices.proxy')}) if request.form.get('restricted.devices.proxy') else False
      config.update({'restricted.devices.unix-block': request.form.get('restricted.devices.unix-block')}) if request.form.get('restricted.devices.unix-block') else False
      config.update({'restricted.devices.unix-char': request.form.get('restricted.devices.unix-char')}) if request.form.get('restricted.devices.unix-char') else False
      config.update({'restricted.devices.unix-hotplug': request.form.get('restricted.devices.unix-hotplug')}) if request.form.get('restricted.devices.unix-hotplug') else False
      config.update({'restricted.devices.usb': request.form.get('restricted.devices.usb')}) if request.form.get('restricted.devices.usb') else False
      config.update({'restricted.networks.subnets': request.form.get('restricted.networks.subnets')}) if request.form.get('restricted.networks.subnets') else False
      config.update({'restricted.networks.uplinks': request.form.get('restricted.networks.uplinks')}) if request.form.get('restricted.networks.uplinks') else False
      config.update({'restricted.snapshots': request.form.get('restricted.snapshots')}) if request.form.get('restricted.snapshots') else False
      config.update({'restricted.virtual-machines.lowlevel': request.form.get('restricted.virtual-machines.lowlevel')}) if request.form.get('restricted.virtual-machines.lowlevel') else False
  
    data.update({'config': config})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_project':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/projects/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_projects':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/projects?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/projects?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'load_project':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/projects/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_project':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/projects/' + name + '?project=' + project
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
