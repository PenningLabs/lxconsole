from flask import jsonify, request
import json
import requests
import os
import time
from lxconsole import db
from lxconsole.models import Server
from datetime import datetime
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


def get_client_crt():
  return 'certs/client.crt'

def get_client_key():
  return 'certs/client.key'

@login_required
def api_instance_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_instance_disk_device':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    # Before applying PATCH, check to make sure device does not already exists so that we do not overwrite an existing device
    if request.form.get('name') in instance['metadata']['devices'].keys():
      return jsonify({"type": "error","error": "Unable to add new device. Device name already exists","error_code": 409,"metadata": {"error": "Unable to add new device. Device name already exists"}})
    description = instance['metadata']['description']
    data = {}
    device = {}
    device.update({'type': 'disk'})
    device.update({'pool': request.form.get('pool')}) if request.form.get('pool') else False
    device.update({'source': request.form.get('source')}) if request.form.get('source') else False
    device.update({'path': request.form.get('path')}) if request.form.get('path') else False
    device.update({'limits_read': request.form.get('limits_read')}) if request.form.get('limits_read') else False
    device.update({'limits_write': request.form.get('limits_write')}) if request.form.get('limits_write') else False
    device.update({'limits_max': request.form.get('limits_max')}) if request.form.get('limits_max') else False
    device.update({'required': request.form.get('required')}) if request.form.get('required') else False
    device.update({'read_only': request.form.get('read_only')}) if request.form.get('read_only') else False
    device.update({'size': request.form.get('size')}) if request.form.get('size') else False
    device.update({'size_state': request.form.get('size_state')}) if request.form.get('size_state') else False
    device.update({'recursive': request.form.get('recursive')}) if request.form.get('recursive') else False
    device.update({'propagation': request.form.get('propagation')}) if request.form.get('propagation') else False
    device.update({'shift': request.form.get('shift')}) if request.form.get('shift') else False
    device.update({'raw_mount_options': request.form.get('raw_mount_options')}) if request.form.get('raw_mount_options') else False
    device.update({'ceph_user_name': request.form.get('ceph_user_name')}) if request.form.get('ceph_user_name') else False
    device.update({'ceph_cluster_name': request.form.get('ceph_cluster_name')}) if request.form.get('ceph_cluster_name') else False
    device.update({'boot_priority': request.form.get('boot_priority')}) if request.form.get('boot_priority') else False

    devices = {}
    devices.update({request.form.get('name'): device})
    data.update({'description': description})
    data.update({'devices': devices})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'add_instance_gpu_device':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    # Before applying PATCH, check to make sure device does not already exists so that we do not overwrite an existing device
    if request.form.get('name') in instance['metadata']['devices'].keys():
      return jsonify({"type": "error","error": "Unable to add new device. Device name already exists","error_code": 409,"metadata": {"error": "Unable to add new device. Device name already exists"}})
    description = instance['metadata']['description']
    data = {}
    device = {}
    device.update({'type': 'gpu'})
    device.update({'gputype': request.form.get('gputype')}) if request.form.get('gputype') else False
    device.update({'vendorid': request.form.get('vendorid')}) if request.form.get('vendorid') else False
    device.update({'productid': request.form.get('productid')}) if request.form.get('productid') else False
    device.update({'id': request.form.get('id')}) if request.form.get('id') else False
    device.update({'pci': request.form.get('pci')}) if request.form.get('pci') else False
    device.update({'uid': request.form.get('uid')}) if request.form.get('uid') else False
    device.update({'gid': request.form.get('gid')}) if request.form.get('gid') else False
    device.update({'mode': request.form.get('mode')}) if request.form.get('mode') else False
    device.update({'mig.ci': request.form.get('mig.ci')}) if request.form.get('mig.ci') else False
    device.update({'mig.gi': request.form.get('mig.gi')}) if request.form.get('mig.gi') else False
    devices = {}
    devices.update({request.form.get('name'): device})
    data.update({'description': description})
    data.update({'devices': devices})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'add_instance_network_device':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    # Before applying PATCH, check to make sure device does not already exists so that we do not overwrite an existing device
    if request.form.get('name') in instance['metadata']['devices'].keys():
      return jsonify({"type": "error","error": "Unable to add new device. Device name already exists","error_code": 409,"metadata": {"error": "Unable to add new device. Device name already exists"}})
    description = instance['metadata']['description']
    data = {}
    device = {}
    device.update({'type': 'nic'})
    device.update({'nictype': request.form.get('nictype')}) if request.form.get('nictype') else False
    device.update({'parent': request.form.get('parent')}) if request.form.get('parent') else False
    device.update({'network': request.form.get('network')}) if request.form.get('network') else False
    device.update({'interface_name': request.form.get('interface_name')}) if request.form.get('interface_name') else False
    device.update({'mtu': request.form.get('mtu')}) if request.form.get('mtu') else False
    device.update({'mode': request.form.get('mode')}) if request.form.get('mode') else False
    device.update({'hwaddr': request.form.get('hwaddr')}) if request.form.get('hwaddr') else False
    device.update({'host_name': request.form.get('host_name')}) if request.form.get('host_name') else False
    device.update({'limits_ingress': request.form.get('limits_ingress')}) if request.form.get('limits_ingress') else False
    device.update({'limits_egress': request.form.get('limits_egress')}) if request.form.get('limits_egress') else False
    device.update({'limits_max': request.form.get('limits_max')}) if request.form.get('limits_max') else False
    device.update({'ipv4_address': request.form.get('ipv4_address')}) if request.form.get('ipv4_address') else False
    device.update({'ipv4_gateway': request.form.get('ipv4_gateway')}) if request.form.get('ipv4_gateway') else False
    device.update({'ipv4_host_table': request.form.get('ipv4_host_table')}) if request.form.get('ipv4_host_table') else False
    device.update({'ipv4_host_address': request.form.get('ipv4_host_address')}) if request.form.get('ipv4_host_address') else False
    device.update({'ipv4_routes': request.form.get('ipv4_routes')}) if request.form.get('ipv4_routes') else False
    device.update({'ipv4_routes_external': request.form.get('ipv4_routes_external')}) if request.form.get('ipv4_routes_external') else False
    device.update({'ipv6_address': request.form.get('ipv6_address')}) if request.form.get('ipv6_address') else False
    device.update({'ipv6_gateway': request.form.get('ipv6_gateway')}) if request.form.get('ipv6_gateway') else False
    device.update({'ipv6_host_table': request.form.get('ipv6_host_table')}) if request.form.get('ipv6_host_table') else False
    device.update({'ipv6_host_address': request.form.get('ipv6_host_address')}) if request.form.get('ipv6_host_address') else False
    device.update({'ipv6_routes': request.form.get('ipv6_routes')}) if request.form.get('ipv6_routes') else False
    device.update({'ipv6_routes_external': request.form.get('ipv6_routes_external')}) if request.form.get('ipv6_routes_external') else False
    device.update({'security_mac_filtering': request.form.get('security_mac_filtering')}) if request.form.get('security_mac_filtering') else False
    device.update({'security_ipv4_filtering': request.form.get('security_ipv4_filtering')}) if request.form.get('security_ipv4_filtering') else False
    device.update({'security_ipv6_filtering': request.form.get('security_ipv6_filtering')}) if request.form.get('security_ipv6_filtering') else False
    device.update({'maas_subnet_ipv4': request.form.get('maas_subnet_ipv4')}) if request.form.get('maas_subnet_ipv4') else False
    device.update({'maas_subnet_ipv6': request.form.get('maas_subnet_ipv6')}) if request.form.get('maas_subnet_ipv6') else False
    device.update({'boot_priority': request.form.get('boot_priority')}) if request.form.get('boot_priority') else False
    device.update({'vlan': request.form.get('vlan')}) if request.form.get('vlan') else False
    device.update({'vlan_tagged': request.form.get('vlan_tagged')}) if request.form.get('vlan_tagged') else False
    device.update({'security_port_isolation': request.form.get('security_port_isolation')}) if request.form.get('security_port_isolation') else False
    device.update({'gvrp': request.form.get('gvrp')}) if request.form.get('gvrp') else False
    device.update({'security_acls': request.form.get('security_acls')}) if request.form.get('security_acls') else False
    device.update({'security_acls_default_ingress_action': request.form.get('security_acls_default_ingress_action')}) if request.form.get('security_acls_default_ingress_action') else False
    device.update({'security_acls_default_egress_action': request.form.get('security_acls_default_egress_action')}) if request.form.get('security_acls_default_egress_action') else False
    device.update({'security_acls_default_ingress_logged': request.form.get('security_acls_default_ingress_logged')}) if request.form.get('security_acls_default_ingress_logged') else False
    device.update({'security_acls_default_egress_logged': request.form.get('security_acls_default_egress_logged')}) if request.form.get('security_acls_default_egress_logged') else False    
    devices = {}
    devices.update({request.form.get('name'): device})
    data.update({'description': description})
    data.update({'devices': devices})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'add_instance_proxy_device':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    # Before applying PATCH, check to make sure device does not already exists so that we do not overwrite an existing device
    if request.form.get('name') in instance['metadata']['devices'].keys():
      return jsonify({"type": "error","error": "Unable to add new device. Device name already exists","error_code": 409,"metadata": {"error": "Unable to add new device. Device name already exists"}})
    description = instance['metadata']['description']
    data = {}
    device = {}
    device.update({'type': 'proxy'})
    device.update({'listen': request.form.get('listen')}) if request.form.get('listen') else False
    device.update({'connect': request.form.get('connect')}) if request.form.get('connect') else False
    device.update({'bind': request.form.get('bind')}) if request.form.get('bind') else False
    device.update({'uid': request.form.get('uid')}) if request.form.get('uid') else False
    device.update({'gid': request.form.get('gid')}) if request.form.get('gid') else False
    device.update({'mode': request.form.get('mode')}) if request.form.get('mode') else False
    device.update({'nat': request.form.get('nat')}) if request.form.get('nat') else False
    device.update({'proxy_protocol': request.form.get('proxy_protocol')}) if request.form.get('proxy_protocol') else False
    device.update({'security_uid': request.form.get('security_uid')}) if request.form.get('security_uid') else False
    device.update({'security_gid': request.form.get('security_gid')}) if request.form.get('security_gid') else False
    devices = {}
    devices.update({request.form.get('name'): device})
    data.update({'description': description})
    data.update({'devices': devices})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'add_instance_unix_device':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    # Before applying PATCH, check to make sure device does not already exists so that we do not overwrite an existing device
    if request.form.get('name') in instance['metadata']['devices'].keys():
      return jsonify({"type": "error","error": "Unable to add new device. Device name already exists","error_code": 409,"metadata": {"error": "Unable to add new device. Device name already exists"}})
    description = instance['metadata']['description']
    data = {}
    device = {}
    device.update({'type': request.form.get('type')}) if request.form.get('type') else False
    device.update({'source': request.form.get('source')}) if request.form.get('source') else False
    device.update({'path': request.form.get('path')}) if request.form.get('path') else False
    device.update({'major': request.form.get('major')}) if request.form.get('major') else False
    device.update({'minor': request.form.get('minor')}) if request.form.get('minor') else False
    device.update({'uid': request.form.get('uid')}) if request.form.get('uid') else False
    device.update({'gid': request.form.get('gid')}) if request.form.get('gid') else False
    device.update({'mode': request.form.get('mode')}) if request.form.get('mode') else False
    device.update({'required': request.form.get('required')}) if request.form.get('required') else False
    devices = {}
    devices.update({request.form.get('name'): device})
    data.update({'description': description})
    data.update({'devices': devices})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())
  

  if endpoint == 'add_instance_usb_device':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    # Before applying PATCH, check to make sure device does not already exists so that we do not overwrite an existing device
    if request.form.get('name') in instance['metadata']['devices'].keys():
      return jsonify({"type": "error","error": "Unable to add new device. Device name already exists","error_code": 409,"metadata": {"error": "Unable to add new device. Device name already exists"}})
    description = instance['metadata']['description']
    data = {}
    device = {}
    device.update({'type': 'usb'})
    device.update({'vendorid': request.form.get('vendorid')}) if request.form.get('vendorid') else False
    device.update({'productid': request.form.get('productid')}) if request.form.get('productid') else False
    device.update({'uid': request.form.get('uid')}) if request.form.get('uid') else False
    device.update({'gid': request.form.get('gid')}) if request.form.get('gid') else False
    device.update({'mode': request.form.get('mode')}) if request.form.get('mode') else False
    devices = {}
    devices.update({request.form.get('name'): device})
    data.update({'description': description})
    data.update({'devices': devices})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'attach_instance_profile':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    description = instance['metadata']['description']
    data = {}
    profiles = instance['metadata']['profiles']
    if request.form.get('name') not in profiles:
      profiles.append(request.form.get('name'))
    data.update({'description': description})
    data.update({'profiles': profiles})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'change_instance_state':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.form.get('instance')
    action = request.form.get('action')
    force = request.form.get('force')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/state?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    if force == 'true':
      data = { 'action': action, 'force': True }
    else:
      data = { 'action': action, 'force': False }
    results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'copy_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    location = request.args.get('location')
    #Target location is needed for clustered servers and not allowed on non-clustered servers
    if location == 'none':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?target='+location+'&project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    data.update({'name': request.form.get('name')})
    source = {}
    source.update({'type': 'copy'})
    source.update({'source': instance })
    source.update({'project': project})
    data.update({'source': source})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'create_instance_backup':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/backups?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    
    # Determine file name
    name = request.form.get('name')
    if not name:
      now = datetime.now()
      dt_string = now.strftime("%Y%m%d%H%M%S")
      name = instance + '-' + dt_string

    # Determine file extenstion
    compression_algorithm = request.form.get('compression_algorithm')
    if compression_algorithm == 'bzip2':
      extenstion = '.tar.bz2'
    elif compression_algorithm == 'gzip':
      extenstion = '.tar.gz'
    elif compression_algorithm == 'lzma':
      extenstion = '.tar.lzma'
    elif compression_algorithm == 'xz':
      extenstion = '.tar.xz'
    elif compression_algorithm == 'zstd':
      extenstion = '.tar.zst'
    else: 
      extenstion = '.tar'

    # Append file extension to name
    name = name + extenstion

    data = {}
    data.update({'name': name})
    data.update({'instance_only': True }) if request.form.get('instance_only') == 'true' else data.update({'instance_only': False })
    data.update({'optimized_storage': True }) if request.form.get('optimized_storage') == 'true' else data.update({'optimized_storage': False })
    data.update({'compression_algorithm': request.form.get('compression_algorithm')}) if request.form.get('compression_algorithm') else False
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())
  

  if endpoint == 'create_instance_snapshot':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/snapshots?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    data.update({'name': request.form.get('name')})
    if request.form.get('stateful') == 'true':
      data.update({'stateful': True})
    else:
      data.update({'stateful': False})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'create_instance_snapshot_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    location = request.args.get('location')
    #Target location is needed for clustered servers and not allowed on non-clustered servers
    if location == 'none':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances?target='+location+'&project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    data.update({'name': request.form.get('name')})
    source = {}
    source.update({'type': 'copy'})
    source.update({'instance_only': True})
    source.update({'source': instance + '/' + request.form.get('snapshot')})
    source.update({'project': project})
    data.update({'source': source})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'delete_instance_backup':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    backup = request.args.get('backup')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/backups/' + backup + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    if os.path.isfile('backups/' + str(server.id) + '/' + project + '/' + instance + '/' + backup):
      os.unlink('backups/' + str(server.id) + '/' + project + '/' + instance + '/' + backup)
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'delete_instance_device':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    device = request.args.get('device')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    data = instance['metadata']
    data['devices'].pop(device)
    results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'delete_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.form.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'delete_instance_log':
    id = request.args.get('id')
    project = request.args.get('project')
    log = request.args.get('log')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + log + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'delete_instance_snapshot':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    snapshot = request.args.get('snapshot')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/snapshots/' + snapshot + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'detach_instance_profile':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    profile = request.args.get('profile')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    instance = instance['metadata']
    description = instance['description']
    instance_profiles = instance['profiles']
    instance_profiles.remove(profile)
    data = {}
    data.update({ 'description': description })
    data.update({ 'profiles': instance_profiles})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'display_instance_log':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    log = request.args.get('log')
    url = 'https://' + server.addr + ':' + str(server.port) + log + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return results.text
  

  if endpoint == 'establish_instance_console_websocket':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/console?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    data.update({'type': 'console'})
    data.update({'width': int(request.form.get('width'))})
    data.update({'height': int(request.form.get('height'))})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    results = json.dumps(results.json())
    results = json.loads(results)

    operation = results['operation'] if results['operation'] else ''
    secret = str(results['metadata']['metadata']['fds']['0']) if str(results['metadata']['metadata']['fds']['0']) else ''
    control = str(results['metadata']['metadata']['fds']['control']) if str(results['metadata']['metadata']['fds']['control']) else ''

    return jsonify({'operation': operation, 'secret': secret, 'control': control})
  

  if endpoint == 'establish_instance_exec_websocket':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/exec?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    if request.form.get('shell') == "sh":
        data.update({'command': ["/bin/sh"]})
    else:
        data.update({'command': ["/bin/bash"]})
    data.update({'wait-for-websocket':True})
    data.update({'interactive': True})
    data.update({'width': int(request.form.get('width'))})
    data.update({'height': int(request.form.get('height'))})
    environment = {}
    environment.update({'HOME': '/root'})
    environment.update({'TERM': 'xterm'})
    environment.update({'USER': 'root'})
    data.update({'environment': environment})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    results = json.dumps(results.json())
    results = json.loads(results)

    operation = results['operation'] if results['operation'] else ''
    secret = str(results['metadata']['metadata']['fds']['0']) if str(results['metadata']['metadata']['fds']['0']) else ''
    control = str(results['metadata']['metadata']['fds']['control']) if str(results['metadata']['metadata']['fds']['control']) else ''

    return jsonify({'operation': operation, 'secret': secret, 'control': control})
  

  if endpoint == 'export_instance_backup':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    instance = request.args.get('instance')
    backup = request.args.get('backup')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '/backups/' + backup + '/export?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    os.system('mkdir -p backups/' + str(server.id) + '/' + project + '/' + instance)
    filename = 'backups/' + str(server.id) + '/' + project + '/' + instance + '/' + backup
    with requests.get(url, stream=True, verify=server.ssl_verify, cert=(client_cert, client_key)) as r:
      r.raise_for_status()
      with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192): 
          f.write(chunk)
    return jsonify({"status": "Ok", "status_code": 200, "metadata": "{}"})


  if endpoint == 'get_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  
  # Virtual Machine only
  if endpoint == 'copy_instance_proc_stat':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')    
    client_cert = get_client_crt()
    client_key = get_client_key()

    # Unable to read /proc/stat directly on virtual machines use lxd files api...getting an EOF error
    # So we will copy /proc/stat to /tmp/stat and then read that file as a work around
    data = {}
    #data.update({'command': ['/bin/sh', '-c', 'cat /proc/stat \u003e /tmp/stat' ]})
    data.update({'command': ['cp', '/proc/stat', '/tmp/stat']})
    data.update({'wait-for-websocket': False})
    data.update({'interactive': False})
    data.update({'width': 80 })
    data.update({'height': 24 })
    data.update({'user': 0 })
    data.update({'group': 0 })
    data.update({'cwd': "/" })
    data.update({'record-output': False })
    data.update({'environment': {} })
    
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/exec?project=' + project
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())

  # Virtual Machine only
  if endpoint == 'get_instance_proc_stat':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')    
    client_cert = get_client_crt()
    client_key = get_client_key()

    #Get /proc/stat information but from /tmp/stat
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/files?project=' + project + '&path=/tmp/stat'
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    if 'cpu' in results.text:
      results = results.text.split('\n')
      for result in results:
        stats = result.split()
        if 'cpu' in stats:
          user_time = int(stats[1])
          system_time= int(stats[3])
          idle_time = int(stats[4])
          return jsonify({'user_time':user_time, 'system_time':system_time, 'idle_time':idle_time})
    return jsonify({'user_time':0, 'system_time':0, 'idle_time':1})

  # Virtual Machine only
  if endpoint == 'copy_instance_proc_meminfo':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')    
    client_cert = get_client_crt()
    client_key = get_client_key()

    # Unable to read /proc/stat directly on virtual machines use lxd files api...getting an EOF error
    # So we will copy /proc/stat to /tmp/stat and then read that file as a work around
    data = {}
    #data.update({'command': ['/bin/sh', '-c', 'cat /proc/meminfo \u003e /tmp/meminfo' ]})
    data.update({'command': ['cp', '/proc/meminfo', '/tmp/meminfo']})
    data.update({'wait-for-websocket': False})
    data.update({'interactive': False})
    data.update({'width': 80 })
    data.update({'height': 24 })
    data.update({'user': 0 })
    data.update({'group': 0 })
    data.update({'cwd': "/" })
    data.update({'record-output': False })
    data.update({'environment': {} })
    
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/exec?project=' + project
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())

  # Virtual Machine only
  if endpoint == 'get_instance_proc_meminfo':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')    
    client_cert = get_client_crt()
    client_key = get_client_key()

    #Get /proc/meminfo information but from /tmp/meminfo
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/files?project=' + project + '&path=/tmp/meminfo'
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    if 'MemTotal' in results.text:
      results = results.text.split('\n')
      mem_total = results[0].split()
      mem_available = results[2].split()
      percentage = 100 * ( 1 - ( int(mem_available[1]) / int(mem_total[1]) ) )
      return jsonify({'mem_total':int(mem_total[1]), 'mem_available':int(mem_available[1]), 'percentage':percentage})
    return jsonify({'mem_total':0, 'mem_available':0, 'percentage':0})


  if endpoint == 'get_instance_cpu_usage':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')    
    client_cert = get_client_crt()
    client_key = get_client_key()

    #Get instance state to retrieve instance cpu usage
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/state?project=' + project
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    results = json.dumps(results.json())
    results = json.loads(results)
    #Get cpu usage
    if 'cpu' in results['metadata']:
      if 'usage' in results['metadata']['cpu']:
        #Usage is reported in nanoseconds
        instance_cpu_time = int(results['metadata']['cpu']['usage'])
      else:
        instance_cpu_time = 0
    else:
      instance_cpu_time = 0

    #Get /proc/stat information
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/files?project=' + project + '&path=/proc/stat'
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    if 'cpu' in results.text:
      results = results.text.split('\n')
      for result in results:
        stats = result.split()
        if stats[0] == 'cpu':
          #0 = 'cpu'
          #1 = <user time>
          #2 = <nice time>
          #3 = <system time>
          #4 = <idle time>
          user_time = int(stats[1])
          system_time= int(stats[3])
          idle_time = int(stats[4])
          host_cpu_time = user_time + system_time + idle_time

          return jsonify({'instance_cpu_time':instance_cpu_time,'host_cpu_time': host_cpu_time})
      
    return jsonify({'instance_cpu_time':0,'host_cpu_time': 0})
  

  if endpoint == 'get_instance_disk_devices':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    expanded_devices = instance['metadata']['expanded_devices']
    devices = []
    instance_state_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/state?project=' + project
    instance_state = requests.get(instance_state_url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance_state = json.dumps(instance_state.json())
    instance_state = json.loads(instance_state)
    if expanded_devices:
      for expanded_device in expanded_devices:
        if expanded_devices[expanded_device]['type'] == 'disk':
          device = {}
          device.update({ 'device': expanded_device })
          device.update({ 'type': expanded_devices[expanded_device]['type'] })
          if 'path' in expanded_devices[expanded_device]:
            device.update({ 'path': expanded_devices[expanded_device]['path'] })
          if 'pool' in expanded_devices[expanded_device]:
            device.update({ 'pool': expanded_devices[expanded_device]['pool'] })
          if expanded_device in instance_state['metadata']['disk']:
            if 'usage' in instance_state['metadata']['disk'][expanded_device]:
              device.update({ 'usage': instance_state['metadata']['disk'][expanded_device]['usage'] })

          devices.append(device)
    return jsonify({ 'data': devices })


  if endpoint == 'get_instance_gpu_devices':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    expanded_devices = instance['metadata']['expanded_devices']
    devices = []
    if expanded_devices:
      for expanded_device in expanded_devices:
        if expanded_devices[expanded_device]['type'] == 'gpu':
          device = {}
          device.update({ 'device': expanded_device })
          device.update({ 'type': expanded_devices[expanded_device]['type'] })
          if 'gputype' in expanded_devices[expanded_device]:
            device.update({ 'gputype': expanded_devices[expanded_device]['gputype'] })
          if 'vendorid' in expanded_devices[expanded_device]:
            device.update({ 'vendorid': expanded_devices[expanded_device]['vendorid'] })
          if 'productid' in expanded_devices[expanded_device]:
            device.update({ 'productid': expanded_devices[expanded_device]['productid'] })
          if 'id' in expanded_devices[expanded_device]:
            device.update({ 'id': expanded_devices[expanded_device]['id'] })
          if 'pci' in expanded_devices[expanded_device]:
            device.update({ 'pci': expanded_devices[expanded_device]['pci'] })
          if 'uid' in expanded_devices[expanded_device]:
            device.update({ 'uid': expanded_devices[expanded_device]['uid'] })
          if 'gid' in expanded_devices[expanded_device]:
            device.update({ 'gid': expanded_devices[expanded_device]['gid'] })
          if 'mode' in expanded_devices[expanded_device]:
            device.update({ 'mode': expanded_devices[expanded_device]['mode'] })
          if 'mig.ci' in expanded_devices[expanded_device]:
            device.update({ 'mig.ci': expanded_devices[expanded_device]['mig.ci'] })
          if 'mig.gi' in expanded_devices[expanded_device]:
            device.update({ 'mig.gi': expanded_devices[expanded_device]['mig.gi'] })
          devices.append(device)
    return jsonify({ 'data': devices })


  if endpoint == 'get_instance_interfaces':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/state?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/state?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    networks = instance['metadata']['network']
    interfaces = []
    if networks:
      for network in networks:
        if network:
          interface = {}
          interface.update({ 'name': network })
          interface.update({ 'hwaddr': networks[network]['hwaddr'] })
          interface.update({ 'state': networks[network]['state'] })
          addresses = networks[network]['addresses']
          interface.update({ 'ipv4_addresses': [] })
          interface.update({ 'ipv6_addresses': [] })
          for address in addresses:
            #if address['family'] == 'inet' and address['scope'] == 'global':
            if address['family'] == 'inet':
              interface['ipv4_addresses'] += [ address['address'] ]
            if address['family'] == 'inet6':
              interface['ipv6_addresses'] += [ address['address'] ]
          interfaces.append(interface)
    return jsonify({ 'data': interfaces })


  if endpoint == 'get_instance_network_devices':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    expanded_devices = instance['metadata']['expanded_devices']
    devices = []
    if expanded_devices:
      for expanded_device in expanded_devices:
        if expanded_devices[expanded_device]['type'] == 'nic':
          device = {}
          device.update({ 'device': expanded_device })
          device.update({ 'type': expanded_devices[expanded_device]['type'] })
          if 'name' in expanded_devices[expanded_device]:
            device.update({ 'name': expanded_devices[expanded_device]['name'] })
          if 'network' in expanded_devices[expanded_device]:
            device.update({ 'network': expanded_devices[expanded_device]['network'] })
          if 'nictype' in expanded_devices[expanded_device]:
            device.update({ 'nictype': expanded_devices[expanded_device]['nictype'] })
          if 'parent' in expanded_devices[expanded_device]:
            device.update({ 'parent': expanded_devices[expanded_device]['parent'] })
          devices.append(device)
    return jsonify({ 'data': devices })


  if endpoint == 'get_instance_proxy_devices':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    expanded_devices = instance['metadata']['expanded_devices']
    devices = []
    if expanded_devices:
      for expanded_device in expanded_devices:
        if expanded_devices[expanded_device]['type'] == 'proxy':
          device = {}
          device.update({ 'device': expanded_device })
          device.update({ 'type': expanded_devices[expanded_device]['type'] })
          if 'connect' in expanded_devices[expanded_device]:
            device.update({ 'connect': expanded_devices[expanded_device]['connect'] })
          if 'listen' in expanded_devices[expanded_device]:
            device.update({ 'listen': expanded_devices[expanded_device]['listen'] })
          devices.append(device)
    return jsonify({ 'data': devices })


  if endpoint == 'get_instance_state':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/state?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/state?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())

  # Container only
  if endpoint == 'get_instance_unix_devices':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    expanded_devices = instance['metadata']['expanded_devices']
    devices = []
    if expanded_devices:
      for expanded_device in expanded_devices:
        if expanded_devices[expanded_device]['type'] == 'unix-block' or expanded_devices[expanded_device]['type'] == 'unix-char':
          device = {}
          device.update({ 'device': expanded_device })
          device.update({ 'type': expanded_devices[expanded_device]['type'] })
          if 'source' in expanded_devices[expanded_device]:
            device.update({ 'source': expanded_devices[expanded_device]['source'] })
          if 'path' in expanded_devices[expanded_device]:
            device.update({ 'path': expanded_devices[expanded_device]['path'] })
          if 'major' in expanded_devices[expanded_device]:
            device.update({ 'major': expanded_devices[expanded_device]['major'] })
          if 'minor' in expanded_devices[expanded_device]:
            device.update({ 'minor': expanded_devices[expanded_device]['minor'] })
          if 'uid' in expanded_devices[expanded_device]:
            device.update({ 'uid': expanded_devices[expanded_device]['uid'] })
          if 'gid' in expanded_devices[expanded_device]:
            device.update({ 'gid': expanded_devices[expanded_device]['gid'] })
          if 'mode' in expanded_devices[expanded_device]:
            device.update({ 'mode': expanded_devices[expanded_device]['mode'] })
          if 'required' in expanded_devices[expanded_device]:
            device.update({ 'required': expanded_devices[expanded_device]['required'] })
          devices.append(device)
    return jsonify({ 'data': devices })


  if endpoint == 'get_instance_usb_devices':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    expanded_devices = instance['metadata']['expanded_devices']
    devices = []
    if expanded_devices:
      for expanded_device in expanded_devices:
        if expanded_devices[expanded_device]['type'] == 'usb':
          device = {}
          device.update({ 'device': expanded_device })
          device.update({ 'type': expanded_devices[expanded_device]['type'] })
          if 'vendorid' in expanded_devices[expanded_device]:
            device.update({ 'vendorid': expanded_devices[expanded_device]['vendorid'] })
          if 'productid' in expanded_devices[expanded_device]:
            device.update({ 'productid': expanded_devices[expanded_device]['productid'] })
          if 'uid' in expanded_devices[expanded_device]:
            device.update({ 'uid': expanded_devices[expanded_device]['uid'] })
          if 'gid' in expanded_devices[expanded_device]:
            device.update({ 'gid': expanded_devices[expanded_device]['gid'] })
          if 'mode' in expanded_devices[expanded_device]:
            device.update({ 'mode': expanded_devices[expanded_device]['mode'] })
          if 'required' in expanded_devices[expanded_device]:
            device.update({ 'required': expanded_devices[expanded_device]['required'] })
          devices.append(device)
    return jsonify({ 'data': devices })


  if endpoint == 'get_instance_websocket_host':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    return jsonify({ 'addr': server.addr, 'port': server.port, 'proxy': server.proxy })
  

  if endpoint == 'list_instance_backups':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/backups?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/backups?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    backups = json.dumps(results.json())
    backups = json.loads(backups)
    devices = []
    if backups:
      for backup in backups['metadata']:
        # Check if backup file exists
        if os.path.isfile('backups/' + str(server.id) + '/' + project + '/' + name + '/' + backup['name']):
          backup.update({'backup_file_exists': True})
          backup.update({'backup_file_size': os.path.getsize('backups/' + str(server.id) + '/' + project + '/' + name + '/' + backup['name'])})
        else:
          backup.update({'backup_file_exists': False})

    return jsonify(backups)


  if endpoint == 'list_instance_logs':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/logs?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/logs?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    
    # Newly created VMs will not have logs until it starts, causing a 404 error
    results = json.dumps(results.json())
    results = json.loads(results)
    if results['metadata'] is None:
      return jsonify({"metadata":[]})
    return jsonify(results)


  if endpoint == 'list_instance_snapshots':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/snapshots?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + name + '/snapshots?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'migrate_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    location = request.args.get('location')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?target='+location+'&project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    data.update({'name': instance })
    data.update({'migration': True})
    data.update({'live': False})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'publish_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    properties = {}
    properties.update({ 'description':request.form.get('description') })
    properties.update({ 'os': request.form.get('os') })
    properties.update({ 'release': request.form.get('release') })
    data.update({ 'properties': properties })
    source = {}
    source.update({ 'type': 'instance' })
    source.update({ 'name': instance })
    data.update({ 'source': source })
    if request.form.get('public') == 'true':
      data.update({'public': True})
    else:
      data.update({'public': False})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'publish_instance_snapshot':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    snapshot = request.args.get('snapshot')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    data = {}
    properties = {}
    properties.update({ 'description':request.form.get('description') })
    properties.update({ 'os': request.form.get('os') })
    properties.update({ 'release': request.form.get('release') })
    data.update({ 'properties': properties })
    source = {}
    source.update({ 'type': 'snapshot' })
    source.update({ 'name': instance + '/' + snapshot })
    data.update({ 'source': source })
    if request.form.get('public') == 'true':
      data.update({'public': True})
    else:
      data.update({'public': False})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'rename_instance':
      id = request.args.get('id')
      project = request.args.get('project')
      instance = request.args.get('instance')
      server = Server.query.filter_by(id=id).first()
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
      client_cert = get_client_crt()
      client_key = get_client_key()
      data = {}
      data.update({'name': request.form.get('name')})
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
      return jsonify(results.json())


  if endpoint == 'restore_instance_snapshot':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    data = {}
    data.update({'restore': request.form.get('name')})
    results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'update_instance':
    id = request.args.get('id')
    project = request.args.get('project')
    instance = request.args.get('instance')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/instances/' + instance + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    # If the update was from JSON tab, update it with a PUT request
    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    # Get the current config
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    instance = json.dumps(results.json())
    instance = json.loads(instance)
    existing_config = instance['metadata']['config']
 
    # Create a new dict to hold the differences between existing config and form config
    updated_config = {}
    # Loop through and compare differences between existing config and form config
    for key, val in request.form.items():
      # If key is description, continue as it is not part of config
      if key == 'description':
        continue
      # If the key does not exist in existing config, create and set it to empty string so we can compare it to form config
      if not key in existing_config:
        existing_config.update( { key: '' } )
      # If the post key is different than existing key capture this difference in new dict
      if request.form.get(key) != existing_config[key]:
        updated_config.update({key: request.form.get(key)})

    # Send a PATCH request to update only the differences in config
    data = {}
    data.update({'description': request.form.get('description')})
    data.update({'config' : updated_config })
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())
