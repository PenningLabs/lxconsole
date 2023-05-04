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
def api_storage_volumes_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_storage_volume':
    id = request.args.get('id')
    project = request.args.get('project')
    pool = request.args.get('pool')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + pool + '/volumes?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    data.update({'description': request.form.get('description')})
    data.update({'type': request.form.get('type')})
    data.update({'content_type': request.form.get('content_type')})
    config = {}
    config.update({'size': request.form.get('size')}) if request.form.get('size') else False
    config.update({'block.filesystem': request.form.get('block.filesystem')}) if request.form.get('block.filesystem') else False
    config.update({'block.mount_options': request.form.get('block.mount_options')}) if request.form.get('block.mount_options') else False
    config.update({'security.shifted': request.form.get('security.shifted')}) if request.form.get('security.shifted') else False
    config.update({'security.unmapped': request.form.get('security.unmapped')}) if request.form.get('security.unmapped') else False
    config.update({'lvm.stripes': request.form.get('lvm.stripes')}) if request.form.get('lvm.stripes') else False
    config.update({'lvm.stripes.size': request.form.get('lvm.stripes.size')}) if request.form.get('lvm.stripes.size') else False
    config.update({'snapshots.expiry': request.form.get('snapshots.expiry')}) if request.form.get('snapshots.expiry') else False
    config.update({'snapshots.schedule': request.form.get('snapshots.schedule')}) if request.form.get('snapshots.schedule') else False
    config.update({'snapshots.pattern': request.form.get('snapshots.pattern')}) if request.form.get('snapshots.pattern') else False
    config.update({'zfs.remove_snapshots': request.form.get('zfs.remove_snapshots')}) if request.form.get('zfs.remove_snapshots') else False
    config.update({'zfs.use_refquota': request.form.get('zfs.use_refquota')}) if request.form.get('zfs.use_refquota') else False
    
    data.update({'config': config})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_storage_volume':
    id = request.args.get('id')
    project = request.args.get('project')
    pool = request.args.get('pool')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + pool + '/volumes/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_storage_volumes':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    pool  = request.args.get('pool')
    recursion = request.args.get('recursion')

    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + pool + '/volumes?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + pool + '/volumes?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'load_storage_volume':
    id = request.args.get('id')
    project = request.args.get('project')
    pool = request.args.get('pool')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
   
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + pool + '/volumes/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_storage_volume':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    pool = request.args.get('pool')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/storage-pools/' + pool + '/volumes/' + name + '?project=' + project
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
