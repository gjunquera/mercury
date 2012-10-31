from merc.lib.modules import Module
import os
import re
import shutil

class sslscanner(Module):
    """Description: Find SSL related and vulnerable code on apk and generates a report"""
    
    SSL_FOLDER = "ssl"
    DECOMPILED_APK_FOLDER = ""
    REPORT_FOLDER = os.path.join("ssl", "report")
    
    SSL_PATTERNS = ["SSLContext", "SSLSocketFactory", "SSLSession", "TrustManager", "AllowAllHostnameVerifier", "HttpsURLConnection", 
                     "SSLEngine", "SSLParameters", "X509ExtendedKeyManager"]
    
    X509TM_IMPL_PATTERN = [ [True, "(.*implements *X509TrustManager.*)"], [False, "(.*public void checkServerTrusted.*{.*checkServerTrusted.*})"] ]
    X509TM_NEW_PATTERN = [ [True, "(.*new *X509TrustManager.*)"], [False, "(.*public void checkServerTrusted.*{.*checkServerTrusted.*})"] ]
    SSLSOCKFAC_EXT_PATTERN = [ [True, "(.*extends SSLSocketFactory.*)"], [True, "(.*void checkServerTrusted.*)"], [False, "(.*public void checkServerTrusted.*{.*checkServerTrusted.*})"] ]    
    ALLOWALLHOSTS_PATTERN = [ [True, "(.*setHostnameVerifier\((AllowAllHostnameVerifier|new *AllowAllHostnameVerifier)\).*)"] ]
    VULNERABLE_PATTERNS = [ X509TM_IMPL_PATTERN, X509TM_NEW_PATTERN, SSLSOCKFAC_EXT_PATTERN]
    
    TOTAL_SCANNED = 0.0
    TOTAL_VULNERABLE = 0.0
    TOTAL_SSL_REFS = 0.0
          
    cert_extensions = [".pem", ".crt", ".cer", ".der", ".bks", ".pfx", ".p12", ".p7b", ".p7r", ".spc", ".sst", ".stl", ".key"]
    
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["scanner", "misc"]

    def execute(self, session, _arg):

        sslscanner.TOTAL_SCANNED = 0.0
        sslscanner.TOTAL_VULNERABLE = 0.0
        sslscanner.TOTAL_SSL_REFS = 0.0

        initial_path = os.getcwd()

        self.session = session
        package_filter = _arg.get('filter')
        decompile_str = _arg.get('decompile')
        decompiled_apks_dir = _arg.get('decompiledFolder')
        report_folder = _arg.get('reportFolder')
        
        decompile = False
        if (decompile_str != None) and (decompile_str == "true"):
            decompile = True
        if (decompiled_apks_dir is not None) and (len(decompiled_apks_dir) > 0):
            self.DECOMPILED_APK_FOLDER =  decompiled_apks_dir
            decompile = False
        else:
            self.DECOMPILED_APK_FOLDER = self.SSL_FOLDER
        if (report_folder is not None) and (len(report_folder) > 0):
            self.REPORT_FOLDER = report_folder
        else:
            self.REPORT_FOLDER = os.path.join("ssl", "report")
            
        
        path_list = []
        if decompile:
            #get the apks path on the device to pull and decompile later
            request = {'packageName': package_filter}
            ret = self.session.executeCommand("packages", "path", request)    
            # Iterate through paths returned
            for pair in ret.structured_data:
                for value in pair.value:
                    line = str(value)
                    #just a workaround to avoid decompile the framework apk 
                    if self.getApkName(line) != "framework-res.apk":
                        path_list.append(line)            
        else:
            #get the directories for the folder passed as parameter
            directories = os.listdir(self.DECOMPILED_APK_FOLDER)
            for element in directories:
                if os.path.isdir(os.path.join(self.DECOMPILED_APK_FOLDER, element)):
                    path_list.append(element)

        #list that contains the data required for the report
        apks_data = []
        
        for path in path_list:            
            apk_name = self.getApkName(path)
            folder_name = self.getFolderName(apk_name)
            if not os.path.exists(self.DECOMPILED_APK_FOLDER):
                os.mkdir(self.DECOMPILED_APK_FOLDER)
            os.chdir(self.DECOMPILED_APK_FOLDER)
            
            if decompile:
                self.decompile(folder_name, path, apk_name)

            if os.path.exists(folder_name):
                
                sslscanner.TOTAL_SCANNED += 1
                match_ssl_pattern = False
                match_vulnerable = False
                
                os.chdir(folder_name)
                certificates_list = []
                vuln_data_list = []
                ssl_data_list = []

                for root,dirs,files in os.walk(os.path.join(".")):
                    for file in files:
                        #if the file is a .java scan it
                        if file.endswith(".java"):
                            file_path = os.path.join(root, file)
                            f = open(file_path, 'r')
                            file_content = f.read()
                            f.close()
                            
                            data = None
                            #check for vulnerable patterns
                            if VulnerableData.checkVulberablePatterns(file_content):
                                match_vulnerable = True
                                data = VulnerableData(os.path.join(root, file), file_content)
                                data.vulnerable = True
                                vuln_data_list.append(data)
                                                            
                            #check for SSL references
                            data = None
                            old_file_content = file_content
                            for pattern in self.SSL_PATTERNS:
                                new_file_content, ids = SSLData.checkSSLReferenceAndCreateId(old_file_content, pattern, file_path)
                                if new_file_content != None:
                                    match_ssl_pattern = True
                                    old_file_content = new_file_content
                                    if data is None:
                                        data = SSLData(os.path.join(root, file), new_file_content, [])
                                    else:
                                        data.content = new_file_content
                                    num_ids = 0
                                    for id in ids:
                                        data.patterns.append("<a href=#" + id + ">" + pattern + " - " + str(num_ids) + "</a>")
                                        num_ids += 1
                                                                                                
                            if data != None:
                                ssl_data_list.append(data)

                        #check if the file is a certificate
                        else:
                            for ext in self.cert_extensions:
                                if file.endswith(ext):
                                    certificates_list.append(file)

                if match_ssl_pattern:
                    sslscanner.TOTAL_SSL_REFS += 1
                if match_vulnerable:
                    sslscanner.TOTAL_VULNERABLE += 1
                apks_data.append(ApkData(apk_name=apk_name, vuln_data=vuln_data_list, certificate_files=certificates_list, ssl_data=ssl_data_list))                                             
                #back to the initial directory
                os.chdir(initial_path)
                
            else:
                #back to the initial directory
                os.chdir(initial_path)
        
        #generate the report
        report = Report(apks_data)
        generate_index = True
        if (package_filter != None) and (len(package_filter) > 0):
            generate_index = False
        report.generateReport(self.REPORT_FOLDER, generate_index)
        
    def decompile(self, folder_name, path, apk_name):
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
     
    def getApkName(self, path):
        path_split = path.split("/")
        if (len(path_split)) > 0:
            apk_name = path_split[len(path_split) - 1]
            return apk_name
        else:
            path_split = path.split("/")
            if (len(path_split)) > 0:
                apk_name = path_split[len(path_split) - 1]
                return apk_name
        return path
    
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
    
