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
def api_cluster_groups_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_cluster_group':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/groups?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    data.update({'description': request.form.get('description')})
    data.update({'members': request.form.getlist('members')})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_cluster_group':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/groups/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  

  if endpoint == 'is_cluster_member_enabled':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    data = results.json()['metadata']
    return str(data['enabled'])


  if endpoint == 'list_cluster_groups':
    if api_cluster_groups_endpoint('is_cluster_member_enabled') == 'True':
      id = request.args.get('id')
      project = request.args.get('project')
      server = Server.query.filter_by(id=id).first()
      recursion = request.args.get('recursion')
      if recursion == '1':
        url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/groups?recursion=1&project=' + project
      else:
        url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/groups?project=' + project
      client_cert = get_client_crt()
      client_key = get_client_key()
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
      return jsonify(results.json())
    data = { "metadata": []}
    return jsonify(data)
  

  if endpoint == 'load_cluster_group':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/groups/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  

  if endpoint == 'update_cluster_group':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/groups/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    if request.form.get('name'):
      data = {}
      data.update({'name': request.form.get('name')})
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
      return jsonify(results.json())
    return False
  