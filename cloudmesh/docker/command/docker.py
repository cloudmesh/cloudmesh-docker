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

class DockerCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_docker(self, args, arguments):
        """
        ::

          Usage:
                docker deploy --host=NAMES
                docker exec --command=COMMAND --host=NAMES

          Arguments:
              NAMES   hostname(s) of the target machine(s)
              COMMAND Docker command to execute on the target machine(s)

          Options:
              -f      specify the file

          Description:
             The option --file=FIL specifies a file in text format in which the 
             hosts are defined. Lines with a # char are ignored 
        
             The option --host=NAMES specifies the host names or ip addresses in 
             parameterized form. For example 192.168.50.[1-3] results in the list  
             192.168.50.1, 192.168.50.2, 192.168.50.3

             The option --command=COMMAND specifies the Docker command to execute
             on the target machine(s). See `docker help` for more info
        """
        
        VERBOSE(arguments)

        if arguments['deploy']:
            if arguments['--host']:
                hostnames = arguments['--host']
                hostnames = Parameter.expand(hostnames)
                self.deploy_docker(hostnames)
            elif arguments['--file']:
                print('Not yet implemented.')
        elif arguments['exec']:
            if arguments['--host'] and arguments['--command']:
                hostnames = Parameter.expand(arguments['--host'])
                command = arguments['--command']
                self.exec_command(command, hostnames)

        return ''


    def deploy_docker(self, hosts):
        working_hosts = self.get_working_hosts(hosts)
        if not working_hosts:
            print('Failed to connect to all of the provided hosts. Deploy aborted.')
        else:
            self.download_docker(working_hosts)
            self.install_docker(working_hosts)
            self.cleanup_docker(working_hosts)


    def get_working_hosts(self, hosts):
        print('Testing SSH...')
        command = 'uname -a'
        responses = Host.ssh(hosts, command)

        working_hosts = []
        for res in responses:
            host = res['host']
            out = res['stdout']
            if out and 'Linux' in out:
                print('Successfully connected to ' + host)
                working_hosts.append(host)
            elif out:
                print(host + ' is not a Linux machine')
            else:
                print('Failed to connect to ' + host)

        return working_hosts


    def download_docker(self, hosts):
        print('Downloading Docker on hosts...')
        command = 'curl -fsSL https://get.docker.com -o get-docker.sh'
        Host.ssh(hosts, command)
        print('Downloaded Docker on hosts.')


    def install_docker(self, hosts):
        print('Installing Docker on hosts...')
        command = 'sudo sh get-docker.sh'
        Host.ssh(hosts, command)
        print('Installed Docker on hosts.')

    
    def cleanup_docker(self, hosts):
        print('Cleaning up Docker installation on hosts...')
        command = 'rm -f get-docker.sh'
        Host.ssh(hosts, command)
        print('Success! Installed Docker on hosts and cleaned up installation files.')


    def exec_command(self, command, hosts):
        responses = Host.ssh(hosts, 'sudo docker ' + command)
        for res in responses:
            out = res['stdout']
            if out:
                print(out)
            else:
                print('No response from', res['host'])

