from flask import jsonify, request
import json
import requests
import os
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
def api_network_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_network_forward':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/forwards?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'listen_address': request.form.get('listen_address')})
    data.update({'description': request.form.get('description')})
    #config = {}
    #config.update({'user.mykey': request.form.get('user.mykey')}) if request.form.get('user.mykey') else False
    port = {}
    port.update({'description': request.form.get('port_description')}) if request.form.get('port_description') else False
    port.update({'listen_port': request.form.get('port_listen_port')}) if request.form.get('port_listen_port') else False
    port.update({'protocol': request.form.get('port_protocol')}) if request.form.get('port_protocol') else False
    port.update({'target_address': [ request.form.get('port_target_address') ]}) if request.form.get('port_target_address') else False
    port.update({'target_port': [ request.form.get('port_target_port') ]}) if request.form.get('port_target_port') else False

    #data.update({'config': config})
    data.update({'ports': [ port ]})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'add_network_load_balancer':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/load-balancers?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'listen_address': request.form.get('listen_address')})
    data.update({'description': request.form.get('description')})
    backend = {}
    backend.update({'description': request.form.get('backend_description')}) if request.form.get('backend_description') else False
    backend.update({'name': request.form.get('backend_name')}) if request.form.get('backend_name') else False
    backend.update({'target_address': request.form.get('backend_target_address')}) if request.form.get('backend_target_address') else False
    backend.update({'target_port': request.form.get('backend_target_port')}) if request.form.get('backend_target_port') else False
    #config = {}
    #config.update({'user.mykey': request.form.get('user.mykey')}) if request.form.get('user.mykey') else False
    port = {}
    port.update({'description': request.form.get('port_description')}) if request.form.get('port_description') else False
    port.update({'listen_port': request.form.get('port_listen_port')}) if request.form.get('port_listen_port') else False
    port.update({'protocol': request.form.get('port_protocol')}) if request.form.get('port_protocol') else False
    port.update({'target_backend': [ request.form.get('port_target_backend') ]}) if request.form.get('port_target_backend') else False

    data.update({'backends': [ backend ]})
    #data.update({'config': config})
    data.update({'ports': [ port ]})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'add_network_peer':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/peers?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    data.update({'description': request.form.get('description')})
    data.update({'target_network': request.form.get('target_network')})
    data.update({'target_project': request.form.get('target_network')})
    #config = {}
    #config.update({'user.mykey': request.form.get('user.mykey')}) if request.form.get('user.mykey') else False

    #data.update({'config': config})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_network_forward':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/forwards/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'delete_network_load_balancer':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/load-balancers/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'delete_network_peer':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/peers/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'get_network_state':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/state?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/state?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    try:
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key), timeout=5)
      results.raise_for_status()
    except requests.exceptions.RequestException as errex:
      return jsonify({'metadata': []})

    return jsonify(results.json())


  if endpoint == 'list_network_forwards':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/forwards?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/forwards?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    try:
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key), timeout=5)
      results.raise_for_status()
    except requests.exceptions.RequestException as errex:
      return jsonify({'metadata': []})

    forwards = json.dumps(results.json())
    forwards = json.loads(forwards)
    if forwards['metadata']:
      return jsonify(results.json())
    else:
      return jsonify({'metadata': []})
  

  if endpoint == 'list_network_leases':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/leases?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/leases?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    try:
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key), timeout=5)
      results.raise_for_status()
    except requests.exceptions.RequestException as errex:
      return jsonify({'metadata': []})
  
    leases = json.dumps(results.json())
    leases = json.loads(leases)
    if leases['metadata']:
      return jsonify(results.json())
    else:
      return jsonify({'metadata': []})
  

  if endpoint == 'list_network_load_balancers':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/load-balancers?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/load-balancers?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    try:
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key), timeout=5)
      results.raise_for_status()
    except requests.exceptions.RequestException as errex:
      return jsonify({'metadata': []})

    load_balancers = json.dumps(results.json())
    load_balancers = json.loads(load_balancers)
    if load_balancers['metadata']:
      return jsonify(results.json())
    else:
      return jsonify({'metadata': []})
  

  if endpoint == 'list_network_peers':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    name = request.args.get('name')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/peers?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + name + '/peers?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    try:
      results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key), timeout=5)
      results.raise_for_status()
    except requests.exceptions.RequestException as errex:
      return jsonify({'metadata': []})

    peers = json.dumps(results.json())
    peers = json.loads(peers)
    if peers['metadata']:
      return jsonify(results.json())
    else:
      return jsonify({'metadata': []})
  

  if endpoint == 'load_network_forward':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
   
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/forwards/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'load_network_load_balancer':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
   
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/load-balancers/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  
  
  if endpoint == 'load_network_peer':
    id = request.args.get('id')
    project = request.args.get('project')
    network = request.args.get('network')
    name = request.form.get('name')
    server = Server.query.filter_by(id=id).first()
   
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/peers/' + name + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_network_forward':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    network = request.args.get('network')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/forwards/' + name + '?project=' + project
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


  if endpoint == 'update_network_load_balancer':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    network = request.args.get('network')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/load-balancers/' + name + '?project=' + project
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
  

  if endpoint == 'update_network_peer':
    id = request.args.get('id')
    project = request.args.get('project')
    name = request.args.get('name')
    server = Server.query.filter_by(id=id).first()
    network = request.args.get('network')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/networks/' + network + '/peers/' + name + '?project=' + project
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
