from flask import jsonify, request
import json
import re
import pyotp
from lxconsole import db, bcrypt
from lxconsole.models import User, UserGroup, Group, TOTP, Setting
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

    #Check for password requirements
    minimumCharacterLength = Setting.query.filter_by(name='minimumCharacterLength').first()
    if minimumCharacterLength and int(minimumCharacterLength.value or 0) > 0:
      if (len(request.form.get('password')) < int(minimumCharacterLength.value)):
        password_check = False
        alert = "Passwords must be at least " + minimumCharacterLength.value + " characters long"
        return jsonify({"alert": alert})

    enablePasswordComplexity = Setting.query.filter_by(name='enablePasswordComplexity').first()
    if enablePasswordComplexity and enablePasswordComplexity.value == 'true':
      requireUppercaseCharacters = Setting.query.filter_by(name='requireUppercaseCharacters').first()
      requireLowercaseCharacters = Setting.query.filter_by(name='requireLowercaseCharacters').first()
      requireNumbers = Setting.query.filter_by(name='requireNumbers').first()
      requireSpecialCharacters = Setting.query.filter_by(name='requireSpecialCharacters').first()

      if (len(request.form.get('password')) < 8):
        password_check = False
        alert = "Passwords must be at least 8 characters when complexity is enabled"
        return jsonify({"alert": alert})
      if requireLowercaseCharacters and requireLowercaseCharacters.value == 'true' and not re.search("[a-z]", request.form.get('password')):
        password_check = False
        alert = "Password complexity requires lowercase letters"
        return jsonify({"alert": alert})
      if requireUppercaseCharacters and requireUppercaseCharacters.value == 'true' and not re.search("[A-Z]", request.form.get('password')):
        password_check = False
        alert = "Password complexity requires uppercase letters"
        return jsonify({"alert": alert})
      if requireNumbers and requireNumbers.value == 'true' and not re.search("[0-9]", request.form.get('password')):
        password_check = False
        alert = "Password complexity requires numbers"
        return jsonify({"alert": alert})
      if requireSpecialCharacters and requireSpecialCharacters.value == 'true' and not re.search(r'[!@#$%^&*(),.?":{}|<>]', request.form.get('password')):
        password_check = False
        alert = "Password complexity requires special characters"
        return jsonify({"alert": alert})

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

    json_object = json.loads('{"status": 200, "alert": "New user account created"}')
    return jsonify(json_object)

  if endpoint == 'get_mfa_status':
    id = request.args.get('id')
    mfa = TOTP.query.filter_by(user_id=id).first()
    return jsonify({"enabled": mfa.enabled})

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
    data.update({'created_at': user.created_at})
    return jsonify({"metadata": data})


  if endpoint == 'delete_user':
    # May want to query by username too
    id = request.form.get('id')
    user = User.query.filter_by(id=id).first()

    # Delete user+group relationships
    UserGroup.query.filter_by(user_id=id).delete()
    db.session.commit()

    # Delete User TOTP Information
    TOTP.query.filter_by(user_id=id).delete()
    db.session.commit()

    # Delete user
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
    user = User.query.filter_by(id=id).first()

    #Action for adding or removing a group or updating otp or updating password
    action = request.form.get('action')
    if action:
      if action == 'add_group':
        group_id = request.form.get('add_group')
        usergroup = UserGroup(user_id=id, group_id=group_id)
        db.session.add(usergroup)
        db.session.commit()
        return jsonify({"alert": "Account group updated"})
      if action == 'remove_group':
        group_id = request.form.get('remove_group')
        usergroup = UserGroup.query.filter_by(user_id=id, group_id=group_id).first()
        db.session.delete(usergroup)
        db.session.commit()
        return jsonify({"alert": "Account group updated"})
      if action == 'disable_mfa':
        mfa = TOTP.query.filter_by(user_id=id).first()
        mfa.enabled = False
        db.session.commit()
        return jsonify({"alert": "MFA Disabled"})
      if action == 'enable_mfa':
        mfa = TOTP.query.filter_by(user_id=id).first()
        otp = request.form.get('otp')
        totp = pyotp.TOTP(mfa.key)
        if totp.verify(otp):
          mfa.enabled = True
          db.session.commit()
          return jsonify({"alert": "MFA Enabled"})
        else:
          return jsonify({"error_code": 403, "error": "The one-time password is incorrect"})
      if action == 'update_password':
        if request.form.get('password') or request.form.get('confirm_password'):
          if request.form.get('password') == request.form.get('confirm_password'):

            minimumCharacterLength = Setting.query.filter_by(name='minimumCharacterLength').first()
            if minimumCharacterLength and int(minimumCharacterLength.value or 0) > 0:
              if (len(request.form.get('password')) < int(minimumCharacterLength.value)):
                password_check = False
                alert = "Passwords must be at least " + minimumCharacterLength.value + " characters long"
                return jsonify({"alert": alert})

            enablePasswordComplexity = Setting.query.filter_by(name='enablePasswordComplexity').first()
            if enablePasswordComplexity and enablePasswordComplexity.value == 'true':
              requireUppercaseCharacters = Setting.query.filter_by(name='requireUppercaseCharacters').first()
              requireLowercaseCharacters = Setting.query.filter_by(name='requireLowercaseCharacters').first()
              requireNumbers = Setting.query.filter_by(name='requireNumbers').first()
              requireSpecialCharacters = Setting.query.filter_by(name='requireSpecialCharacters').first()

              if (len(request.form.get('password')) < 8):
                password_check = False
                alert = "Passwords must be at least 8 characters when complexity is enabled"
                return jsonify({"alert": alert})
              if requireLowercaseCharacters and requireLowercaseCharacters.value == 'true' and not re.search("[a-z]", request.form.get('password')):
                password_check = False
                alert = "Password complexity requires lowercase letters"
                return jsonify({"alert": alert})
              if requireUppercaseCharacters and requireUppercaseCharacters.value == 'true' and not re.search("[A-Z]", request.form.get('password')):
                password_check = False
                alert = "Password complexity requires uppercase letters"
                return jsonify({"alert": alert})
              if requireNumbers and requireNumbers.value == 'true' and not re.search("[0-9]", request.form.get('password')):
                password_check = False
                alert = "Password complexity requires numbers"
                return jsonify({"alert": alert})
              if requireSpecialCharacters and requireSpecialCharacters.value == 'true' and not re.search(r'[!@#$%^&*(),.?":{}|<>]', request.form.get('password')):
                password_check = False
                alert = "Password complexity requires special characters"
                return jsonify({"alert": alert})

            user.password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            db.session.commit()
            return jsonify({"alert": "Account password updated"})  
          else:
            return jsonify({'error_code': 403, 'error': 'Could not update password. Passwords did not match'})
        else:
          return jsonify({'error_code': 403, 'error': 'Could not update password. Please set both password and confirm password'})
      if action == 'update_user_details':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.email = request.form.get('email')
        
        db.session.commit()
        return jsonify({"alert": "Account profile updated"})
