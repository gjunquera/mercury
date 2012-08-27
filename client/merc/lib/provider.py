#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import shlex
import Message_pb2
from interface import BaseCmd, BaseArgumentParser

class Provider(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#provider> "

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1

    def do_columns(self, args):
        """
Get the columns of the specified content uri
usage: columns [--output <file>] uri

--------------------------------
Example - finding the columns on content://settings/secure
--------------------------------
*mercury#provider> columns content://settings/secure

_id | name | value
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'columns', add_help = False)
        parser.add_argument('uri')
        
        parser.setOutputToFileOption()

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = {}

            if (splitargs.uri):
                request['uri'] = splitargs.uri

            response = self.session.executeCommand("provider", "columns", request)
            msg = "| "
            if response.error == "OK":
                for pair in response.structured_data:
                    for column in pair.value:
                        msg += str(column) + " | "
            else:
                msg += response.error
            print msg
        # FIXME: Choose specific exceptions to catch
        except Exception as e:
            pass

    def do_query(self, args):
        """
Query the specified content provider
usage: query [--projection <column> [<column> ...]] [--selection <rows>]
             [--selectionArgs <arg> [<arg> ...]] [--sortOrder <order>]
             [--showColumns <true/false>] [--output <file>]
             Uri

             
The general structure of a content URI is:
content://authority/table

--------------------------------
Example - querying the settings content provider
--------------------------------
*mercury#provider> query content://settings/secure

_id | name | value
.....

5 | assisted_gps_enabled | 1

9 | wifi_networks_available_notification_on | 1

10 | sys_storage_full_threshold_bytes | 2097152

11 | sys_storage_threshold_percentage | 10

12 | preferred_network_mode | 3

13 | cdma_cell_broadcast_sms | 1

14 | preferred_cdma_subscription | 1

15 | mock_location | 0

17 | backup_transport | com.google.android.backup/.BackupTransportService

18 | throttle_polling_sec | 600

...
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'query', add_help = False)
        parser.add_argument('--projection', '-p', nargs = '+', metavar = '<column>')
        parser.add_argument('--selection', '-s', metavar = '<rows>')
        parser.add_argument('--selectionArgs', '-sa', nargs = '+', metavar = '<arg>')
        parser.add_argument('--sortOrder', '-so', metavar = '<order>')
        parser.add_argument('--showColumns', '-nc', metavar = '<true/false>')
        parser.add_argument('Uri')
        
        parser.setOutputToFileOption()

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            response = self.session.executeCommand("provider", "query", request)
            if str(response.error) == "OK":
                for pair in response.structured_data:
                    msg = "| "
                    for value in pair.value:
                        msg += str(value) + " | "
                    print msg + "\n"

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass
        
    def do_read(self, args):
        """
Read from the specified content uri using openInputStream
usage: read [--output <file>] Uri

--------------------------------
Example - attempting a directory traversal on a content provider that does not support file reading
--------------------------------
*mercury#provider> read content://settings/secure/../../../../../../../../../../../system/etc/hosts

No files supported by provider at content://settings/secure/../../../../../../../../../../../system/etc/hosts
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'read', add_help = False)
        parser.add_argument('Uri')
        
        parser.setOutputToFileOption()

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)
            
            response = self.session.executeCommand("provider", "read", request)
            print str(response.data)

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass


    def do_insert(self, args):
        """
Insert into the specified content uri
usage: insert Uri [--string column=data [column=data ...]]
              [--boolean column=data [column=data ...]]
              [--integer column=data [column=data ...]]
              [--double column=data [column=data ...]]
              [--float column=data [column=data ...]]
              [--long column=data [column=data ...]]
              [--short column=data [column=data ...]]
              
----------------------------------------------------------------
Example - insert a new item into a content provider
----------------------------------------------------------------
*mercury#provider> insert content://com.vulnerable.im/messages --string date=1331763850325 type=0 --integer _id=7

