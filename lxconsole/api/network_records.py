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
def api_network_records_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_network_record':
    id = request.args.get('id')
    project = request.args.get('project')
    zone = request.args.get('zone')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-zones/' + zone + '/records?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    data.update({'description': request.form.get('description')})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_network_record':
    id = request.args.get('id')
    project = request.args.get('project')
    zone = request.args.get('zone')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-zones/' + zone + '/records/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  


  if endpoint == 'list_network_records':
    id = request.args.get('id')
    project = request.args.get('project')
    zone = request.args.get('zone')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-zones/' + zone + '/records?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-zones/' + zone + '/records?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  

  if endpoint == 'load_network_record':
    id = request.args.get('id')
    project = request.args.get('project')
    zone = request.args.get('zone')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-zones/' + zone + '/records/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  

  if endpoint == 'update_network_record':
    id = request.args.get('id')
    project = request.args.get('project')
    zone = request.args.get('zone')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-zones/' + zone + '/records/' + name + '?project=' + project
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
  