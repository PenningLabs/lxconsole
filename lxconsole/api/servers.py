from flask import jsonify, request
import json
import requests
from lxconsole import db
from lxconsole.models import Server
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


#Change this to db written file
clientCrt = 'certs/client.crt'
clientKey = 'certs/client.key'

@login_required
def api_servers_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_server':
    addr = request.form.get('addr')
    port = request.form.get('port')
    proxy = request.form.get('proxy')
    ssl_verify = request.form.get('ssl_verify')
    user_id = request.form.get('user_id')

    if ssl_verify == 'false':
      sslVerify = False
    else:
      sslVerify = True

    if not user_id:
      user_id = 0

    #Should verify that we can connect to url before inserting into database
    url = 'https://' + addr + ':' + port + '/1.0'

    server_name = ''
    try:
      results = requests.get(url, verify=sslVerify, cert=(clientCrt, clientKey))
      results = results.json()
      if 'environment' in results['metadata'].keys():
        if 'server_name' in results['metadata']['environment'].keys():
          server_name = results['metadata']['environment']['server_name']
      if not server_name:
        return jsonify({"status":"", "error": 'Unable to retrieve server information. The lxconsole certificate may not be trusted by this server.'})
    except requests.exceptions.RequestException as err:
      return jsonify({"status":"", "error": str(err)})
        
    server = Server(addr=addr, port=port, name=server_name, proxy=proxy, ssl_verify=sslVerify, user_id=user_id)
    db.session.add(server)
    db.session.commit()

    json_object = json.loads('{"status": 200, "error": ""}')
    return jsonify(json_object)


  if endpoint == 'get_server':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    return jsonify({"data": [dict(id=server.id, port=server.port, addr=server.addr, name=server.name, proxy=server.proxy, ssl_verify=server.ssl_verify, user_id=server.user_id)]}) 


  if endpoint == 'remove_server':
    id = request.args.get('id')
    server = Server.query.filter_by(id=id).first()
    db.session.delete(server)
    db.session.commit()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'list_servers':
    servers = Server.query.all()
    return jsonify({"data": [dict(id=server.id, addr=server.addr, port=server.port, name=server.name, proxy=server.proxy, ssl_verify=server.ssl_verify, user_id=server.user_id) for server in servers]}) 


  if endpoint == 'update_server':
    id = request.form.get('id')
    server = Server.query.filter_by(id=id).first()
    ssl_verify = request.form.get('ssl_verify')

    if ssl_verify == 'false':
      sslVerify = False
    else:
      sslVerify = True
  
    server.addr = request.form.get('addr')
    server.port = request.form.get('port')
    server.proxy = request.form.get('proxy')
    server.ssl_verify = sslVerify
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)
