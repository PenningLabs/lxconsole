from flask import jsonify, request, json
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
def api_storage_pools_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_storage_pool':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    # at this point check to see if parf of a cluster, if so, send this data to each server
    cluster_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster?project=' + project
    results = requests.get(cluster_url, verify=server.ssl_verify, cert=(client_cert, client_key))
    cluster = results.json()['metadata']
      
    if request.form.get('json'):
      json_data = request.form.get('json')
      json_data = json.loads(json_data)
      data = {}
      data.update({'name': json_data['name']})
      data.update({'description': json_data['description']})
      data.update({'driver': json_data['driver']})
      config = {}
     
      if 'source' in json_data['config'].keys():
        config.update({'source': json_data['config']['source']})

      if 'driver' in json_data['config'].keys():
        if json_data['config']['driver'] == 'btrfs':
          if 'size' in json_data['config'].keys():
            config.update({'size': str(json_data['config']['size'])})

        if json_data['config']['driver'] == 'lvm':
          if 'size' in json_data['config'].keys():
            config.update({'size': str(json_data['config']['size'])})
        
        if json_data['config']['driver'] == 'zfs':
          if 'size' in json_data['config'].keys():
            config.update({'size': str(json_data['config']['size'])})
          if 'zfs.pool_name' in json_data['config'].keys():
            config.update({'size': str(json_data['config']['size'])})
            config.update({'zfs.pool_name': json_data['config']['zfs.pool_name']})


      if cluster['enabled']:  
        # Send target server specific config parameters if clustered to each member
        data.update({'config': config})
        cluster_members_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/members?recursion=1&project=' + project
        results = requests.get(cluster_members_url, verify=server.ssl_verify, cert=(client_cert, client_key))
        cluster_members = results.json()['metadata']
        for member in cluster_members:
          member_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools?project=' + project + '&target=' + member['server_name']
          results = requests.post(member_url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)

        # Remove target server specific config parameters if clustered
          if 'source' in json_data['config'].keys():
            json_data['config'].pop('source')
          if 'size' in json_data['config'].keys():
            json_data['config'].pop('size')
          if 'zfs.pool_name' in json_data['config'].keys():
            json_data['config'].pop('zfs.pool_name')

      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=json_data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    data.update({'description': request.form.get('description')})
    data.update({'driver': request.form.get('driver')})
    config = {}
    config.update({'source': request.form.get('source')}) if request.form.get('source') else False

    if request.form.get('driver') == 'btrfs':
      config.update({'size': request.form.get('size')}) if request.form.get('size') else False

    if request.form.get('driver') == 'lvm':
      config.update({'size': request.form.get('size')}) if request.form.get('size') else False

    if request.form.get('driver') == 'zfs':
      config.update({'size': request.form.get('size')}) if request.form.get('size') else False
      config.update({'zfs.pool_name': request.form.get('zfs.pool_name')}) if request.form.get('zfs.pool_name') else False

    if cluster['enabled']:
      # Send target server specific config parameters if clustered to each member
      data.update({'config': config})
      cluster_members_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/members?recursion=1&project=' + project
      results = requests.get(cluster_members_url, verify=server.ssl_verify, cert=(client_cert, client_key))
      cluster_members = results.json()['metadata']
      for member in cluster_members:
        member_url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools?project=' + project + '&target=' + member['server_name']
        results = requests.post(member_url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
   
    if request.form.get('driver') == 'btrfs':
      config.update({'btrfs.mount_options': request.form.get('btrfs.mount_options')}) if request.form.get('btrfs.mount_options') else False
      config.update({'rsync.bwlimit': request.form.get('rsync.bwlimit')}) if request.form.get('rsync.bwlimit') else False
      config.update({'rsync.compression': request.form.get('rsync.compression')}) if request.form.get('rsync.compression') else False
      config.update({'volatile.initial_source': request.form.get('volatile.initial_source')}) if request.form.get('volatile.initial_source') else False
      config.update({'volume.size': request.form.get('volume.size')}) if request.form.get('volume.size') else False

    if request.form.get('driver') == 'ceph':
      config.update({'ceph.cluster_name': request.form.get('ceph.cluster_name')}) if request.form.get('ceph.cluster_name') else False
      config.update({'ceph.osd.force_reuse': request.form.get('ceph.osd.force_reuse')}) if request.form.get('ceph.osd.force_reuse') else False
      config.update({'ceph.osd.pg_num': request.form.get('ceph.osd.pg_num')}) if request.form.get('ceph.osd.pg_num') else False
      config.update({'ceph.osd.pool_name': request.form.get('ceph.osd.pool_name')}) if request.form.get('ceph.osd.pool_name') else False
      config.update({'ceph.osd.data_pool_name': request.form.get('ceph.osd.data_pool_name')}) if request.form.get('ceph.osd.data_pool_name') else False
      config.update({'ceph.rbd.clone_copy': request.form.get('ceph.rbd.clone_copy')}) if request.form.get('ceph.rbd.clone_copy') else False
      config.update({'ceph.rbd.features': request.form.get('ceph.rbd.features')}) if request.form.get('ceph.rbd.features') else False
      config.update({'ceph.user.name': request.form.get('ceph.user.name')}) if request.form.get('ceph.user.name') else False
      config.update({'rsync.bwlimit': request.form.get('rsync.bwlimit')}) if request.form.get('rsync.bwlimit') else False
      config.update({'rsync.compression': request.form.get('rsync.compression')}) if request.form.get('rsync.compression') else False
      config.update({'volatile.initial_source': request.form.get('volatile.initial_source')}) if request.form.get('volatile.initial_source') else False
      config.update({'volatile.pool.pristine': request.form.get('volatile.pool.pristine')}) if request.form.get('volatile.pool.pristine') else False
      config.update({'volume.block.filesystem': request.form.get('volume.block.filesystem')}) if request.form.get('volume.block.filesystem') else False
      config.update({'volume.block.mount_options': request.form.get('volume.block.mount_options')}) if request.form.get('volume.block.mount_options') else False
      config.update({'volume.size': request.form.get('volume.size')}) if request.form.get('volume.size') else False

    if request.form.get('driver') == 'cephfs':
      config.update({'cephfs.cluster_name': request.form.get('cephfs.cluster_name')}) if request.form.get('cephfs.cluster_name') else False
      config.update({'cephfs.path': request.form.get('cephfs.path')}) if request.form.get('cephfs.path') else False
      config.update({'cephfs.user.name': request.form.get('cephfs.user.name')}) if request.form.get('cephfs.user.name') else False

      #Additional options that may or may not be used in cephfs, need to test
      config.update({'rsync.bwlimit': request.form.get('rsync.bwlimit')}) if request.form.get('rsync.bwlimit') else False
      config.update({'rsync.compression': request.form.get('rsync.compression')}) if request.form.get('rsync.compression') else False
      config.update({'volatile.initial_source': request.form.get('volatile.initial_source')}) if request.form.get('volatile.initial_source') else False
      config.update({'volatile.pool.pristine': request.form.get('volatile.pool.pristine')}) if request.form.get('volatile.pool.pristine') else False
      config.update({'volume.block.filesystem': request.form.get('volume.block.filesystem')}) if request.form.get('volume.block.filesystem') else False
      config.update({'volume.block.mount_options': request.form.get('volume.block.mount_options')}) if request.form.get('volume.block.mount_options') else False
      config.update({'volume.size': request.form.get('volume.size')}) if request.form.get('volume.size') else False

    if request.form.get('driver') == 'dir':
      config.update({'rsync.bwlimit': request.form.get('rsync.bwlimit')}) if request.form.get('rsync.bwlimit') else False
      config.update({'rsync.compression': request.form.get('rsync.compression')}) if request.form.get('rsync.compression') else False
      config.update({'volatile.initial_source': request.form.get('volatile.initial_source')}) if request.form.get('volatile.initial_source') else False
      config.update({'volume.size': request.form.get('volume.size')}) if request.form.get('volume.size') else False

    if request.form.get('driver') == 'lvm':
      config.update({'lvm.thinpool_name': request.form.get('lvm.thinpool_name')}) if request.form.get('lvm.thinpool_name') else False
      config.update({'lvm.use_thinpool': request.form.get('lvm.use_thinpool')}) if request.form.get('lvm.use_thinpool') else False
      config.update({'lvm.vg_name': request.form.get('lvm.vg_name')}) if request.form.get('lvm.vg_name') else False
      config.update({'lvm.vg.force_reuse': request.form.get('lvm.vg.force_reuse')}) if request.form.get('lvm.vg.force_reuse') else False
      config.update({'volume.lvm.stripes': request.form.get('volume.lvm.stripes')}) if request.form.get('volume.lvm.stripes') else False
      config.update({'volume.lvm.stripes.size': request.form.get('volume.lvm.stripes.size')}) if request.form.get('volume.lvm.stripes.size') else False
      config.update({'rsync.bwlimit': request.form.get('rsync.bwlimit')}) if request.form.get('rsync.bwlimit') else False
      config.update({'rsync.compression': request.form.get('rsync.compression')}) if request.form.get('rsync.compression') else False
      config.update({'volatile.initial_source': request.form.get('volatile.initial_source')}) if request.form.get('volatile.initial_source') else False
      config.update({'volume.block.filesystem': request.form.get('volume.block.filesystem')}) if request.form.get('volume.block.filesystem') else False
      config.update({'volume.block.mount_options': request.form.get('volume.block.mount_options')}) if request.form.get('volume.block.mount_options') else False
      config.update({'volume.size': request.form.get('volume.size')}) if request.form.get('volume.size') else False

    if request.form.get('driver') == 'zfs':
      config.update({'volume.zfs.remove_snapshots': request.form.get('volume.zfs.remove_snapshots')}) if request.form.get('volume.zfs.remove_snapshots') else False
      config.update({'volume.zfs.use_refquota': request.form.get('volume.zfs.use_refquota')}) if request.form.get('volume.zfs.use_refquota') else False
      config.update({'zfs.clone_copy': request.form.get('zfs.clone_copy')}) if request.form.get('zfs.clone_copy') else False
      config.update({'rsync.bwlimit': request.form.get('rsync.bwlimit')}) if request.form.get('rsync.bwlimit') else False
      config.update({'rsync.compression': request.form.get('rsync.compression')}) if request.form.get('rsync.compression') else False
      config.update({'volatile.initial_source': request.form.get('volatile.initial_source')}) if request.form.get('volatile.initial_source') else False
      config.update({'volume.size': request.form.get('volume.size')}) if request.form.get('volume.size') else False

    # Remove target server specific config parameters if clustered
    if cluster['enabled']:
      if 'source' in config.keys():
        config.pop('source')
      if 'size' in config.keys():
        config.pop('size')
      if 'zfs.pool_name' in config.keys():
        config.pop('zfs.pool_name')

    data.update({'config': config})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_storage_pool':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_storage_pools':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  

  if endpoint == 'load_storage_pool':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_storage_pool':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + name + '?project=' + project
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