class VulnerableData:
    def __init__(self, file_name="", file_content=""):
        self.name = file_name
        self.content = file_content
        self.vulnerable = False
        
    @staticmethod
    def checkVulberablePattern(file_content="", pattern=[]):
        for element in pattern:
            if element[0] != VulnerableData.checkPattern(file_content, element[1]):
                return False
        return True

    #Returns true if one vulnerable pattern matches
    @staticmethod
    def checkVulberablePatterns(file_content=""):
        for pattern in sslscanner.VULNERABLE_PATTERNS:
            if VulnerableData.checkVulberablePattern(file_content, pattern):
                return True
        return False
    
    @staticmethod
    def checkPattern(file_content="", pattern=""):
        content = file_content.replace("\n", "")
        regex = re.compile(pattern)
        match = regex.match(content)              
        if match != None:
            return True
        return False     
        
class SSLData:
    def __init__(self, file_name="", file_content="", patterns=[], vulnerable=False):
        self.name = file_name
        self.content = file_content
        self.patterns = patterns
        self.vulnerable = vulnerable
        
    @staticmethod
    def isList(var):
        if type(var) is list:
            return True
        return False
        
    @staticmethod
    def checkSSLReference(file_content="", pattern=""):
        lines = file_content.split("\n")
        for line in lines:
            regex = re.compile('(.*' + pattern + '.*)')
            match = regex.match(line)              
            if match != None:
                return True
        return False

    @staticmethod
    def checkSSLReferenceAndCreateId(file_content="", pattern="", file_name=""):
        lines = file_content.split("\n")
        new_file_content = ""
        num_matches = 0
        ids = []
        for line in lines:
            regex = re.compile('.*(' + pattern + ').*')
            match = regex.match(line)
            if match != None:
                match_str = match.group()
                ids.append(file_name + pattern + str(num_matches))
                new_line =  match_str.replace(pattern, "<b id=\"" + file_name + pattern + str(num_matches) + "\" style=\"color:red;\">" + pattern + "</b>")
                new_file_content += new_line + "\n"
                num_matches += 1 
            else:
                new_file_content += line + "\n"
        if num_matches > 0:
            return new_file_content, ids
        else:
            return None, ids
        
