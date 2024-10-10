from flask import jsonify, request
import json
from lxconsole import db
from lxconsole.models import Setting
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


@login_required
def api_settings_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_setting':
    name = request.form.get('name')
    value = request.form.get('value')
    setting = Setting(name=name, value=value)
    db.session.add(setting)
    db.session.commit()
    db.session.flush()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'get_setting':
    name = request.args.get('name')
    setting = Setting.query.filter_by(name=name).first()
    data = {}
    data.update({'id': setting.id})
    data.update({'name': setting.name})
    data.update({'value': setting.value})
    return jsonify({"metadata": data})


  if endpoint == 'delete_setting':
    name = request.form.get('name')
    setting = Setting.query.filter_by(name=name).first()
    db.session.delete(setting)
    db.session.commit()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'list_settings':
    settings = Setting.query.all()
    data = []
    for setting in settings:
      data.append(dict(id=setting.id, name=setting.name, value=setting.value))
    return jsonify({"data": data})


  if endpoint == 'update_setting':
    name = request.form.get('name')
    value = request.form.get('value')
    if Setting.query.filter_by(name=name).first():
      setting = Setting.query.filter_by(name=name).first()
      setting.value = value
      db.session.commit()
    else:
      setting = Setting(name=name, value=value)
      db.session.add(setting)
      db.session.commit()
      db.session.flush()

    return jsonify({"alert": "Setting updated"})
