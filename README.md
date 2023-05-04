# lxconsole
This open source application that provides a web-based user interface capable of managing multiple LXD servers from a single location. Some of the features include:

- Connect and manage multiple LXD servers
- Create LXD container and virtual machine instances from either a form or JSON input
- Start, stop, rename, and delete LXD instances
- Copy instances to create new instances 
- Create, restore and delete snapshots of instances
- Create instances from snaphots
- Migrate instances between hosts on an LXD cluster
- Download LXD container and virtual machine images to LXD hosts
- Create, edit, apply, and remove LXD profiles
- Create, edit, and delete networks, storage pools, storage volumes, and projects
- Switch between projects on an LXD host
- Interact with instances using web-based terminal
- Create and download backups of LXD instance to your local computer
- Create local users and groups
- Apply role based access control

Lxconsole is a python web application that used flask as a framework.

This software is currently in BETA TESTING. Please see roadmap.txt for development plans.

Use the following instructions to setup this software on a linux server:
1. Clone the git repository (git clone https://github.com/PenningLabs/lxconsole.git)
2. Install the python packages found in requirements.txt. (pip3 install -r requirements.txt)
3. Using python, run the run.py file. (python3 run.py)
4. Using your browser, visit http://YOURIPADDRESS:5000


Instructions on setting up lxconsole as a docker image.
1. Build the docker image (sudo docker build --no-cache -t penninglabs/lxconsole:v0.0.0 .)
2. Run the docker container (sudo docker run -p 5000:5000 --name lxconsole -d penninglabs/lxconsole:v0.0.0)
3. Additionally the flask session secret key can be set using the environment variable LXCONSOLE_SECRET_KEY. 
4. Mounted volumes of interest for persistence include the certs (lxconsole client.key and client.crt) and instance (db.sqlite3 database) directories:
  - /opt/lxconsole/certs
  - /opt/lxconsole/instance

