# 0.4.7
 - Updated argparser to parse known args for operabilty with gunicorn
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