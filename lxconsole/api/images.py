from flask import jsonify, request, json
import requests
from lxconsole import db
from lxconsole.models import Server,Simplestream
from flask_login import login_required
from lxconsole.api.access_controls import privilege_check


def get_client_crt():
  return 'certs/client.crt'

def get_client_key():
  return 'certs/client.key'

@login_required
def api_images_endpoint(endpoint):

  if not privilege_check(endpoint, request.args.get('id')):
    return jsonify({'data': [], 'metadata':[], 'error': 'not authorized', 'error_code': 403})


  if endpoint == 'add_image':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    image = request.form.get('image')

    # When using the manual form, the version and variant are included in the image string
    if request.form.get('image_version'):
      if request.form.get('image_variant'):
        image = request.form.get('image') + '/' + request.form.get('image_version') + '/' + request.form.get('image_variant')
      else :
        image = request.form.get('image') + '/' + request.form.get('image_version')
        

    data = {}
    source = {}
    source.update({'type': 'image'})
    source.update({'certificate': ''})
    source.update({'protocol': 'simplestreams'})
    if request.form.get('simplestreams_id'):
      simplestreams_id = request.form.get('simplestreams_id')
      simplestream = Simplestream.query.filter_by(id=simplestreams_id).first()
      source.update({'server': simplestream.url})
      source.update({'mode': 'pull'})
      source.update({'allow_inconsistent': 'false'})
    else:
      source.update({'server': request.form.get('repo')})
    source.update({'alias': image })
    source.update({'image_type': request.form.get('image_type')})

    data.update({'source': source})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    
    return jsonify(results.json())


  if endpoint == 'delete_image':
    id = request.args.get('id')
    project = request.args.get('project')
    fingerprint = request.form.get('fingerprint')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images/' + fingerprint + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.delete(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())

  if endpoint == 'list_simplestream_images':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    url = 'https://images.linuxcontainers.org/streams/v1/index.json'
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=True, cert=(client_cert, client_key))
    images = []
    image_results = json.dumps(results.json())
    image_results = json.loads(image_results)
    if 'index' in image_results.keys():
      if 'images' in image_results['index'].keys():
        if 'products' in image_results['index']['images'].keys():
          images = image_results['index']['images']['products']
    return jsonify(images)


  if endpoint == 'list_images':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    recursion = request.args.get('recursion')
    if recursion == '1':
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images?recursion=1&project=' + project
    else:
      url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())
   

  if endpoint == 'load_image':
    id = request.args.get('id')
    project = request.args.get('project')
    fingerprint = request.form.get('fingerprint')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images/' + fingerprint + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.get(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'refresh_image':
    id = request.args.get('id')
    project = request.args.get('project')
    server = Server.query.filter_by(id=id).first()
    fingerprint = request.form.get('fingerprint')
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images/' + fingerprint + '/refresh?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key))
    return jsonify(results.json())


  if endpoint == 'update_image':
    id = request.args.get('id')
    project = request.args.get('project')
    fingerprint = request.args.get('fingerprint')
    server = Server.query.filter_by(id=id).first()
    url = 'https://' + server.addr + ':' + str(server.port) + '/1.0/images/' + fingerprint + '?project=' + project
    client_cert = get_client_crt()
    client_key = get_client_key()

    if request.form.get('json'):
      data = request.form.get('json')
      results = requests.put(url, verify=server.ssl_verify, cert=(client_cert, client_key), data=data)
      return jsonify(results.json())

    data = {}
    data.update({'name': request.form.get('name')})
    results = requests.post(url, verify=server.ssl_verify, cert=(client_cert, client_key), json=data)
    return jsonify(results.json())
