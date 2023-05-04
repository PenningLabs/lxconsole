from flask import jsonify, request, session
import json
import requests
from lxconsole import db, bcrypt
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


@login_required
def api_roles_endpoint(endpoint):

  if not privilege_check(endpoint):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})

  if endpoint == 'add_role':
    pass

  if endpoint == 'get_role':
    pass

  if endpoint == 'delete_role':
    pass

  if endpoint == 'list_roles':
    return jsonify({"data": session['roles']})

  if endpoint == 'update_role':
    pass
