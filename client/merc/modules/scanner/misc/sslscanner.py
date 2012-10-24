from merc.lib.modules import Module
import os
import re
import shutil

class sslscanner(Module):
    """Description: Find SSL related code on apk"""

    SSL_FOLDER = "ssl"
    REPORT_FOLDER = os.path.join("ssl", "report")
    
    SSL_PATTERNS = ["SSLContext", "SSLSocketFactory", "SSLContextFactory"]
    
    cert_extensions = [".pem", ".crt", ".cer", ".der", ".bks", ".pfx", ".p12", ".p7b", ".p7r", ".spc", ".sst", ".stl", ".key"]
    
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["scanner", "misc"]

    def execute(self, session, _arg):

        initial_path = os.getcwd()

        self.session = session
        package_filter = _arg.get('filter')
        decompile_str = _arg.get('decompile')
        
        decompile = False
        if (decompile_str != None) and (decompile_str == "true"):
            decompile = True
            
        request = {'packageName': package_filter}
        #get the apks path
        ret = self.session.executeCommand("packages", "path", request)
        path_list = []
        if os.path.exists("result_ssl.txt"):
            os.remove("result_ssl.txt")
        
        # Iterate through paths returned
        for pair in ret.structured_data:
            for value in pair.value:
                line = str(value)
                #just a workaround to avoid decompile the framework apk 
                if self.getApkName(line) != "framework-res.apk":
                    path_list.append(line)

        #list that contains the data required for the report
        apks_data = []
        
        #pull the apks from the phone
        for path in path_list:
            
            #pull the apks from the phone
            apk_name = self.getApkName(path)
            folder_name = self.getFolderName(apk_name)
            if not os.path.exists(self.SSL_FOLDER):
                os.mkdir(self.SSL_FOLDER)
            os.chdir(self.SSL_FOLDER)
            
            if decompile:
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
    
                os.system("adb pull " + path + " " + folder_name + "/.")
            
                #Decompile the apk and create a jar
                #d2j-dex2jar.bat -f -o %1-dex2jar.jar %1.apk
                os.chdir(folder_name)
                jar_name = folder_name + "-dex2jar.jar"
                os.system("d2j-dex2jar.bat -f -o " + jar_name + " " + apk_name)
            
                #create java files from jar
                if not os.path.exists("java"):
                    os.mkdir("java")
                os.system("move " + folder_name + "-dex2jar.jar java/.")
                os.chdir("java")
                os.system("jar xf " + folder_name + "-dex2jar.jar")
                os.system("jad -o -r -sjava -dsrc **/*.class")
                
                #clean unused files
                dir_list = os.listdir(os.path.join("."))
                for dir_name in dir_list:
                    if dir_name != "src":
                        if not os.path.isfile(dir_name):
                            self.rm_rf(dir_name)

            if os.path.exists(folder_name):                            
                os.chdir(folder_name)
                matches_list = []
                certificates_list = []
                tm_data_list = []
                ssl_data_list = []

                #find SSL related patterns 
                for root,dirs,files in os.walk(os.path.join(".")):
                    for file in files:
                        if file.endswith(".java"):
                            file_path = os.path.join(root, file)
                            f = open(file_path, 'r')
                            file_content = f.read()
                            f.close()
                            #check if the file implements X509TrustManager
                            if X509TMData.checkX509TrustManager(file_content):
                                data = X509TMData(os.path.join(root, file), file_content)
                                matches_list.append(file_path)
                                data.vulnerable = X509TMData.checkVulnerableServerTrusted(file_content)
                                tm_data_list.append(data)
                                
                            #check for SSL references
                            data = None
                            for pattern in self.SSL_PATTERNS:
                                if SSLData.checkSSLReference(file_content, pattern):
                                    if data is None:
                                        data = SSLData(os.path.join(root, file), file_content, [])
                                    data.patterns.append(pattern)
                                    
                            if SSLData.checkSSLReference(file_content, "extends SSLSocketFactory"):
                                if data is None:
                                    data = SSLData(os.path.join(root, file), file_content, [])
                                data.vulnerable = X509TMData.checkVulnerableServerTrusted(file_content)
                                                                    
                            if data != None:
                                ssl_data_list.append(data)

                        #check if the file is a certificate
                        else:
                            for ext in self.cert_extensions:
                                if file.endswith(ext):
                                    certificates_list.append(file)

                apks_data.append(ApkData(apk_name=apk_name, tm_data=tm_data_list, certificate_files=certificates_list, ssl_data=ssl_data_list))                                             
                #back to the initial directory
                os.chdir(initial_path)
                
                #write result to file
                #result_file = open("result_ssl.txt", "a")
                #result_file.write("\nFiles found on " + folder_name + ":\n")
                #for match in matches_list:
                #    result_file.write("    " + match + "\n")
                #result_file.close()
            else:
                #back to the initial directory
                os.chdir(initial_path)
        
        report = Report(apks_data)        
        report.generateReport()
             
    def getApkName(self, path):
        path_split = path.split("/")
        apk_name = path_split[len(path_split) - 1]
        return apk_name
    
    def getFolderName(self, apk_name):
        folder_name = apk_name.split(".apk")[0]
        return folder_name
    
    def rm_rf(self, d):
        if not os.path.isdir(d):
            return
        for path in (os.path.join(d,f) for f in os.listdir(d)):
            if os.path.isdir(path):
                self.rm_rf(path)
            else:
                os.unlink(path)
        os.rmdir(d)
    
class X509TMData:
    def __init__(self, file_name="", file_content=""):
        self.name = file_name
        self.content = file_content
        self.vulnerable = False
        
    @staticmethod
    def checkX509TrustManager(file_content=""):
        lines = file_content.split("\n")
        for line in lines:                                
            match = re.match(r'(.*implements X509TrustManager.*)', line)
            if match != None:
                return True
        return False

    @staticmethod
    def checkVulnerableServerTrusted(file_content=""):
        content = file_content.replace("\n", "")
        match = re.match(r'(.*public void checkServerTrusted.*{.*checkServerTrusted.*})', content)
        if match != None:
            #the class is not vulnerable
            return False
        #the class is vulnerable
        return True
        
class SSLData:
    def __init__(self, file_name="", file_content="", patterns=[], vulnerable=False):
        self.name = file_name
        self.content = file_content
        self.patterns = patterns
        self.vulnerable = vulnerable
        
    @staticmethod
    def checkSSLReference(file_content="", pattern=""):
        lines = file_content.split("\n")
        for line in lines:
            regex = re.compile('(.*' + pattern + '.*)')
            match = regex.match(line)              
            if match != None:
                return True
        return False
        
class ApkData:
    def __init__(self, apk_name="", tm_data=[], certificate_files=[], ssl_data=[]):
        self.apk_name = apk_name
        self.tm_data = tm_data
        self.cert_files = certificate_files
        self.ssl_data = ssl_data

class Report:
    def __init__(self, apks_data=[]):
        self.apks_data = apks_data
        
    def generateReport(self):
        
        index_summary_links = []
        index_summary_links.append(Report.MenuLink("Vulnerable Apks", "#vulnApks"))
        index_summary_links.append(Report.MenuLink("Apks with X509TrustManager", "#X509TMApks"))
        index_summary_links.append(Report.MenuLink("Apks with SSL", "#SSLApks"))
        
        #creating the links for index file menu
        index_scanned_links = []
        for apk_data in self.apks_data:
            file_name = apk_data.apk_name.split(".apk")[0]
            index_scanned_links.append(Report.MenuLink(apk_data.apk_name, file_name + ".html"))
            
        #creating the sections for report index file
        index_sections = []
        index_sections.append(Report.MenuSection("Summary", index_summary_links))
        index_sections.append(Report.MenuSection("Scanned Apks", index_scanned_links))
        
        index_html = self.makeIndexHtml("SSL Report", index_sections, "")
        if not os.path.exists(sslscanner.REPORT_FOLDER):
            os.mkdir(sslscanner.REPORT_FOLDER)
        self.createHtmlFile(index_html, os.path.join(os.getcwd(), sslscanner.REPORT_FOLDER), "index")
        
        for apk_data in self.apks_data:
            #creating the links for package files
            apk_links = []
            apk_links.append(Report.MenuLink("Certificate Files", "#certFiles"))
            apk_links.append(Report.MenuLink("X509TrustManager Files List", "#X509TMList"))
            apk_links.append(Report.MenuLink("X509TrustManager Files Content", "#X509TMContent"))
            apk_links.append(Report.MenuLink("SSL Files List", "#SSLList"))
            apk_links.append(Report.MenuLink("SSL Files Content", "#SSLContent"))
                
            #creating the sections for report index file
            apk_sections = []
            apk_sections.append(Report.MenuSection("Package SSL Info", apk_links))
            
            package_html = self.makeApkHtml(apk_data.apk_name, apk_sections, apk_data, apk_data.apk_name)
            file_name = apk_data.apk_name.split(".apk")[0]
            self.createHtmlFile(package_html, os.path.join(os.getcwd(), sslscanner.REPORT_FOLDER), file_name)

        self.copyCssToDestination(sslscanner.REPORT_FOLDER)            
        
        
    def makeIndexHtml(self, title, menu_sections, content):
        html = "<html>\n"
        html += "<link rel=\"stylesheet\" href=\"report.css\">\n"
        html += "<body>\n"
        html += self.makeMenu(menu_sections) + "\n"
        html += self.makeIndexContent(content, title) + "\n"
        html += "</body>\n"
        html += "</html>"      
        return html
    
    def makeIndexContent(self, content, title):
        html = "<div id=\"content\">\n"
        html += "<p id=\"title\">" + title + "</p>\n"
        html += self.makeVulnerableApksHtml() + "\n"
        html += self.makeX509RefsHtml() + "\n"
        html += self.makeSSLRefsHtml() + "\n"
        html += "</div>"
        return html
    
    def makeVulnerableApksHtml(self):
        html = "<p id=\"vulnApks\" class=\"section_title\">Vulnerable Apks</p>\n"
        lines = []
        for apk_data in self.apks_data:
            found = False
            for tm_data in apk_data.tm_data:
                if tm_data.vulnerable:
                    lines.append([self.linkfyApkName(apk_data.apk_name)])
                    found = True
                    break;
            if not found:
                for ssl_data in apk_data.ssl_data:
                    if ssl_data.vulnerable:
                        lines.append([self.linkfyApkName(apk_data.apk_name)])
                        break;
                                                    
        html += self.makeTable(lines) + "\n"
        return html

    def makeX509RefsHtml(self):
        lines = []
        for apk_data in self.apks_data:
            if len(apk_data.tm_data) > 0:
                lines.append([self.linkfyApkName(apk_data.apk_name)])
        return self.makeRefsHtml("X509TMApks", "Apks that implements X509TrustManager", lines)

    def makeSSLRefsHtml(self):
        lines = []
        for apk_data in self.apks_data:
            if len(apk_data.ssl_data) > 0:
                lines.append([self.linkfyApkName(apk_data.apk_name)])
        return self.makeRefsHtml("SSLApks", "Apks with SSL references", lines)
    
    def makeRefsHtml(self, id="", title="", lines=[]):
        html = "<p id=\"" + id + "\" class=\"section_title\">" + title + "</p>\n"
        html += self.makeTable(lines) + "\n"
        return html
    
    def linkfyApkName(self, apk_name):
        link = apk_name.split(".apk")[0] + ".html"
        return "<a href=\"" + link + "\">" + apk_name + "</a>"
        
    
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
    
    def makeApkHtml(self, title, menu_sections, content, package):
        html = "<html>\n"
        html += "<link rel=\"stylesheet\" href=\"report.css\">\n"
        html += "<body>\n"
        html += self.makeMenu(menu_sections) + "\n"
        html += self.makeApkContent(content, package, title) + "\n"
        html += "</body>\n"
        html += "</html>"
        return html    
    
    def makeApkContent(self, apk_data, package, title):
        html = "<div id=\"content\">\n"
        html += "<p id=\"title\">" + title + "</p>\n"
        html += self.makeCertificatesList(apk_data.cert_files) + "\n"
        html += self.makeX509TMListHtml(apk_data.tm_data) + "\n"
        html += self.makeFileContentHtml(apk_data.tm_data, "X509TrustManager Files Content", "X509TMContent") + "\n"
        html += self.makeSSLListHtml(apk_data.ssl_data)
        html += self.makeFileContentHtml(apk_data.ssl_data, "SSL Files Content", "SSLContent") + "\n"
        return html
    
    def makeCertificatesList(self, cert_list):
        html = "<p id=\"certFiles\" class=\"section_title\">Certificate Files Found</p>\n"
        lines = []
        for cert in cert_list:
            lines.append([cert])                
        html += self.makeTable(lines) + "\n"
        return html        
    
    def makeX509TMListHtml(self, data):
        html = "<p id=\"X509TMList\" class=\"section_title\">X509TrustManager Files List</p>\n"
        lines = []
        for tm_data in data:
            file_link = "<a href=\"#" + tm_data.name + "\">" + tm_data.name + "</a>"
            if tm_data.vulnerable:
                lines.append([file_link, "This class is VULNERABLE to MITM"])
            else:
                lines.append([file_link, "This class is NOT VULNERABLE"])                
        html += self.makeTable(lines) + "\n"
        return html
    
    def makeSSLListHtml(self, data):
        html = "<p id=\"SSLList\" class=\"section_title\">Files with SSL References</p>\n"
        lines = []
        lines.append(["<b>Files</b>", "<b>Patterns Found</b>"])
        for ssl_data in data:
            pattern_html = ""
            for pattern in ssl_data.patterns:
                pattern_html += pattern + "<br>"
            file_link = "<a href=\"#" + ssl_data.name + "\">" + ssl_data.name + "</a>"
            lines.append([file_link, pattern_html])
        html += self.makeTable(lines) + "\n"
        return html    

    def makeFileContentHtml(self, data, title, id):
        html = "<p id=\"" + id + "\" class=\"section_title\">" + title + "</p>\n"
        for element in data:
            lines = []
            html += "<br><br><p id=\"" + element.name + "\"><b>" + element.name + "</b></p><br>\n"
            html_content = element.content.replace("\n", "<br>")
            html_content = html_content.replace(" ", "&nbsp;")
            lines.append([html_content])                
            html += self.makeTable(lines) + "\n"
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
    
    def createHtmlFile(self, html="", path="", filename="generated_html"):
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path, filename + ".html"), 'w')
        f.write(html)
        f.close()
        
    def copyCssToDestination(self, dest_path=""):
        current_path = os.getcwd()
        shutil.copyfile(os.path.join(current_path, "merc", "modules", "information", "report", "report.css"), os.path.join(dest_path, "report.css"))        
    
    class MenuSection:
        def __init__(self, section_title="", section_links=[]):
            self.title = section_title
            self.links = section_links
            
    class MenuLink:
        def __init__(self, link_title="", link_id=""):
            self.title = link_title
            self.id = link_id
