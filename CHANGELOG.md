# 0.6.3
 - Added MFA status on the users page
 - The users page will now only list users for accounts with the list_users_all privilege (Administrator role by default)
 - Added new privilege to Administrator role allowing only this role the ability to add/remove groups to a user
 - The get_mfa_status API endpoint is replaced with get_account_mfa_status or get_user_mfa_status
 - New account.py adds API endpoints for logged in user account

# 0.6.2
 - Updated toast notifications to allow for mulitple notifications
 - Added forceful stop on instances page for state change
 - Added additional notifications for errors with instance action changes

# 0.6.1
 - Converted remaining tables to new format
 - Renamed Proxy to WebSocket Proxy in servers table fields
 - Added additional fields to network zones, including network records per zone
 - Added metadata to operations table
 - Updated remaining datatable layouts
 - Added acknowledging status for warnings
 - Added metadata field to operations table
 - Now displaying key alongside the TOTP QR Code
 - Updated datatables and components to newer versions
 - Fixed additional configuration properties when adding new project
 - Added .gitignore file
 - Added fix for permanent login sessions
 - Added cleanup of records when deleting groups or users

# 0.6.0
 - Added additional packages to python requirements.txt, notably pyotp and qrcode
 - Updated the python requirements.txt version numbers for packages
 - Added an Account page to enable the multi-factor authentication option
 - Added an Expiry Date field to the Certificates table
 - Added a Registries page to support OCI based registries
 - Deprecated the Simplestreams page
 - Added a new Settings page with password requirement settings
 - Added timezone aware created_at default values for user account creation
 - Fixed typo in Network Zones file

# 0.5.7
 - Added check for session state
 - Removed unused library from login and register pages

# 0.5.6
 - Added exporting status to instance backups table
 - Added multirecord select functions to images table
 - Added bootstrap toast notifications for images table actions

# 0.5.5
 - Added status to instance backups
 - Updated datatables on Network Zones page to handle a returned error
 - Added persistence for the number of table rows selected in instances page
 - Updated display rendering of timestamps on instances page

# 0.5.4
 - Added screenshots directory with screenshots
 - Added system warnings page allowing user to acknowledge and delete warnings

# 0.5.3
 - Updated instances list to handle Error status

# 0.5.2
 - Added started_at time to instances info
 
# 0.5.1
 - Added VGA console support for Chrome
 - Changed theme persistence from sessionStorage to localStorage

# 0.5.0
 - Added Dark theme option
 - Added VGA based console option to Virtual Machines via Spice-HTML5

# 0.4.8
 - Added new lxd image repository for LXD based servers to catalog. Catalog automatically populates image catalog from respective images repository based on server type, incus or lxd
 
 # 0.4.7
 - Updated argparser to parse known args for operability with Gunicorn
 - Updated relative links to use url_for allowing for non-root proxy redirects
 - Fixed backup URL download links
 - Added alias when publishing an instance to an image

# 0.4.6
 - Added optional --host and --port command-line args to override flask behavior
 - Added optional FLASK_RUN_PORT and FLASK_RUN_HOST environment variables to override flask behaviour
 - Removed LXD label on servers page
 
# 0.4.5
 - Added source column to instance disk devices table
 - Updated backup exports to use server hostname directory instead of id number
 
# 0.4.4
 - Fixed bug when creating network adapters in clustered environments

# 0.4.3
 - Added code to create bridged, macvlan, ovn, sriov, and pysical adapters with config options 

# 0.4.2
 - Added migrate option to change storage pool of root device
 - Added migrate option to change project of an instance
 - Added storage pool selection when creating new instance
 
# 0.4.1
 - Added selectize.js to allow ordered multiple select option of profiles when creating new instance

# 0.4.0
 - Upgraded Bootstrap from version 4 to version 5
 - Converted containers and virtual-machines endpoints to instances endpoint to support Incus
 - Combined containers and virtual-machines pages to instances page
 - Datatable errors now display on console.log rather than the default alert
 - Handled 404 error for logs on a new virtual machine
 - Fixed several undefined value errors that may occur
 - Updated virtual-machine cpu and memory functions to no longer use sleep

# 0.3.0
 - Improved Dockerfile for quicker builds
 - Added version specific flask and werkzeug to requirements due to build error in dependencies
 - Added a Network Zones page
 - Added a Network page with DHCP Leases, Network Load Balancers, Forwards, and Peers
 - Added missing parameters in API for creating a network
 - Upgraded jQuery to version 3.7.1
 - Updated layout to container and virtual machines pages
 
# 0.2.1
- Updated local xterm.js packages to version 5.1.0 and loading from local file
- Modified CSS to hide terminal scrollbar in chrome based browsers
- Added dynamic resize of terminal when sidebar is toggled

# 0.2.0
- Added cluster groups
- Added evacuate and restore options for cluster members
- Added cluster members roles to tables
- Added cluster members actions
- Removed serializeJSON library in favor of jquery serialize

# 0.1.0
- Corrected image unit size, changing GiB to MiB
- Added option filter for storage volumes by adding filter=custom to URL
- Changed the image catalog for adding images to a dynamic list generated from https://images.linuxcontainers.org

# v0.0.2
- Fix for reloading/loading of page content bug in network-acl page

# v0.0.1
- Fix an undefind varaible error when loading list of containers without root disk
