from merc.lib.modules import Module
from merc.lib import Message_pb2

class Report(Module):
    """Description: Use Mercury Commands to create a HTML Report
Credit: Glauco Junquera - Samsung SIDI"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information", "report"]

    def execute(self, session, _arg):
        
        content = PackageContent()
        
        #Request packages info
        request = {'filter': None, 'output': None, 'permissions': None}
        response = session.executeCommand("packages", "info", request)
        content.packages.ParseFromString(str(response.data))
        
        #Request service info
        request = {'filter': None, 'output': None, 'permissions': None}        
        response = session.executeCommand("service", "info", request)
        content.service.ParseFromString(str(response.data))
            
        #Request activity info
        request = {'filter': None, 'output': None}                    
        response = session.executeCommand("activity", "info", request)
        content.activity.ParseFromString(str(response.data))
            
        #Request provider info
        request = {'filter': None, 'output': None, 'permissions': None}                    
        response = session.executeCommand("provider", "info", request)
        content.provider.ParseFromString(str(response.data))
        
        #Request Broadcast Receiver info
        request = {'filter': None, 'output': None, 'permissions': None}
        response = session.executeCommand("broadcast", "info", request)
        content.broadcast.ParseFromString(str(response.data))
        
        #Request Native Info
        request = {'filter': None, 'output': None}
        response = session.executeCommand("native", "info", request)
        content.native.ParseFromString(str(response.data))
        
        #Request Debuggable Info
        request = {'filter': None, 'output': None}
        response = session.executeCommand("debuggable", "info", request)
        content.debug.ParseFromString(str(response.data))

#TODO
        #Request Attack Surface Info
#        request = {'packageName': None}        
#        response = self.session.executeCommand("packages", "attacksurface", {'packageName':splitargs.packageName})
        
        general_links = []
        general_links.append(MenuLink("Package Info", "#packageInfo"))
        
        components_links = []
        components_links.append(MenuLink("Activities", "#activities"))
        components_links.append(MenuLink("Broadcast Receivers", "#receivers"))
        components_links.append(MenuLink("Content Providers", "#providers"))
        components_links.append(MenuLink("Services", "#services"))
        components_links.append(MenuLink("Native Libraries", "#native"))
        
        general_sections = []
        general_sections.append(MenuSection("General Info", general_links))
        general_sections.append(MenuSection("Package Components", components_links))

        package_names = []
        #crate an html for each package
        for info in content.packages.info:
            package_names.append(str(info.packageName))
            html = self.makePackageHtml(str(info.packageName), general_sections, content, str(info.packageName))
            self.copyHtmlToFile(html, "report/" + str(info.packageName) + ".html")
            
        #create index page menu links
        general_links = []
        general_links.append(MenuLink("Debug Packages", "#debug"))
        
        package_links = []
        for package in package_names:
            package_links.append(MenuLink(package, package + ".html"))
            
        index_sections = []
        index_sections.append(MenuSection("Debug Packages", general_links))
        index_sections.append(MenuSection("Packages", package_links))
        
        html = self.makeGeneralHtml("Mercury Report", index_sections, content)
        self.copyHtmlToFile(html, "report/report_index.html")        
        
    def makeGeneralHtml(self, title, menu_sections, content):
        html = "<html>\n"
        html += "<link rel=\"stylesheet\" href=\"report.css\">\n"
        html += "<body>\n"
        html += self.makeHeader(title) + "\n"
        html += self.makeMenu(menu_sections) + "\n"
        html += self.makeGeneralContent(content) + "\n"
        html += "</body>\n"
        html += "</html>"                
        return html

    def makePackageHtml(self, title, menu_sections, content, package):
        html = "<html>\n"
        html += "<link rel=\"stylesheet\" href=\"report.css\">\n"
        html += "<body>\n"
        html += self.makeHeader(title) + "\n"
        html += self.makeMenu(menu_sections) + "\n"
        html += self.makePackageContent(content, package) + "\n"
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
    
    def makePackageContent(self, content, package):
        html = "<div id=\"content\">\n"
        html += self.makePackageGeneralInfoHtml(content.packages, package) + "\n"
        html += self.makeActivityHtml(content.activity, package) + "\n"
        html += self.makeBroadcastHtml(content.broadcast, package) + "\n"
        html += self.makeProviderHtml(content.provider, package) + "\n"
        html += self.makeServiceHtml(content.service, package) + "\n"
        html += self.makeNativeHtml(content.native, package) + "\n"        
        html += "</div>"
        return html
    
    def makeGeneralContent(self, content):
        html = "<div id=\"content\">\n"
        html += self.makeDebugHtml(content.debug) + "\n"
        html += "</div>"        
        return html
    
    def makeServiceHtml(self, content, package=None):
        html = "<p id=\"services\">Services</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
#                lines.append(["Package Name", str(info.packageName)])
                lines.append(["Service", str(info.service)])
                lines.append(["Required Permission", str(info.permission)])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeActivityHtml(self, content, package=None):
        html = "<p id=\"activities\">Activities</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
                lines.append([str(info.activity)])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeProviderHtml(self, content, package=None):
        html = "<p id=\"providers\">Content Providers</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
#                lines.append(["PackageName",  str(info.packageName)])
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
    
    def makeBroadcastHtml(self, content, package=None):
        html = "<p id=\"receivers\">Broadcast Receivers</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
#                lines.append(["Package name", str(info.packageName)])
                lines.append(["Receiver", str(info.receiver)])
                lines.append(["Required Permission", str(info.permission)])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeNativeHtml(self, content, package=None):
        html = "<p id=\"native\">Native Libraries</p>\n"
        for info in content.info:
            if (package != None) and (package == str(info.packageName)):
                lines = []
#                lines.append(["Package name", str(info.packageName)])
                for native in info.nativeLib:
                    lines.append([native])
                html += self.makeTable(lines) + "\n"
        return html
    
    def makeDebugHtml(self, content, package=None):
        html = "<p id=\"debug\">Debuggable Packages</p>\n"
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
    
    def makePackageGeneralInfoHtml(self, content, package=None):
        html = "<p id=\"packageInfo\">Package Info</p>\n"
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
                lines.append(["Permission", permission_str])
                html += self.makeTable(lines) + "\n"
        return html
    
    def copyHtmlToFile(self, html="", path="generated_report.html"):
        f = open(path, 'w')
        f.write(html)
        f.close()
            
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
