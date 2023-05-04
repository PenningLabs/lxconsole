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
def api_operations_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'delete_operation':
    id = request.args.get('id')
    project = request.args.get('project')
    operation_id = request.form.get('id')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/operations/' + operation_id + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_operations':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/operations?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/operations?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    #Convert result JSON to string
    data = json.dumps(results.json())
    #Convert to dict
    data = json.loads(data)

    #Check if running exists as metadata.key. This is needs to exist for datatables
    if "running" not in data['metadata']:
      data['metadata']['running'] = []
    
    #Check for image download tokens exist after downloading image in clustered environment
    for operation in data['metadata']['running']:
      if operation['class'] == 'token':
        if operation['description'] == 'Image download token':
          if operation['may_cancel']:
            url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/operations/' + operation['id'] + '?project=' + project
            requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))

    return jsonify(data)


  if endpoint == 'load_operation':
    id = request.args.get('id')
    project = request.args.get('project')
    operation_id = request.form.get('id')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/operations/' + operation_id + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
