from flask import render_template, send_file, url_for, flash, redirect, request, session
from lxconsole import app, db, bcrypt
from lxconsole.forms import RegistrationForm, LoginForm, OTPForm
from lxconsole.models import User, Server, Simplestream, Registry, Group, AccessControl, UserGroup, TOTP
from flask_login import login_user, current_user, logout_user, login_required
from lxconsole.api import api
import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode

app.register_blueprint(api)

@app.route("/")
def home():
  if current_user.is_authenticated:
    return redirect(url_for('servers'))
  else:
    if User.query.first():
      return redirect(url_for('login'))
    # Populate Simplestreams and Registry table with default values on initial installation setup
    if not Simplestream.query.first():
      images_simplestream = Simplestream(url='https://images.linuxcontainers.org', alias='images')
      ubuntu_simplestream = Simplestream(url='https://cloud-images.ubuntu.com/releases', alias='ubuntu')
      ubuntu_daily_simplestream = Simplestream(url='https://cloud-images.ubuntu.com/daily', alias='ubuntu-daily')
      db.session.add(images_simplestream)
      db.session.add(ubuntu_simplestream)
      db.session.add(ubuntu_daily_simplestream)
      db.session.commit()
    if not Registry.query.first():
      images_registry = Registry(url='https://images.linuxcontainers.org', protocol='simplestreams', alias='images')
      ubuntu_registry = Registry(url='https://cloud-images.ubuntu.com/releases', protocol='simplestreams', alias='ubuntu')
      ubuntu_daily_registry = Registry(url='https://cloud-images.ubuntu.com/daily', protocol='simplestreams', alias='ubuntu-daily')
      docker_registry = Registry(url='https://docker.io', protocol='oci', alias='docker')
      db.session.add(images_registry)
      db.session.add(ubuntu_registry)
      db.session.add(ubuntu_daily_registry)
      db.session.add(docker_registry)
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

@app.route("/images")
@login_required
def images():
  return render_template('images.html', page_title='Images', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/instance")
@login_required
def instance():
  return render_template('instance.html', page_title='Instance', page_user_id=current_user.id, page_username=current_user.username,)

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

@app.route("/network-records")
@login_required
def network_records():
  return render_template('network-records.html', page_title='Network Records', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/network-zones")
@login_required
def network_zones():
  return render_template('network-zones.html', page_title='Network Zones', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/network")
@login_required
def network():
  return render_template('network.html', page_title='Network', page_user_id=current_user.id, page_username=current_user.username,)

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

@app.route("/registries")
@login_required
def registries():
  return render_template('registries.html', page_title='Registries', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/server")
@login_required
def server():
  return render_template('server.html', page_title='Server', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/servers")
@login_required
def servers():
  # Logout and redirect to login if `client_crt` session is not set
  if 'client_crt' not in session:
    logout_user()
    return redirect(url_for('login'))
  
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

@app.route("/warnings")
@login_required
def warnings():
  return render_template('warnings.html', page_title='Warnings', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/backups/<serverId>/<project>/<instance>/<filename>")
@login_required
def backups(serverId, project, instance, filename):
  return send_file('../backups/' + serverId + '/' + project + '/' + instance + '/' + filename )

@app.route("/login_otp", methods=['GET', 'POST'])
def login_otp():
  if current_user.is_authenticated:
    return redirect(url_for('servers'))
  if session['otp_user_id'] and session['otp_passwd_authenticated'] and session['otp_key']:
    form = OTPForm()
    if form.validate_on_submit():
      otp_token = form.token.data
      totp = pyotp.TOTP(session['otp_key'])
      if totp.verify(otp_token):
        user = User.query.filter_by(id=session['otp_user_id']).first()
        login_user(user)
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
        
        groups = UserGroup.query.filter_by(user_id=session['otp_user_id']).all()
        for group in groups:
          access_controls = AccessControl.query.filter_by(group_id=group.group_id).all()
          for access_control in access_controls:
            if access_control.scope == 'global':
              for role in session['roles']:
                if role['id'] == access_control.role_id:
                  session['global_roles'].append(str(role['name']))
            if access_control.scope == 'host':
              for role in session['roles']:
                if role['id'] == access_control.role_id:
                  session['host_roles'][access_control.server_id].append(str(role['name']))

        session.pop('otp_user_id', default=None)
        session.pop('otp_passwd_authenticated', default=None)
        session.pop('otp_key', default=None)

        return redirect(next_page) if next_page else redirect(url_for('servers'))

      else:
        flash('Your time-based one time password was incorrect. Try again', 'danger')
    return render_template('login_otp.html', title='OTP', form=form)
  else:
    return redirect(url_for('login'))
  
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
  login_form = LoginForm()
  if login_form.validate_on_submit():
    user = User.query.filter_by(username=login_form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, login_form.password.data):
      # Check to see if otp is enabled for the user. If it is return redirect of login_otp page
      otp = TOTP.query.filter_by(user_id=user.id).first()
      if otp and otp.enabled:
        session.permanent = login_form.remember.data
        session['otp_user_id'] = user.id
        session['otp_passwd_authenticated'] = True
        session['otp_key'] = otp.key
        session['otp_next_page'] = request.args.get('next')
        return redirect(url_for('login_otp'))
      else:
        session.permanent = login_form.remember.data
        login_user(user, remember=login_form.remember.data)
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
      for group in groups:
        access_controls = AccessControl.query.filter_by(group_id=group.group_id).all()
        for access_control in access_controls:
          if access_control.scope == 'global':
            for role in session['roles']:
              if role['id'] == access_control.role_id:
                session['global_roles'].append(str(role['name']))
          if access_control.scope == 'host':
            for role in session['roles']:
              if role['id'] == access_control.role_id:
                session['host_roles'][access_control.server_id].append(str(role['name']))

      return redirect(next_page) if next_page else redirect(url_for('servers'))
    else:
      flash('Login Unsuccessful. Please check username and password', 'danger')
  return render_template('login.html', title='Login', form=login_form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
  otp = TOTP.query.filter_by(user_id=current_user.id).first()
  if otp:
    if otp.key:
      otp_key = otp.key
    else:
      otp_key = pyotp.random_base32()
      otp.key = otp_key
      db.session.commit()
  else:
    otp_key = pyotp.random_base32()
    otp_record = TOTP(user_id=current_user.id, key=otp_key)
    db.session.add(otp_record)
    db.session.commit()

  # Create the totp URI used to generate QRCode and set username and issuer
  totp_uri = pyotp.totp.TOTP(otp_key).provisioning_uri(name=current_user.username, issuer_name='LXConsole')

  # Generate QRCode
  qr = qrcode.QRCode(version=1, box_size=10, border=2)
  qr.add_data(totp_uri)
  qr.make(fit=True)
  img = qr.make_image(fill_color='black', back_color='white')
  buffered = BytesIO()
  img.save(buffered)
  qr_img_bytes = b64encode(buffered.getvalue()).decode("utf-8")
  
  return render_template('account.html', page_title='Account', qr_img=qr_img_bytes, totp_key=otp_key, page_user_id=current_user.id, page_username=current_user.username,)

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

@app.route("/settings")
@login_required
def settings():
  return render_template('settings.html', page_title='Settings', page_user_id=current_user.id, page_username=current_user.username,)

@app.route("/logs")
@login_required
def logs():
  return render_template('logs.html', page_title='Logs', page_user_id=current_user.id, page_username=current_user.username,)

@app.route('/api')
@login_required
def api():
  return redirect(url_for('api.index'))