content://com.vulnerable.im/messages/3
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'insert', add_help = False)
        parser.add_argument('--string', '-s', nargs = '+', metavar = 'column=data')
        parser.add_argument('--boolean', '-b', nargs = '+', metavar = 'column=data')
        parser.add_argument('--integer', '-i', nargs = '+', metavar = 'column=data')
        parser.add_argument('--double', '-d', nargs = '+', metavar = 'column=data')
        parser.add_argument('--float', '-f', nargs = '+', metavar = 'column=data')
        parser.add_argument('--long', '-l', nargs = '+', metavar = 'column=data')
        parser.add_argument('--short', '-sh', nargs = '+', metavar = 'column=data')
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            response = self.session.executeCommand("provider", "insert", request)
            print str(response.data)

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass

    def do_delete(self, args):
        """
Delete from the specified content uri
usage: delete Uri [--where <where>] [--selectionArgs <arg> [<arg> ...]]
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'delete', add_help = False)
        parser.add_argument('--where', '-w', metavar = '<where>')
        parser.add_argument('--selectionArgs', '-sa', nargs = '+', metavar = '<arg>')
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            response = self.session.executeCommand("provider", "delete", request)
           
            for pair in response.structured_data:
                for pair in response.structured_data:
                    if pair.key == "rows_deleted":
                        for value in pair.value:
                            print str(value) + " rows have been deleted."

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass

    def do_update(self, args):
        """
Update the specified content uri
usage: update Uri [--string column=data [column=data ...]]
              [--boolean column=data [column=data ...]]
              [--integer column=data [column=data ...]]
              [--double column=data [column=data ...]]
              [--float column=data [column=data ...]]
              [--long column=data [column=data ...]]
              [--short column=data [column=data ...]] [--where <where>]
              [--selectionArgs <arg> [<arg> ...]]
              
----------------------------------------------------------------
Example - updating an item in a content provider
----------------------------------------------------------------
*mercury#provider> update content://com.vulnerable.im/messages --string date=1331930604655 contact=lolzcopter41 account=3 body="Hi" --where _id=3


1 rows have been updated.
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'update', add_help = False)
        parser.add_argument('--string', '-s', nargs = '+', metavar = 'column=data')
        parser.add_argument('--boolean', '-b', nargs = '+', metavar = 'column=data')
        parser.add_argument('--integer', '-i', nargs = '+', metavar = 'column=data')
        parser.add_argument('--double', '-d', nargs = '+', metavar = 'column=data')
        parser.add_argument('--float', '-f', nargs = '+', metavar = 'column=data')
        parser.add_argument('--long', '-l', nargs = '+', metavar = 'column=data')
        parser.add_argument('--short', '-sh', nargs = '+', metavar = 'column=data')
        parser.add_argument('--where', '-w', metavar = '<where>')
        parser.add_argument('--selectionArgs', '-sa', nargs = '+', metavar = '<arg>')
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            response = self.session.executeCommand("provider", "update", request)
           
            for pair in response.structured_data:
                if pair.key == "rows_updated":
                    for value in pair.value:
                        print str(value) + " rows have been updated." 

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass


    def do_info(self, args):
        """
Get information about exported content providers with optional filters. . It is possible to search for keywords in content provider information and permissions using the filters.
usage: info [--filter <filter>] [--permissions <filter>] [--output <file>]

--------------------------------
Example - finding all content provider with the keyword "settings" in them
--------------------------------
*mercury#provider> info -f settings

Package name: com.google.android.gsf
Authority: com.google.settings
Required Permission - Read: null
Required Permission - Write: com.google.android.providers.settings.permission.WRITE_GSETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

Package name: com.android.providers.settings
Authority: settings
Required Permission - Read: null
Required Permission - Write: android.permission.WRITE_SETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

--------------------------------
Example - finding all content providers that do not require any permissions to read from them or write to them
--------------------------------
*mercury#provider> info -p null

Package name: com.google.android.gsf
Authority: com.google.settings
Required Permission - Read: null
Required Permission - Write: com.google.android.providers.settings.permission.WRITE_GSETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

Package name: com.android.providers.settings
Authority: settings
Required Permission - Read: null
Required Permission - Write: android.permission.WRITE_SETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

Package name: com.google.android.apps.uploader
Authority: com.google.android.apps.uploader
Required Permission - Read: null
Required Permission - Write: null
Grant Uri Permissions: false
Multiprocess allowed: false

...
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')
        parser.add_argument('--permissions', '-p', metavar = '<filter>')
        
        parser.setOutputToFileOption()


        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            response = self.session.executeCommand("provider", "info", request)
            provider_response = Message_pb2.ProviderResponse()
            provider_response.ParseFromString(str(response.data))
            for info in provider_response.info:
                print "PackageName: " + info.packageName
                print "Authority: " + info.authority
                print "Required Permission - Read: " + info.readPermission
                print "Required Permission - Write: " + info.writePermission
                print "Grant Uri Permissions: " + str(info.grantUriPermissions)
                print "Multiprocess allowed: " + str(info.multiprocess)
                for uri in info.uriPermissionPatterns:
                    print "URI Permission Pattern: " + uri
                for pathPermission in  info.pathPermissions:
                    if len(pathPermission.readPermission) > 0:
                        print "Path Permission - Read: " + pathPermission.readPermission + " needs " + pathPermission.readNeeds
                    if len(pathPermission.writePermission) > 0:
                        print "Path Permission - Write: " + pathPermission.writePermission + " needs " + pathPermission.writeNeeds
                print "\n"
        # FIXME: Choose specific exceptions to catch
        except Exception as e:
            pass


    def do_finduri(self, args):
        """
