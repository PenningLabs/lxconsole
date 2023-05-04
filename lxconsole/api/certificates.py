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
def api_certificates_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})

  if endpoint == 'add_certificate':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    project = request.args.get('project')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/certificates?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      data = data.replace('-----BEGIN CERTIFICATE-----\\n', '')
      data = data.replace('-----END CERTIFICATE-----\\n', '')
      data = data.replace('-----END CERTIFICATE-----', '')
      results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    certificate = request.form.get('certificate')
 
    certificate = certificate.replace('-----BEGIN CERTIFICATE-----\n', '')
    certificate = certificate.replace('-----END CERTIFICATE-----\n', '')
    certificate = certificate.replace('-----END CERTIFICATE-----', '')
    data.update({'certificate': certificate})
    data.update({'type': 'client'})

    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())


  if endpoint == 'delete_certificate':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    project = request.args.get('project')
    fingerprint = request.form.get('fingerprint')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/certificates/' + fingerprint + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'list_certificates':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    project = request.args.get('project')
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/certificates?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/certificates?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
  
  
  if endpoint == 'load_certificate':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    project = request.args.get('project')
    fingerprint = request.form.get('fingerprint')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/certificates/' + fingerprint + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_certificate':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    project = request.args.get('project')
    fingerprint = request.args.get('fingerprint')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/certificates/' + fingerprint + '?project=' + project
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

