from flask import jsonify, request
import json
from lxconsole import db
from lxconsole.models import Registry
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


#Change this to db written file
clientCrt = 'certs/client.crt'
clientKey = 'certs/client.key'

@login_required
def api_registries_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_registry':
    url = request.form.get('url').strip()
    protocol = request.form.get('protocol')
    alias = request.form.get('alias').strip()
    
    registry = Registry(url=url, protocol=protocol, alias=alias)
    db.session.add(registry)
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'delete_registry':
    id = request.form.get('id')
    registry = Registry.query.filter_by(id=id).first()
    db.session.delete(registry)
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)

  if endpoint == 'get_registry':
    id = request.args.get('id')
    registry = Registry.query.filter_by(id=id).first()
    return jsonify({"data": [dict(id=registry.id, url=registry.url, protocol=registry.protocol, alias=registry.alias)]}) 
  
  if endpoint == 'list_registries':
    registries = Registry.query.all()
    return jsonify({"data": [dict(id=registry.id, url=registry.url, protocol=registry.protocol, alias=registry.alias) for registry in registries]}) 


  if endpoint == 'update_registry':
    id = request.form.get('id')
    registry = Registry.query.filter_by(id=id).first()
  
    registry.url = request.form.get('url').strip()
    registry.protocol = request.form.get('protocol')
    registry.alias = request.form.get('alias').strip()
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)