Find content uri strings that are referenced in a package
usage: finduri [--output <file>] packageName

----------------------------------------------------------------
Example - finding all content URI's referenced in the browser package
----------------------------------------------------------------
*mercury#provider> finduri com.android.browser

/system/app/Browser.apk:
Contains no classes.dex

/system/app/Browser.odex:
content://com.google.android.partnersetup.rlzappprovider/
content://com.google.settings/partner
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'finduri', add_help = False)
        parser.add_argument('packageName')
        
        parser.setOutputToFileOption()

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            path = self.session.executeCommand("packages", "path", {'packageName':splitargs.packageName})

            print ""

            # Delete classes.dex that might be there from previously
            self.session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})

            # Iterate through paths returned
            for pair in path.structured_data:
                for value in pair.value:
                    line = str(value)
                    
                    if (".apk" in line):
                        print line + ":"
                        if str(self.session.executeCommand("core", "unzip", {'filename':'classes.dex', 'path':line, 'destination':'/data/data/com.mwr.mercury/'}).error) != "OK":
    
                            print "Contains no classes.dex\n"
    
                        else:
    
                            #strings = self.session.executeCommand("provider", "finduri", {'path':'/data/data/com.mwr.mercury/classes.dex'}).data
                            response = self.session.executeCommand("provider", "finduri", {'path':'/data/data/com.mwr.mercury/classes.dex'})
                            
                            if str(response.error) == "OK":
                                for pair in response.structured_data:
                                    if pair.key == "uri":
                                        for value in pair.value:
                                            value_str = str(value)
                                            if (("CONTENT://" in value_str.upper()) and ("CONTENT://" != value_str.upper())):
                                                print value_str[value_str.upper().find("CONTENT"):]

                            # Delete classes.dex
                            self.session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})
    
                            print ""
    
    
                    if (".odex" in line):
                        print line + ":"
                        response_odex = self.session.executeCommand("provider", "finduri", {'path':line})
                        if str(response_odex.error) == "OK":
                                for pair in response_odex.structured_data:
                                    if pair.key == "uri":
                                        for value in pair.value:
                                            value_str = str(value)
                                            if (("CONTENT://" in value_str.upper()) and ("CONTENT://" != value_str.upper())):
                                                print value_str[value_str.upper().find("CONTENT"):] 
                                print ""


        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass
