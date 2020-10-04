from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.docker.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Host import Host
from os import system

class DockerCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_docker(self, args, arguments):
        """
        ::

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

        if arguments['list']:
            if arguments['--host']:
                hostnames = arguments['--host']
                hostnames = Parameter.expand(hostnames)
            elif arguments['--file']:
                print('Not yet implemented.')
        elif arguments['deploy']:
            if arguments['--host']:
                hostnames = arguments['--host']
                hostnames = Parameter.expand(hostnames)
                self.deploy_docker(hostnames)
            elif arguments['--file']:
                print('Not yet implemented.')

        return ''


    def deploy_docker(self, hosts):
        self.upgrade_hosts(hosts)
        self.download_docker(hosts)
        self.install_docker(hosts)
        self.cleanup_docker(hosts)


    def upgrade_hosts(self, hosts):
        self.exec_on_remote_hosts(
                hosts,
                'sudo apt-get update && sudo apt-get upgrade'
            )


    def download_docker(self, hosts):
        self.exec_on_remote_hosts(
                hosts,
                'curl -fsSL https://get.docker.com -o get-docker.sh'
            )


    def install_docker(self, hosts):
        self.exec_on_remote_hosts(
                hosts,
                'sudo sh get-docker.sh'
            )

    
    def cleanup_docker(self, hosts):
        self.exec_on_remote_hosts(
                hosts,
                'rm -f get-docker.sh'
            )

    '''
    host - Hostname of the machine we want to run the command on.
    command - A bash command.
    '''
    def exec_on_remote_hosts(self, hosts, command):
        result = Host.ssh(hosts, command)
        print(result[0]['stdout'])
