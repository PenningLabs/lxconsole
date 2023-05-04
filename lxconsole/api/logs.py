from flask import jsonify, request
import json
import requests
from lxconsole import db, bcrypt
from lxconsole.models import Log
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


def record_log(control, item, message, server_id, user_id, project, status_code ):
  log = Log(control=control, server_id=server_id, project=project, message=message, user_id=user_id, item=item, status_code=status_code)
  db.session.add(log)
  db.session.commit()  


@login_required
def api_logs_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_log':
    id = request.form.get('logname')
    control = request.form.get('control')
    server_id = request.form.get('server_id')
    project = request.form.get('project')
    message = request.form.get('message')
    user_id = request.form.get('user_id')
    item = request.form.get('item')
    status_code = request.form.get('status_code')

    log = Log(control=control, server_id=server_id, project=project, message=message, user_id=user_id, item=item, status_code=status_code)
    db.session.add(log)
    db.session.commit()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'get_log':
    id = request.args.get('id')
    log = Log.query.filter_by(id=id).first()
    data = {}
    data.update({'id': log.id})
    data.update({'control': log.control})
    data.update({'server_id': log.server_id})
    data.update({'project': log.project})
    data.update({'message': log.message})
    data.update({'user_id': log.user_id})
    data.update({'item': log.item})
    data.update({'status_code': log.status_code})
    data.update({'created_at': log.created_at})
    return jsonify({"metadata": data})


  if endpoint == 'delete_log':
    id = request.form.get('id')
    log = Log.query.filter_by(id=id).first()
    db.session.delete(log)
    db.session.commit()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'list_logs':
    logs = Log.query.all()
    return jsonify({"data": [dict(id=log.id, control=log.control, server_id=log.server_id, project=log.project, message=log.message, user_id=log.user_id, item=log.item, status_code=log.status_code, created_at=log.created_at) for log in logs]}) 


  if endpoint == 'update_log':
    pass
