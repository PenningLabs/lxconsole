from flask import jsonify, request
import json
import requests
from lxconsole import db, bcrypt
from lxconsole.models import Group, UserGroup, AccessControl
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


@login_required
def api_groups_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_group':
    name = request.form.get('name')
    description = request.form.get('description')
    group = Group(name=name, description=description)
    db.session.add(group)
    db.session.commit()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'get_group':
    id = request.args.get('id')
    group = Group.query.filter_by(id=id).first()
    data = {}
    data.update({'id': group.id})
    data.update({'name': group.name})
    data.update({'description': group.description})
    return jsonify({"metadata": data})


  if endpoint == 'delete_group':
    # May want to query by group name too
    id = request.form.get('id')
    group = Group.query.filter_by(id=id).first()

    # Delete user+group relationships
    UserGroup.query.filter_by(group_id=id).delete()
    db.session.commit()

    # Delete access-control linked to group
    AccessControl.query.filter_by(group_id=id).delete()
    db.session.commit()

    # Delete group
    db.session.delete(group)
    db.session.commit()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'list_groups':
    groups = Group.query.all()
    return jsonify({"data": [dict(id=group.id, name=group.name, description=group.description) for group in groups]}) 


  if endpoint == 'update_group':
    id = request.form.get('id')
    group = Group.query.filter_by(id=id).first()
    group.name = request.form.get('name')
    group.description = request.form.get('description')
    db.session.commit()
    return jsonify({"alert": "Group updated"})
