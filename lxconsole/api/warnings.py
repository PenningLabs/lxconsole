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
def api_warnings_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})

  if endpoint == 'delete_warning':
    id = request.args.get('id')
    project = request.args.get('project')
    uuid = request.form.get('uuid')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/warnings/' + uuid
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_warnings':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/warnings?recursion=1'
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/warnings'
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  

  if endpoint == 'load_warning':
    id = request.args.get('id')
    project = request.args.get('project')
    uuid = request.form.get('uuid')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/warnings/' + uuid 
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_warning':
    id = request.args.get('id')
    project = request.args.get('project')
    uuid = request.args.get('uuid')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/warnings/' + uuid
    client_cert = get_client_crt()
    client_key = get_client_key()
    
    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'status': request.form.get('status')})
    results = requests.patch(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())



