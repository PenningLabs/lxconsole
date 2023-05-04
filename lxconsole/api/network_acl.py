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
def api_network_acl_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_network_acl':
    id = request.args.get('id')
    project = request.args.get('project')
    acl = request.args.get('acl')
    type = request.form.get('type')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-acls/' + acl + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    data = json.dumps(results.json())
    data = json.loads(data)
    
    config = {}
    config.update({'action': request.form.get('action')}) if request.form.get('action') else False
    config.update({'description': request.form.get('description')}) if request.form.get('description') else False
    config.update({'destination': request.form.get('destination')}) if request.form.get('destination') else False
    config.update({'destination_port': request.form.get('destination_port')}) if request.form.get('destination_port') else False
    config.update({'icmp_code': request.form.get('icmp_code')}) if request.form.get('icmp_code') else False
    config.update({'icmp_type': request.form.get('icmp_type')}) if request.form.get('icmp_type') else False
    config.update({'protocol': request.form.get('protocol')}) if request.form.get('protocol') else False
    config.update({'source': request.form.get('source')}) if request.form.get('source') else False
    config.update({'source_port': request.form.get('source_port')}) if request.form.get('source_port') else False
    config.update({'state': request.form.get('state')}) if request.form.get('state') else False

    data['metadata'][type] += [config]
    
    results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data['metadata'])    
    return jsonify(results.json())


  if endpoint == 'delete_network_acl':
    id = request.args.get('id')
    project = request.args.get('project')
    acl = request.args.get('acl')
    index = request.form.get('index')
    type = request.form.get('type')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-acls/' + acl + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    data = json.dumps(results.json())
    data = json.loads(data)
    data['metadata'][type].pop(int(index))
    results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data['metadata'])
    return jsonify(results.json())


  if endpoint == 'list_network_acls':
    id = request.args.get('id')
    project = request.args.get('project')
    acl = request.args.get('acl')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-acls/'+acl+'?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/network-acls/'+acl+'?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    data = json.dumps(results.json())
    data = json.loads(data)
    length = len(data['metadata']['ingress'])
    i = 0
    while i < length:
      data['metadata']['ingress'][i]['index'] = i
      i += 1
    length = len(data['metadata']['egress'])
    i = 0
    while i < length:
      data['metadata']['egress'][i]['index'] = i
      i += 1
    return jsonify(data)
