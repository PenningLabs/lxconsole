from flask import jsonify, request
import json
import requests
from lxconsole import db, bcrypt
from lxconsole.models import User, UserGroup, Group
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


def retrieve_user_groups(user_id):
  usergroups = UserGroup.query.filter_by(user_id=user_id).all()
  groups = []
  for usergroup in usergroups:
    group = Group.query.filter_by(id=usergroup.group_id).first()
    groups.append(group.name)
  return groups


@login_required
def api_users_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_user':
    username = request.form.get('username')
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password, first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    db.session.flush()
    user_id = user.id

    #Add user to group
    usergroup = UserGroup(user_id=user_id, group_id=request.form.get('group_id'))
    db.session.add(usergroup)
    db.session.commit()

    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'get_user':
    id = request.args.get('id')
    user = User.query.filter_by(id=id).first()
    data = {}
    data.update({'id': user.id})
    data.update({'username': user.username})
    data.update({'email': user.email})
    data.update({'first_name': user.first_name})
    data.update({'last_name': user.last_name})
    data.update({'groups': retrieve_user_groups(id)})

    return jsonify({"metadata": data})


  if endpoint == 'delete_user':
    id = request.form.get('id')
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    json_object = json.loads('{"status": 200}')
    return jsonify(json_object)


  if endpoint == 'list_users':
    users = User.query.all()
    data = []
    for user in users:
      groups = retrieve_user_groups(user.id)
      data.append(dict(id=user.id, username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name, groups=groups))
    return jsonify({"data": data})


  if endpoint == 'list_user_groups':
    id = request.args.get('id')
    groups = retrieve_user_groups(id)
    return jsonify({"data": groups})


  if endpoint == 'update_user':
    id = request.form.get('id')

    #Action for adding or removing a group
    action = request.form.get('action')
    if action:
      if action == 'add':
        group_id = request.form.get('add_group')
        usergroup = UserGroup(user_id=id, group_id=group_id)
        db.session.add(usergroup)
        db.session.commit()
      if action == 'remove':
        group_id = request.form.get('remove_group')
        usergroup = UserGroup.query.filter_by(user_id=id, group_id=group_id).first()
        db.session.delete(usergroup)
        db.session.commit()
      return jsonify({"alert": "Account group updated"})

    user = User.query.filter_by(id=id).first()

    if request.form.get('password') or request.form.get('confirm_password'):
      if request.form.get('password') == request.form.get('confirm_password'):
        user.password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        db.session.commit()
        return jsonify({"alert": "Account password updated"})
      else:
        return jsonify({'alert': 'Could not update user. Passwords did not match'})
 
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.email = request.form.get('email')
    
    db.session.commit()
    return jsonify({"alert": "Account profile updated"})
