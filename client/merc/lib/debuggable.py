#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import shlex
import Message_pb2
from interface import BaseCmd, BaseArgumentParser

class Debuggable(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#debuggable> "

    def do_back(self, _args):
        """
Return to menu
        """
        return -1

    def do_info(self, args):
        """
Show information about debuggable apps on the device with optional filter
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

            response = self.session.executeCommand("debuggable", "info", {'filter':splitargs.filter} if splitargs.filter else None)

            if str(response.error) == "SUCCESS":
                debug_response = Message_pb2.DebugResponse()
                debug_response.ParseFromString(str(response.data))
                for info in debug_response.info:
                    print "Package name: " + info.packageName
                    print "UID: " + str(int(info.uid))
                    for permission in info.permission:
                        print "Permissions: " + permission
                    print ""
            else:
                print str(response.error)

        # FIXME: Choose specific exceptions to catch
        except Exception as e:
            pass
