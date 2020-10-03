from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.docker.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter

class DockerCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_docker(self, args, arguments):
        """
          Usage:
                docker list --file=FILE
                docker list --host=NAMES
                docker deploy --file=FILE
                docker deploy --host=NAMES

          This command currently is not yet working.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

          Description:
             The option --file=FIL specifies a file in text format in which the 
             hosts are defined. Lines with a # char are ignored 
        
             The option --host=NAMES specifies the host names or ip addresses in 
             parameterized form. For example 192.168.50.[1-3] results in the list  
             192.168.50.1, 192.168.50.2, 192.168.50.3
        """
        
        
        VERBOSE(arguments)

        m = Manager()

        if arguments.list and arguments['--host']:
            arguments.NAMES = arguments['--host'] or None
            arguments.NAMES = Parameter.expand(arguments.NAMES)
            
        elif arguments.list and arguments['--file']:
            arguments.NAMES = arguments['--file'] or None
            arguments.NAMES = Parameter.expand(arguments.NAMES)

        elif arguments.deploy and arguments['--host']:
            arguments.NAMES = arguments['--host'] or None
            arguments.NAMES = Parameter.expand(arguments.NAMES)
            
        elif arguments.deploy and arguments['--file']:
            arguments.NAMES = arguments['--file'] or None
            arguments.NAMES = Parameter.expand(arguments.NAMES)

        print(arguments.NAMES)
        return ""
