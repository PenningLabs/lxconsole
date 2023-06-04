from flask import render_template, send_file, url_for, flash, redirect, request, session
from lxconsole import app, db, bcrypt
from lxconsole.forms import RegistrationForm, LoginForm
from lxconsole.models import User, Server, Simplestream, Group, AccessControl, UserGroup
from flask_login import login_user, current_user, logout_user, login_required
from lxconsole.api import api

app.register_blueprint(api)

@app.route("/")
def home():
  if current_user.is_authenticated:
    return redirect(url_for('servers'))
  else:
    if User.query.first():
      return redirect(url_for('login'))
    if not Simplestream.query.first():
      images_simplestream = Simplestream(url='https://images.linuxcontainers.org', alias='images')
      ubuntu_simplestream = Simplestream(url='https://cloud-images.ubuntu.com/releases', alias='ubuntu')
      ubuntu_daily_simplestream = Simplestream(url='https://cloud-images.ubuntu.com/daily', alias='ubuntu-daily')
      db.session.add(images_simplestream)
      db.session.add(ubuntu_simplestream)
      db.session.add(ubuntu_daily_simplestream)
      db.session.commit()
    if not Group.query.first():
      administrators_group = Group(name='Administrators', description='Default administrators group')
      operators_group = Group(name='Operators', description='Default operators')
      users_group = Group(name='Users', description='Default users group')
      auditors_group = Group(name='Auditors', description='Default auditors group')
      db.session.add(administrators_group)
      db.session.add(operators_group)
      db.session.add(users_group)
      db.session.add(auditors_group)
      db.session.commit()
    if not AccessControl.query.first():
      administrators_access_control = AccessControl(group_id=1, role_id=1, server_id=0, scope='global', description='Default access control for Administrators')
      operators_access_control = AccessControl(group_id=2, role_id=2, server_id=0, scope='global', description='Default access control for Operators')
      users_access_control = AccessControl(group_id=3, role_id=3, server_id=0, scope='global', description='Default access control for Users')
      auditors_access_control = AccessControl(group_id=4, role_id=4, server_id=0, scope='global', description='Default access control for Auditors')
      db.session.add(administrators_access_control)
      db.session.add(operators_access_control)
      db.session.add(users_access_control)
      db.session.add(auditors_access_control)
      db.session.commit()
  return redirect(url_for('register'))
    
@app.route("/certificates")
@login_required
def certificates():
  return render_template('certificates.html', page_title='Certificates', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/cluster-groups")
@login_required
def cluster_groups():
  return render_template('cluster-groups.html', page_title='Cluster Groups', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/cluster-members")
@login_required
def cluster_members():
  return render_template('cluster-members.html', page_title='Cluster Members', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/container")
@login_required
def container():
  return render_template('container.html', page_title='Container: ', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/containers")
@login_required
def containers():
  return render_template('containers.html', page_title='Containers', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/images")
@login_required
def images():
  return render_template('images.html', page_title='Images', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/instances")
@login_required
def instances():
  return render_template('instances.html', page_title='Instances', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/network-acl")
@login_required
def network_acl():
  return render_template('network-acl.html', page_title='Network ACL', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/network-acls")
@login_required
def network_acls():
  return render_template('network-acls.html', page_title='Network ACLs', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/networks")
@login_required
def networks():
  return render_template('networks.html', page_title='Networks', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/operations")
@login_required
def operations():
  return render_template('operations.html', page_title='Operations', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/profiles")
@login_required
def profiles():
  return render_template('profiles.html', page_title='Profiles', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/projects")
@login_required
def projects():
  return render_template('projects.html', page_title='Projects', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/server")
@login_required
def server():
  return render_template('server.html', page_title='Server', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/servers")
@login_required
def servers():
  return render_template('servers.html', page_title='Servers', page_user_id=current_user.id, page_username=current_user.username, client_crt=session['client_crt'])

@app.route("/simplestreams")
@login_required
def simplestreams():
  return render_template('simplestreams.html', page_title='Simplestreams', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/storage-pools")
@login_required
def storage_pools():
  return render_template('storage-pools.html', page_title='Storage Pools', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/storage-volumes")
@login_required
def storage_volumes():
  return render_template('storage-volumes.html', page_title='Storage Volumes', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/virtual-machine")
@login_required
def virtual_machine():
  return render_template('virtual-machine.html', page_title='Virtual Machine: ', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/virtual-machines")
@login_required
def virtual_machines():
  return render_template('virtual-machines.html', page_title='Virtual Machines', page_user_id=current_user.id, page_username=current_user.username,)


@app.route("/backups/<serverId>/<project>/<instance>/<filename>")
@login_required
def backups(serverId, project, instance, filename):
  return send_file('../backups/' + serverId + '/' + project + '/' + instance + '/' + filename )


@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('servers'))
  if User.query.first():
    return redirect(url_for('login'))
  else:
    form = RegistrationForm()
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(username=form.username.data, email=form.email.data, password=hashed_password)
      db.session.add(user)
      db.session.commit()
      user_group = UserGroup(user_id=1, group_id=1)
      db.session.add(user_group)
      db.session.commit()
      flash('Your account has been created! You are now able to log in', 'success')
      return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('servers'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')

      with open('certs/client.crt', 'r') as file:
        session['client_crt'] = file.read()

      session['roles'] = [
        {'id': 1, 'name': 'Administrator', 'description': 'Default role with full privileges'},
        {'id': 2, 'name': 'Operator', 'description': 'Default role granting all LXD-based privileges'},
        {'id': 3, 'name': 'User', 'description': 'Default role with limited privileges'},
        {'id': 4, 'name': 'Auditor', 'description': 'Default role with read-only privileges'},
      ]
      session['global_roles'] = []
      session['host_roles'] = []
      groups = UserGroup.query.filter_by(user_id=current_user.id).all()
      print(groups)
      for group in groups:
        print(group)
        print(group.group_id)
        access_controls = AccessControl.query.filter_by(group_id=group.group_id).all()
        print(access_controls)
        for access_control in access_controls:
          print(access_control)
          if access_control.scope == 'global':
            print(access_control.scope)
            for role in session['roles']:
              print(role['id'])
              print(access_control.role_id)
              if role['id'] == access_control.role_id:
                session['global_roles'].append(str(role['name']))
                print(role['name'])
          if access_control.scope == 'host':
            for role in session['roles']:
              if role['id'] == access_control.role_id:
                session['host_roles'][access_control.server_id].append(str(role['name']))

      return redirect(next_page) if next_page else redirect(url_for('servers'))
    else:
      flash('Login Unsuccessful. Please check username and password', 'danger')
  return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
  return render_template('account.html', title='Account')

@app.route("/users")
@login_required
def users():
  return render_template('users.html', page_title='Users', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/groups")
@login_required
def groups():
  return render_template('groups.html', page_title='Groups', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/roles")
@login_required
def roles():
  return render_template('roles.html', page_title='Roles', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/access-controls")
@login_required
def access_controls():
  return render_template('access-controls.html', page_title='Access Controls', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/logs")
@login_required
def logs():
  return render_template('logs.html', page_title='Logs', page_user_id=current_user.id, page_username=current_user.username,)
