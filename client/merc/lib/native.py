#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import shlex
import Message_pb2
from interface import BaseCmd, BaseArgumentParser

class Native(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#native> "

    def do_back(self, _args):
        """
Return to menu
        """
        return -1

    def do_info(self, args):
        """
Show information about apps on the device containing native code with optional filter
usage: info [--filter <filter>] [--output <file>]

Note: it is possible to use -f instead of --filter as shorthand
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')
        
        parser.setOutputToFileOption()

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            response = self.session.executeCommand("native", "info", {'filter':splitargs.filter} if splitargs.filter else None)
            
            if str(response.error) == "SUCCESS":
                native_response = Message_pb2.NativeResponse()
                native_response.ParseFromString(str(response.data))
                for info in native_response.info:
                    print "Package name: " + info.packageName
                    for native in info.nativeLib:
                        print "Native Library: " + native
                    print ""
            else:
                print str(response.error)

        # FIXME: Choose specific exceptions to catch
        except:
            pass