class ApkData:
    def __init__(self, apk_name="", vuln_data=[], certificate_files=[], ssl_data=[]):
        self.apk_name = apk_name
        self.vuln_data = vuln_data
        self.cert_files = certificate_files
        self.ssl_data = ssl_data

class Report:
    def __init__(self, apks_data=[]):
        self.apks_data = apks_data
        
    def generateReport(self, dest_folder=os.path.join("ssl", "report"), generate_index=True):
        
        index_summary_links = []
        index_summary_links.append(Report.MenuLink("Summary", "#summary"))
        index_summary_links.append(Report.MenuLink("Vulnerable Apks", "#vulnApks"))
#        index_summary_links.append(Report.MenuLink("Apks with X509TrustManager", "#X509TMApks"))
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
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            
        if generate_index:
            self.createHtmlFile(index_html, os.path.join(os.getcwd(), dest_folder), "index")
        
        for apk_data in self.apks_data:
            #creating the links for package files
            apk_links = []
            apk_links.append(Report.MenuLink("Certificate Files", "#certFiles"))
            apk_links.append(Report.MenuLink("Vulnerable Files List", "#VulnList"))
            apk_links.append(Report.MenuLink("Vulnerable Files Content", "#VulnContent"))
            apk_links.append(Report.MenuLink("SSL Files List", "#SSLList"))
            apk_links.append(Report.MenuLink("SSL Files Content", "#SSLContent"))
                
            #creating the sections for report index file
            apk_sections = []
            apk_sections.append(Report.MenuSection("Package SSL Info", apk_links))
            
            package_html = self.makeApkHtml(apk_data.apk_name, apk_sections, apk_data, apk_data.apk_name)
            file_name = apk_data.apk_name.split(".apk")[0]
            self.createHtmlFile(package_html, os.path.join(os.getcwd(), dest_folder), file_name)

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
    
    def makeIndexContent(self, content, title):
        html = "<div id=\"content\">\n"
        html += "<p id=\"title\">" + title + "</p>\n"
        html += self.makeSummaryHtml() + "\n"
        html += self.makeVulnerableApksHtml() + "\n"
#        html += self.makeX509RefsHtml() + "\n"
        html += self.makeSSLRefsHtml() + "\n"
        html += "</div>"
        return html
    
    def makeSummaryHtml(self):
        html = "<p id=\"summary\" class=\"section_title\">Summary</p>\n"
        lines = []
        lines.append(["TOTAL SCANNED APKS", str(int(sslscanner.TOTAL_SCANNED))])
        lines.append(["TOTAL SSL APKS", str(int(sslscanner.TOTAL_SSL_REFS))])
        lines.append(["TOTAL VULNERABLE APKS", str(int(sslscanner.TOTAL_VULNERABLE))])
        ssl_percentage = 0
        vulnerable_percentage = 0
        vulnerable_ssl_percentage = 0
        if sslscanner.TOTAL_SCANNED > 0:
            ssl_percentage = int((sslscanner.TOTAL_SSL_REFS / sslscanner.TOTAL_SCANNED) * 100)
            vulnerable_percentage = int((sslscanner.TOTAL_VULNERABLE / sslscanner.TOTAL_SCANNED) * 100)
        if sslscanner.TOTAL_SSL_REFS > 0:
            vulnerable_ssl_percentage = int((sslscanner.TOTAL_VULNERABLE / sslscanner.TOTAL_SSL_REFS) * 100) 
        lines.append(["SSL APKS PERCENTAGE", str(ssl_percentage) + "%"])
        lines.append(["VULNERABLE APKS PERCENTAGE", str(vulnerable_percentage) + "%"])
        lines.append(["VULNERABLE SSL APKS PERCENTAGE", str(vulnerable_ssl_percentage) + "%"])
        html += self.makeTable(lines) + "\n"
        return html
    
    def makeVulnerableApksHtml(self):
        html = "<p id=\"vulnApks\" class=\"section_title\">Vulnerable Apks</p>\n"
        lines = []
        for apk_data in self.apks_data:
            for vuln_data in apk_data.vuln_data:
                if vuln_data.vulnerable:
                    lines.append([self.linkfyApkName(apk_data.apk_name)])
                    break;
                                                    
        html += self.makeTable(lines) + "\n"
        return html

#    def makeX509RefsHtml(self):
#        lines = []
#        for apk_data in self.apks_data:
#            if len(apk_data.vuln_data) > 0:
#                lines.append([self.linkfyApkName(apk_data.apk_name)])
#        return self.makeRefsHtml("X509TMApks", "Apks that implements X509TrustManager", lines)

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
        html += self.makeVulnListHtml(apk_data.vuln_data) + "\n"
        html += self.makeFileContentHtml(apk_data.vuln_data, "Vulnerable Files Content", "VulnContent") + "\n"
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
    
    def makeVulnListHtml(self, data):
        html = "<p id=\"VulnList\" class=\"section_title\">Vulnerable Files List</p>\n"
        lines = []
        for vuln_data in data:
            file_link = "<a href=\"#" + vuln_data.name + "\">" + vuln_data.name + "</a>"
#            if vuln_data.vulnerable:
            lines.append([file_link, "This class is VULNERABLE to MITM"])
#            else:
#                lines.append([file_link, "This class is NOT VULNERABLE"])                
        html += self.makeTable(lines) + "\n"
        return html
    
    def makeSSLListHtml(self, data):
        html = "<p id=\"SSLList\" class=\"section_title\">Files with SSL References</p>\n"
        lines = []
        lines.append(["<b>Files</b>", "<b>Patterns Found</b>", "<b>Comments</b>"])
        for ssl_data in data:
            pattern_html = ""
            for pattern in ssl_data.patterns:
                pattern_html += pattern + "<br>"
            file_link = "<a href=\"#" + ssl_data.name + "\">" + ssl_data.name + "</a>"
            if ssl_data.vulnerable:
                lines.append([file_link, pattern_html, "This class is VULNERABLE to MITM"])
            else:
                lines.append([file_link, pattern_html, ""])
        html += self.makeTable(lines) + "\n"
        return html    

    def makeFileContentHtml(self, data, title, id):
        html = "<p id=\"" + id + "\" class=\"section_title\">" + title + "</p>\n"
        for element in data:
            lines = []
            html += "<br><br><p id=\"" + element.name + "\"><b>" + element.name + "</b></p><br>\n"
            html_content = element.content.replace("\n", "<br>")
            html_content = html_content.replace(" ", "&nbsp;")
            #workaround to properly create id on bold text
            html_content = html_content.replace("<b&nbsp;id=\"", "<b id=\"")
            html_content = html_content.replace("\"&nbsp;style=\"color:red;\">", "\" style=\"color:red;\">")
            
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
