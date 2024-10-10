from datetime import datetime, timezone
from lxconsole import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.last_name}', '{self.first_name}')"

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    def __repr__(self):
        return f"Group('{self.name}', '{self.description}')"

class AccessControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=True)
    scope = db.Column(db.String(255), nullable=False)
    server_id = db.Column(db.Integer, nullable=True)
    group_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"AccessControl('{self.description}', '{self.scope}', '{self.server_id}, '{self.group_id}, '{self.role_id}')"

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"UserGroup('{self.user_id}', '{self.group_id}')"

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    proxy = db.Column(db.String(255), nullable=True)
    ssl_verify = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Server('{self.addr}', '{self.port}', '{self.name}', '{self.proxy}', '{self.ssl_verify}', '{self.user_id}')"

class Simplestream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(255), nullable=True)
    ssl_verify = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f"Simplestream('{self.url}', '{self.alias}', '{self.ssl_verify}')"

class Registry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    protocol = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(255), nullable=True)
    ssl_verify = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f"Registry('{self.url}', '{self.protocol}', '{self.alias}', '{self.ssl_verify}')"

class TOTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    key = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f"TOTP('{self.user_id}', '{self.key}', '{self.enabled}')"

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=True)
    def __repr__(self):
        return f"Setting('{self.name}', '{self.value}')"
    
# class Log(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     control = db.Column(db.String(255), nullable=True)
#     server_id = db.Column(db.Integer, primary_key=True)
#     project = db.Column(db.String(255), nullable=True)
#     message = db.Column(db.String(255), nullable=True)
#     user_id = db.Column(db.Integer, primary_key=True)
#     item = db.Column(db.String(255), nullable=True)
#     status_code = db.Column(db.Integer, primary_key=True)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     def __repr__(self):
#         return f"Simplestream('{self.id}', '{self.description}')"
