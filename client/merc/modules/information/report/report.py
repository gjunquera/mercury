import os
import shutil
from merc.lib.modules import Module
from merc.lib import Message_pb2

class Report(Module):
    """Description: Use Mercury Commands to create a HTML Report
usage: [destFolder="folder"] [filter="package name"
Credit: Glauco Junquera - Samsung SIDI"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information", "report"]
        self.uris_list = []

    def execute(self, session, _arg):

        self.session = session
                        
        package_filter = _arg.get('filter')
        dest_folder = _arg.get('destFolder')
        query_value = _arg.get('queryProviders')
        self.query = True
        if (query_value is not None) and (query_value.lower() == "false"):
            self.query = False
            
        if dest_folder is None:
            dest_folder = ""
        else:
            dest_folder.replace("\\", "/")
            if not dest_folder.endswith("/"):
                dest_folder += "/"
                
        #return if the destination folder does not exist                
        if (len(dest_folder) > 0) and (not os.path.exists(dest_folder)):
            raise Exception("Destination folder does not exists")
        
        self.cleanFolder(dest_folder + "report")
        
        content = PackageContent()
        
        #Request packages info
        request = {'filter': package_filter, 'output': None, 'permissions': None}
        response = self.session.executeCommand("packages", "info", request)
        content.packages.ParseFromString(str(response.data))
        
        #Request service info
        request = {'filter': package_filter, 'output': None, 'permissions': None}        
        response = self.session.executeCommand("service", "info", request)
        content.service.ParseFromString(str(response.data))
            
        #Request activity info
        request = {'filter': package_filter, 'output': None}                    
        response = self.session.executeCommand("activity", "info", request)
        content.activity.ParseFromString(str(response.data))
            
        #Request provider info
        request = {'filter': package_filter, 'output': None, 'permissions': None}                    
        response = self.session.executeCommand("provider", "info", request)
        content.provider.ParseFromString(str(response.data))
        
        #Request Broadcast Receiver info
        request = {'filter': package_filter, 'output': None, 'permissions': None}
        response = self.session.executeCommand("broadcast", "info", request)
        content.broadcast.ParseFromString(str(response.data))
        
        #Request Native Info
        request = {'filter': package_filter, 'output': None}
        response = self.session.executeCommand("native", "info", request)
        content.native.ParseFromString(str(response.data))
        
        #Request Debuggable Info
        request = {'filter': package_filter, 'output': None}
        response = self.session.executeCommand("debuggable", "info", request)
        content.debug.ParseFromString(str(response.data))

        #Request Attack Surface Info
        request = {}        
        response = self.session.executeCommand("packages", "attacksurface", request)
        content.attacksurface.ParseFromString(str(response.data))
        
        general_links = []
        general_links.append(MenuLink("Package Info", "#packageInfo"))
        general_links.append(MenuLink("Attack Surface", "#attackSurface"))
        general_links.append(MenuLink("Content Provider Uris", "#urisList"))
        if self.query:
            general_links.append(MenuLink("Content Provider Uris Queries", "#uriQueries"))
        general_links.append(MenuLink("Secret Codes", "#secretCodes"))            
        
        components_links = []
        components_links.append(MenuLink("Activities", "#activities"))
        components_links.append(MenuLink("Broadcast Receivers", "#receivers"))
        components_links.append(MenuLink("Content Providers", "#providers"))
        components_links.append(MenuLink("Services", "#services"))
        components_links.append(MenuLink("Native Libraries", "#native"))
        
        menu_sections = []
        menu_sections.append(MenuSection("General Info", general_links))
        menu_sections.append(MenuSection("Package Components", components_links))

        package_names = []
        #crate an html for each package
        for info in content.packages.info:
            if package_filter == None or package_filter == str(info.packageName):
                package_names.append(str(info.packageName))
                html = self.makePackageHtml(str(info.packageName), menu_sections, content, str(info.packageName))
                self.createHtmlFile(html, dest_folder, str(info.packageName))
                
        if package_filter is None:    
            #create index page menu links
            general_links = []
            general_links.append(MenuLink("Device Info", "#deviceInfo"))
            general_links.append(MenuLink("Build Properties", "#buildProp"))
            general_links.append(MenuLink("System Properties", "#systemProp"))
            general_links.append(MenuLink("Unprotected Content Providers", "#unprotected"))
            general_links.append(MenuLink("Unprotected Broadcast Receivers", "#unprotectedBroadcast"))
            general_links.append(MenuLink("Unprotected Services", "#unprotectedService"))
            general_links.append(MenuLink("Content Providers Uris", "#urisList"))
            general_links.append(MenuLink("Content Provider Uris Queries", "#uriQueries"))            
            general_links.append(MenuLink("Secret Codes", "#secretCodes"))
            general_links.append(MenuLink("Debuggable Packages", "#debug"))
            
            package_links = []
            for package in package_names:
                package_links.append(MenuLink(package, package + ".html"))
                
            index_sections = []
            index_sections.append(MenuSection("General Info", general_links))
            index_sections.append(MenuSection("Packages", package_links))
            
            html = self.makeIndexHtml("Mercury Report", index_sections, content)
            self.createHtmlFile(html, dest_folder, "report_index")

        self.copyCssToDestination(dest_folder)
        
    def makeIndexHtml(self, title, menu_sections, content):
        html = "<html>\n"
        html += "<link rel=\"stylesheet\" href=\"report.css\">\n"
        html += "<body>\n"
        html += self.makeMenu(menu_sections) + "\n"
        html += self.makeIndexContent(content, title) + "\n"
        html += "</body>\n"
        html += "</html>"                
        return html

    def makePackageHtml(self, title, menu_sections, content, package):
        html = "<html>\n"
        html += "<link rel=\"stylesheet\" href=\"report.css\">\n"
        html += "<body>\n"
        html += self.makeMenu(menu_sections) + "\n"
        html += self.makePackageContent(content, package, title) + "\n"
        html += "</body>\n"
        html += "</html>"
        return html
        
    def makeHeader(self, title):
        html = "<div id=\"header-wrapper\">\n"
        html += "<div id=\"header-text\">\n"
        html += "<p align=\"center\">" + title + "</p>\n"
        html += "</div>\n"
        html += "</div>"
        return html
    
    def makeMenu(self, menu_sections):
        html = "<div id=\"menu_wrapper\">\n"
        html += "<div id=\"menu\">\n"
        for section in menu_sections:
            html += "<ul>\n"
            html += "<li>" + section.title + "</li>\n"
            for link in section.links:
                html += "<li><a href=\"" + link.id + "\">" + link.title + "</a></li>\n"
        html += "</div>\n"
        html += "</div>"
        return html
    
    def makeTable(self, lines):
        html = "<table>\n"
        for line in lines:
            html += self.makeTableLine(line) + "\n"
        html += "</table>"
        return html
    
    def makeTableLine(self, line):
        html = "<tr>\n"
        for column in line:
            html += "<td>" + column + "</td>\n"
        html += "</tr>"
        return html
    
    def makePackageContent(self, content, package, title):
        uris = self.getPackageUris(package, content.provider)
        html = "<div id=\"content\">\n"
        html += "<p id=\"title\">" + title + "</p>\n"
        html += self.makePackageInfoHtml(content.packages, package) + "\n"
        html += self.makeAttackSurfaceHtml(content.attacksurface, package) + "\n"
        html += self.makeUrisList(uris) + "\n"
        html += self.makeSecretCodesHtml(content.packages, package) + "\n"
        if self.query:
            html += self.makeQueryUris(uris) + "\n"
        html += self.makeActivityHtml(content.activity, package) + "\n"
        html += self.makeBroadcastHtml(content.broadcast, package) + "\n"
        html += self.makeProviderHtml(content.provider, package) + "\n"
        html += self.makeServiceHtml(content.service, package) + "\n"
        html += self.makeNativeHtml(content.native, package) + "\n"
        html += "</div>"
        return html
    
    def makeIndexContent(self, content, title):
        build_prop = self.getBuildProperties()
        system_prop = self.getProperties()
        kernel = self.getKernelVersion()
        html = "<div id=\"content\">\n"
        html += "<p id=\"title\">" + title + "</p>\n"
        html += self.makeDeviceInfoHtml(kernel, build_prop) + "\n"
        html += self.makeBuildPropHtml(build_prop) + "\n"
        html += self.makeSystemPropHtml(system_prop) + "\n"
        html += self.makeUnprotectedProviderHtml(content.provider) + "\n"
        html += self.makeUnprotectedBroadcastHtml(content.broadcast) + "\n"
        html += self.makeUnprotectedServiceHtml(content.service) + "\n"
        html += self.makeUrisList(self.uris_list) + "\n"
        if self.query:
            html += self.makeQueryUris(self.uris_list) + "\n"
        html += self.makeSecretCodesHtml(content.packages, None) + "\n"
        html += self.makeDebugHtml(content.debug) + "\n"
        html += "</div>"        
        return html
    
    def makeServiceHtml(self, content, package=None):
        html = "<p id=\"services\" class=\"section_title\">Services</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
#                lines.append(["Package Name", str(info.packageName)])
                lines.append(["Service", str(info.service)])
                if str(info.permission) == "null":
                    lines.append(["Required Permission", "UNPROTECTED SERVICE"])
                else:                    
                    lines.append(["Required Permission", str(info.permission)])
                action_str = ""
                for action in info.action:
                    action_str += str(action) + "<br>\n"
                lines.append(["Intent Filter Action", action_str])                    
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeAttackSurfaceHtml(self, content, package=None):
        html = "<p id=\"attackSurface\" class=\"section_title\">Attack Surface</p>\n"
        for info in content.attackSurface:
            if (package != None) and (package == str(info.packageName)):
                lines = []
                lines.append(["Exported Activities", str(info.activities)])
                lines.append(["Exported Receivers", str(info.receivers)])
                lines.append(["Exported Content Providers", str(info.providers)])
                lines.append(["Exported Content Services", str(info.services)])                
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeActivityHtml(self, content, package=None):
        html = "<p id=\"activities\" class=\"section_title\">Activities</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
                lines.append([str(info.activity)])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeProviderHtml(self, content, package=None):
        html = "<p id=\"providers\" class=\"section_title\">Content Providers</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
                lines.append(["Authority", str(info.authority)])
                lines.append(["Read Permission", str(info.readPermission)])
                lines.append(["Write Permission", str(info.writePermission)])
                lines.append(["Grant Uri Permissions", str(info.grantUriPermissions)])
                lines.append(["Multiprocess allowed", str(info.multiprocess)])
                for uri in info.uriPermissionPatterns: 
                    lines.append(["URI Permission Pattern", str(uri)])           
                for pathPermission in  info.pathPermissions:
                    if len(pathPermission.readPermission) > 0:
                        lines.append(["Read Path Permission", str(pathPermission.readPermission) + " needs " + str(pathPermission.readNeeds)])
                    if len(pathPermission.writePermission) > 0:
                        lines.append(["Write Path Permission", str(pathPermission.writePermission) + " needs " + str(pathPermission.writeNeeds)])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeUnprotectedProviderHtml(self, content):
        self.getUnprotectedProviders(content)
        html = "<p id=\"unprotected\" class=\"section_title\">Unprotected Providers</p>\n"
        for info in self.rw_unprotected:
            lines = []
            lines.append(["PackageName",  str(info.packageName)])
            lines.append(["Authority", str(info.authority)])
            lines.append(["No Read and Write Permissions"])
            html += self.makeTable(lines) + "\n"
            
        for info in self.w_unprotected:
            lines = []
            lines.append(["PackageName",  str(info.packageName)])
            lines.append(["Authority", str(info.authority)])
            lines.append(["No Write Permission"])
            html += self.makeTable(lines) + "\n"
            
        for info in self.r_unprotected:
            lines = []
            lines.append(["PackageName",  str(info.packageName)])
            lines.append(["Authority", str(info.authority)])
            lines.append(["No Read Permission"])
            html += self.makeTable(lines) + "\n"                        

        return html
    
    def makeUnprotectedBroadcastHtml(self, content):
        html = "<p id=\"unprotectedBroadcast\" class=\"section_title\">Unprotected Broadcast Receivers</p>\n"
        previousPackage = ""
        first = True
        lines = []
        for info in content.info:
            currentPackage = str(info.packageName)
            if str(info.permission) == "null":
                if previousPackage != currentPackage:
                    if not first:
                        html += self.makeTable(lines) + "\n"
                    lines = []                        
                    receivers_str = str(info.receiver)
                    lines.append(["Package Name", str(info.packageName)])
                    lines.append(["Unprotected Receivers", receivers_str])
                    previousPackage = currentPackage
                    first = False
                else:
                    receivers_str += "<br>\n" + str(info.receiver)
                    lines[1] = ["Unprotected Receivers", receivers_str]
        html += self.makeTable(lines) + "\n"
        return html
    
    def makeUnprotectedServiceHtml(self, content):
        html = "<p id=\"unprotectedService\" class=\"section_title\">Unprotected Services</p>\n"
        previousPackage = ""
        first = True
        lines = []
        for info in content.info:
            currentPackage = str(info.packageName)
            if str(info.permission) == "null":
                if previousPackage != currentPackage:
                    if not first:
                        html += self.makeTable(lines) + "\n"
                    lines = []                        
                    services_str = str(info.service)
                    lines.append(["Package Name", str(info.packageName)])
                    lines.append(["Unprotected Services", services_str])
                    previousPackage = currentPackage
                    first = False
                else:
                    services_str += "<br>\n" + str(info.service)
                    lines[1] = ["Unprotected Services", services_str]
        html += self.makeTable(lines) + "\n"
        return html    
    
    def makeBroadcastHtml(self, content, package=None):
        html = "<p id=\"receivers\" class=\"section_title\">Broadcast Receivers</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
#                lines.append(["Package name", str(info.packageName)])
                lines.append(["Receiver", str(info.receiver)])
                lines.append(["Required Permission", str(info.permission)])
                action_str = ""
                for action in info.action:
                    action_str += str(action) + "<br>\n"
                lines.append(["Intent Filter Action", action_str])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeNativeHtml(self, content, package=None):
        html = "<p id=\"native\" class=\"section_title\">Native Libraries</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
#                lines.append(["Package name", str(info.packageName)])
                for native in info.nativeLib:
                    lines.append([str(native)])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeDebugHtml(self, content, package=None):
        html = "<p id=\"debug\" class=\"section_title\">Debuggable Packages</p>\n"
        for info in content.info:
            lines = []
            lines.append(["Package name", str(info.packageName)])
            lines.append(["UID", str(int(info.uid))])
            permission_str = ""
            for permission in info.permission:
                permission_str += str(permission) + "<br>\n"
            lines.append(["Permissions", permission_str])
            html += self.makeTable(lines) + "\n"            
        return html
    
    def makeDeviceInfoHtml(self, kernel_version, build_prop):
        html = "<p id=\"deviceInfo\" class=\"section_title\">Device Info</p>\n"
        lines = []
        lines.append(['Device Brand', self.getFromDictionary(build_prop, 'ro.product.brand')])
        lines.append(['Device Model', self.getFromDictionary(build_prop, 'ro.product.model')])
        lines.append(['Android Version', self.getFromDictionary(build_prop, 'ro.build.version.release')])
        lines.append(['Build ID', self.getFromDictionary(build_prop, 'ro.build.display.id')])
        lines.append(['Kernel Version', kernel_version])
        html += self.makeTable(lines) + "\n"
        return html
    
    def makeBuildPropHtml(self, properties):
        return "<p id=\"buildProp\" class=\"section_title\">Build Properties</p>\n" + self.makeTableFromDict(properties) 
        
    def makeSystemPropHtml(self, properties):
        return "<p id=\"systemProp\" class=\"section_title\">System Properties</p>\n" + self.makeTableFromDict(properties)
    
    def makeTableFromDict(self, dictionary):
        lines = []
        for k in dictionary.keys():
            lines.append([k, dictionary[k]])
        return self.makeTable(lines)
        
    def makeUrisList(self, uris):
        html = "<p id=\"urisList\" class=\"section_title\">Content Provider Uris Found</p>\n"
        lines = []
        for uri in uris:
            lines.append([uri])
        html += self.makeTable(lines) + "\n"            
        return html
    
    def makeQueryUris(self, uris):
        html = "<p id=\"uriQueries\" class=\"section_title\">Content Provider Uris Queries</p>\n"
        for uri in uris:
            request = {'selectionArgs': None, 'selection': None, 'projection': None, 'showColumns': None, 'Uri': uri, 'sortOrder': None, 'output': None}
            response = self.session.executeCommand("provider", "query", request)
            lines = []
            lines.append(["Uri Queried", uri])
            html += self.makeTable(lines) + "\n"
            lines = []
            if str(response.error) == "OK":
                for pair in response.structured_data:
                    line = []
                    for value in pair.value:
                        line.append(str(value))
                    lines.append(line)
                html += self.makeTable(lines) + "\n"   
            else:
                if (response.HasField("error")):
                    lines.append([str(response.error)])
                else:
                    lines.append(["Unknown Error"])
                html += self.makeTable(lines) + "\n" 
        return html
    
    def makeSecretCodesHtml(self, content, package):
        html = "<p id=\"secretCodes\" class=\"section_title\">Secret Codes</p>\n"
        lines = []
        for info in content.info:
            if (package == None) or (package == str(info.packageName)):
                for secretCode in info.secretCode:
                    lines.append([str(secretCode)])
        html += self.makeTable(lines) + "\n"
        return html                        
            
    def makePackageInfoHtml(self, content, package=None):
        html = "<p id=\"packageInfo\" class=\"section_title\">Package Info</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
                lines.append(["Package name", str(info.packageName)])
                lines.append(["Process name", str(info.processName)])
                lines.append(["Version", str(info.version)])
                lines.append(["Data directory", str(info.dataDirectory)])
                lines.append(["APK path", str(info.apkPath)])
                lines.append(["UID", str(info.uid)])
                guid_str = ""
                for guid in info.guid:
                    guid_str += str(guid) + "; "
                if len(guid_str) > 0:
                    lines.append(["GUIDs", guid_str])
                for sharedLib in  info.sharedLibraries:
                    lines.append(["Shared libraries", str(sharedLib)])
                if info.sharedUserId is not None:
                    lines.append(["SharedUserId: ", str(info.sharedUserId) + " (" + str(info.uid) + ")"])
                permission_str = ""
                for permission in  info.permission:
                    permission_str += str(permission) + "<br>\n"
                lines.append(["Permissions", permission_str])
                html += self.makeTable(lines) + "\n"
        return html
    
    def createHtmlFile(self, html="", path="", filename="generated_html"):
        if not os.path.exists(path + "report"):
            os.makedirs(path + "report")
        f = open(path + "report/" + filename + ".html", 'w')
        f.write(html)
        f.close()
        
    def copyCssToDestination(self, dest_path=""):
        current_path = os.getcwd().replace("\\", "/")
        shutil.copyfile(current_path + "/merc/modules/information/report/report.css", dest_path + "report/report.css")
        
    def cleanFolder(self, path):
        #remove all files from report folder
        if os.path.exists(path):
            for the_file in os.listdir(path):
                file_path = os.path.join(path, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception, e:
                    print e

    def getUnprotectedProviders(self, provider_info):
        self.rw_unprotected = []
        self.r_unprotected = []
        self.w_unprotected = []
        for info in provider_info.info:
            if (not info.HasField("writePermission")) and (not info.HasField("readPermission")):
                    self.rw_unprotected.append(info)
            elif (not info.HasField("readPermission")):
                self.r_unprotected.append(info)
            elif (not info.HasField("writePermission")):
                self.w_unprotected.append(info)                    
    
    def queryUri(self, uri):
        response = self.session.executeCommand("provider", "query", {"Uri":uri})
        return response
    
    #TODO call merc.lib,provider directly
    def getPackageUris(self, package, providers_info):
        
        uris = []
        
        for info in providers_info.info:
            if package == str(info.packageName):
                uris.append("content://" + str(info.authority))
                    
        # Delete classes.dex that might be there from previously
        path = self.session.executeCommand("packages", "path", {'packageName':package})            
        self.session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})
        
        # Iterate through paths returned
        for pair in path.structured_data:
            for value in pair.value:
                line = str(value)
                
                if (".apk" in line):
                    if str(self.session.executeCommand("core", "unzip", {'filename':'classes.dex', 'path':line, 'destination':'/data/data/com.mwr.mercury/'}).error) == "OK":
                        response = self.session.executeCommand("provider", "finduri", {'path':'/data/data/com.mwr.mercury/classes.dex'})
                        
                        if str(response.error) == "OK":
                            for pair in response.structured_data:
                                if pair.key == "uri":
                                    for value in pair.value:
                                        value_str = str(value)
                                        if (("CONTENT://" in value_str.upper()) and ("CONTENT://" != value_str.upper())):
                                            uri = value_str[value_str.upper().find("CONTENT"):]
                                            if uri not in uris:
                                                uris.append(uri)
                        # Delete classes.dex
                        self.session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})
    
                if (".odex" in line):
                    response_odex = self.session.executeCommand("provider", "finduri", {'path':line})
                    if str(response_odex.error) == "OK":
                            for pair in response_odex.structured_data:
                                if pair.key == "uri":
                                    for value in pair.value:
                                        value_str = str(value)
                                        if (("CONTENT://" in value_str.upper()) and ("CONTENT://" != value_str.upper())):
                                            uri = value_str[value_str.upper().find("CONTENT"):]
                                            if uri not in uris:
                                                uris.append(uri)
        #populate list with all uris                                                
        for uri in uris:
            if uri not in self.uris_list:
                self.uris_list.append(uri)
        return uris
    
    def getBuildProperties(self):
        properties = {}
        response = self.session.executeCommand("shell", "executeSingleCommand", {'args':'cat /system/build.prop'})
        if str(response.error) == "OK":
            data = str(response.data).split('\n')
            for element in data:
                if (not len(element) == 0) and (not element[0] == '#'):
                    parts = element.split('=')
                    if len(parts) >= 2:
                        properties[parts[0]] = parts[1]
        return properties

    def getProperties(self):
        properties = {}
        response = self.session.executeCommand("shell", "executeSingleCommand", {'args':'getprop'})        
        if str(response.error) == "OK":
            data = str(response.data).split('\n')
            for element in data:
                parts = element.split(':')
                if len(parts) >= 2:
                    parts[0] = parts[0].replace('[', '', 1);
                    parts[0] = self.rreplace(parts[0], ']', '', 1);
                    parts[1] = parts[1].replace('[', '', 1);
                    parts[1] = parts[1].replace(' ', '', 1);
                    parts[1] = self.rreplace(parts[1], ']', '', 1);
                    properties[parts[0]] = parts[1]
        return properties
    
    def getKernelVersion(self):
        response = self.session.executeCommand("shell", "executeSingleCommand", {'args':'cat /proc/version'})
        if str(response.error) == "OK":
            data = str(response.data)
            return data.partition('Linux version')[2].split(' ')[1]
        else:
            return 'Unknown'

    def rreplace(self, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)
    
    def getFromDictionary(self, dictionary, key):
        if dictionary.has_key(key):
            return dictionary[key]
        else:
            return ""
        
            
class MenuSection:
    def __init__(self, section_title="", section_links=[]):
        self.title = section_title
        self.links = section_links
        
class MenuLink:

    def __init__(self, link_title="", link_id=""):
        self.title = link_title
        self.id = link_id
        
class PackageContent:

    def __init__(self):
        self.packages = Message_pb2.PackageResponse()
        self.activity = Message_pb2.ActivityResponse()
        self.provider = Message_pb2.ProviderResponse()
        self.broadcast = Message_pb2.BroadcastResponse()
        self.service = Message_pb2.ServiceResponse()
        self.native = Message_pb2.NativeResponse()
        self.debug = Message_pb2.DebugResponse()
        self.attacksurface = Message_pb2.PackageResponse()

