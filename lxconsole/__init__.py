from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import secrets
import string


app = Flask(__name__)

#Set SECRET_KEY from env if exists
secret_key = os.environ.get('LXCONSOLE_SECRET_KEY')
if not secret_key:
    secret_key = secrets.token_urlsafe(128)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


#Put below app declaration to prevent circular import
from lxconsole import routes

# Create database tables
with app.app_context():
    db.create_all()

#Create cert and key for application. Consider also writing to db, then checking db if exists  then write to file from db
os.system('mkdir -p certs/')
if not os.path.isfile('certs/client.key') and not os.path.isfile('certs/client.crt'):
    import OpenSSL
    import random
    cert_seconds_to_expiry = 60 * 60 * 24 * 365 * 10 # Ten years
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 4096)
    cert = OpenSSL.crypto.X509()
    cert.get_subject().OU = 'LXCONSOLE'
    cert.get_subject().CN = 'Client Certificate'
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(cert_seconds_to_expiry)
    cert.set_serial_number(random.getrandbits(64))
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha512')

    # Write the key and certificate to disk
    with open("certs/client.key", "w") as f:
        f.write( OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key).decode('ascii') )

    with open("certs/client.crt", "w") as f:
        f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert).decode('ascii'))
