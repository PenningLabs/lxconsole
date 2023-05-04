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
def api_cluster_members_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})

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


  if endpoint == 'list_cluster_members':
    if api_cluster_members_endpoint('is_cluster_member_enabled') == 'True':
      id = request.args.get('id')
      project = request.args.get('project')
      server = Server.query.filter_by(id=id).first()
      recursion = request.args.get('recursion')
      if recursion == '1':
        url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/members?recursion=1&project=' + project
      else:
        url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/cluster/members?project=' + project
      client_cert = get_client_crt()
      client_key = get_client_key()
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
      return jsonify(results.json())
    data = { "metadata": []}
    return jsonify(data)

