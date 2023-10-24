//DELETE THIS FUNCTION AFTER CONVERSION TO NEW THEME
function setSidebarToggleValue(){
  sidebarState = localStorage.getItem('sidebarState');
  if (sidebarState == "collapsed"){
    localStorage.setItem('sidebarState','expanded');
  }
  else {
    localStorage.setItem('sidebarState','collapsed');
  }
}

//DELETE THIS FUNCTION AFTER CONVERSION TO NEW THEME
function applySidebarToggleValue() {
  sidebarState = localStorage.getItem('sidebarState');
  if (sidebarState == "collapsed"){
    $("body").toggleClass("sidebar-collapsed"), 
    $(".sidebar").toggleClass("toggled"), 
    $(".sidebar").hasClass("toggled") && $(".sidebar .collapse").collapse("hide")
  }
}

function configureNavbarForServers(){
  $("#serverNavbarLabel").hide()
  $("#serverNavbarSelect").hide()
  $("#projectNavbarLabel").hide()
  $("#projectNavbarSelect").hide()
  
}

function configureSidebarForServers(){
  $("#clusterMembersLinkSidebar").hide()
  $("#clusterGroupsLinkSidebar").hide()
  $("#instanceSidebarLinks").hide()
  $("#coreSidebarLinks").hide()
  $("#networkSidebarLinks").hide()
  $("#additionalSidebarLinks").hide()
}

function populateSidebarLinks(){
  $("#clusterMembersLinkSidebar").show()
  $("#clusterGroupsLinkSidebar").show()
  $("#instanceSidebarLinks").show()
  $("#coreSidebarLinks").show()
  $("#networkSidebarLinks").show()
  $("#additionalSidebarLinks").show()
}

function populateNavbarLinks(){
  $("#serverNavbarLabel").show()
  $("#serverNavbarSelect").show()
  $("#projectNavbarLabel").show()
  $("#projectNavbarSelect").show()
}

function applySidebarLinks() {
  $("#instancesLinkSidebar").attr("href", "instances?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));

  $("#imagesLinkSidebar").attr("href", "images?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#profilesLinkSidebar").attr("href", "profiles?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#networksLinkSidebar").attr("href", "networks?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#storagePoolsLinkSidebar").attr("href", "storage-pools?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#clusterMembersLinkSidebar").attr("href", "cluster-members?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#clusterGroupsLinkSidebar").attr("href", "cluster-groups?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#projectsLinkSidebar").attr("href", "projects?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#networkAclsLinkSidebar").attr("href", "network-acls?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#networkZonesLinkSidebar").attr("href", "network-zones?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#operationsLinkSidebar").attr("href", "operations?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#certificatesLinkSidebar").attr("href", "certificates?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));
  $("#simplestreamsLinkSidebar").attr("href", "simplestreams?id=" + encodeURI(serverId) + "&project=" + encodeURI(project));  
}

function  applySidebarStyles() {
    if (location.pathname == "/instances" || location.pathname == "/instance"){
      $('#instancesSpan').css('color','#fff');
      $('#instancesIcon').css('color','#fff');
    }
    if (location.pathname == "/images"){
      $('#imagesSpan').css('color','#fff');
      $('#imagesIcon').css('color','#fff');
    }
    if (location.pathname == "/profiles"){
      $('#profilesSpan').css('color','#fff');
      $('#profilesIcon').css('color','#fff');
    }
    if (location.pathname == "/networks"){
      $('#networksSpan').css('color','#fff');
      $('#networksIcon').css('color','#fff');
    }
    if (location.pathname == "/storage-pools" || location.pathname == "/storage-volumes"){
      $('#storagePoolsSpan').css('color','#fff');
      $('#storagePoolsIcon').css('color','#fff');
    }
    if (location.pathname == "/cluster-members"){
      $('#cluterMembersSpan').css('color','#fff');
      $('#clusterMembersIcon').css('color','#fff');
    }
    if (location.pathname == "/projects"){
      $('#projectsSpan').css('color','#fff');
      $('#projectsIcon').css('color','#fff');
    }
    if (location.pathname == "/network-acls" || location.pathname == "/network-acl"){
      $('#networkAclsSpan').css('color','#fff');
      $('#networkAclsIcon').css('color','#fff');
    }
    if (location.pathname == "/network-zones" || location.pathname == "/network-zone"){
      $('#networkZonesSpan').css('color','#fff');
      $('#networkZonesIcon').css('color','#fff');
    }
    if (location.pathname == "/operations"){
      $('#operationsSpan').css('color','#fff');
      $('#operationsIcon').css('color','#fff');
    }
    if (location.pathname == "/certificates"){
      $('#certificatesSpan').css('color','#fff');
      $('#certificatesIcon').css('color','#fff');
    }
    if (location.pathname == "/simplestreams"){
      $('#simplestreamsSpan').css('color','#fff');
      $('#simplestreamsIcon').css('color','#fff');
    }
}
