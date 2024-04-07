from flask import jsonify, request
import json
from lxconsole import db
from lxconsole.models import Simplestream
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


#Change this to db written file
clientCrt = 'certs/client.crt'
clientKey = 'certs/client.key'

@login_required
def api_simplestreams_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_simplestream':
    url = request.form.get('url').strip()
    alias = request.form.get('alias').strip()
    
    simplestream = Simplestream(url=url, alias=alias)
    db.session.add(simplestream)
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'delete_simplestream':
    id = request.form.get('id')
    simplestream = Simplestream.query.filter_by(id=id).first()
    db.session.delete(simplestream)
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'list_simplestreams':
    simplestreams = Simplestream.query.all()
    return jsonify({"data": [dict(id=simplestream.id, url=simplestream.url, alias=simplestream.alias) for simplestream in simplestreams]}) 


  # Not yet implemented
  if endpoint == 'update_simplestream':
    id = request.form.get('id')
    simplestream = Simplestream.query.filter_by(id=id).first()
  
    simplestream.url = request.form.get('url').strip()
    simplestream.alias = request.form.get('alias').strip()
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)
