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
def api_server_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'get_server_initial_project':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/projects'
    client_cert = get_client_crt()
    client_key = get_client_key()

    try:
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    except requests.exceptions.RequestException as err:
      return jsonify({'error': str(err)})
    
    results=results.json()
    
    if results['error_code'] > 400:
      return jsonify({'error':results['error']})

    for result in results['metadata']:
      result = result.replace('/1.0/projects/', '')
      if result == 'default':
        project = 'default'
        break
      project = result
    return project


  if endpoint == 'get_server_info':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0'
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    results = results.json()
    
    #If server_name does not match database name, update db name
    if results['metadata']['environment']['server_name'] != server.name:
      server.name = results['metadata']['environment']['server_name']
      db.session.commit()
    return jsonify(results)


  if endpoint == 'get_server_resources':
      id = request.args.get('id')
      server = Server.query.filter_by(id=id).first()
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/resources'
      client_cert = get_client_crt()
      client_key = get_client_key()
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
      return jsonify(results.json())

  if endpoint == 'get_server_warnings':
      id = request.args.get('id')
      server = Server.query.filter_by(id=id).first()
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/warnings?recursion=1'
      client_cert = get_client_crt()
      client_key = get_client_key()
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
      return jsonify(results.json())