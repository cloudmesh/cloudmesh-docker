from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Host import Host
from cloudmesh.common.Printer import Printer

class DockerCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_docker(self, args, arguments):
        """
        ::

          Usage:
              docker deploy --host=NAMES
              docker deploy --force --host=NAMES
              docker deploy -f --host=NAMES
              docker COMMAND... --host=NAMES

          Arguments:
              NAMES   The name of the host(s) on which to install Docker.
                      Use parameter expansion syntax (shown below)
                      for multiple hosts.

              COMMAND  Docker command to execute on the target machine(s)
                       For CLI options see:
                       https://docs.docker.com/engine/reference/commandline/cli/


          Options:

              --force  Install Docker on all of the provided hosts even
                       if it is already installed on one or more of them.
              -f       Short for `--force`.

          Description:

              This command installs Docker on one or more Linux hosts and
              cleans up the temporary installation files. All hosts that
              already have Docker installed are ignored. If the force option
              is specified the installation is redone.


              cms docker deploy --host="red01"
                  install Docker on a single host

              cms docker deploy --host="red[01-05]"
                  install Docker on multiple hosts in parallel

              cms docker COMMAND... --host=HOST
                  Executes the given Docker command on one or more Linux
                  hosts and prints the output from each host in table form.

              cms docker COMMAND

                 Example commands

                    cms docker version--host="red01"
                        run `docker version` on a single host and print the
                        output

                    cms docker version --host="red[01-05]"
                        run `docker version` on multiple hosts and print the
                        output

        """
        
        VERBOSE(arguments)

        if arguments['deploy']:
            force = arguments['-f'] or arguments['--force']

            if arguments['--host']:
                hostnames = arguments['--host']
                hostnames = Parameter.expand(hostnames)
                self.deploy_docker(hostnames, force)
        elif arguments['COMMAND'] and arguments['--host']:
            hostnames = Parameter.expand(arguments['--host'])
            command = ' '.join(arguments['COMMAND'])
            self.exec_command(command, hostnames)
        else:
            print('Command not supported. Run `cms help docker` for usage info.')

        return ''


    '''
    Installs Docker on the provided list of hosts 

    * This function is idempotent, meaning it's ignored
      when called more than once with the same host. This 
      behavior is overridden when force is True
    '''
    def deploy_docker(self, hosts, force):
        working_hosts = self.get_working_hosts(hosts)
        if not working_hosts:
            print('Failed to connect to all of the provided hosts. Deploy aborted.')
        else:
            target_hosts = working_hosts if force else self.get_target_hosts(working_hosts)
            if not target_hosts:
                print('Docker is already installed on all of the provided hosts. Deploy aborted.')
            else:
                self.download_docker(target_hosts)
                self.install_docker(target_hosts)
                self.cleanup_docker(target_hosts)


    '''
    Returns a the provided list of hostnames with all
    unresponsive and non-linux hosts filtered out
    '''
    # @staticmethod
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


    '''
    Returns the provided list of hostnames with all
    hosts that already have Docker filtered out

    * Assumes all of the provided hosts are working.
      See the definition of get_working_hosts for 
      more details
    '''
    def get_target_hosts(self, working_hosts):
        target_hosts = []
        for host in working_hosts:
            print(f'Checking if Docker is already installed on {host}...')

            if self.has_docker(host):
                print(f'Docker is already installed on {host}')
            else:
                print(f'Docker is not installed on {host}')
                target_hosts.append(host)

        return target_hosts


    '''
    Returns True if the given host already has
    Docker installed
    '''
    def has_docker(self, host):
        response = Host.ssh(host, 'which docker')
        docker_path = response[0]['stdout']
        
        return len(docker_path) > 0


    '''
    Downloads the Docker install script on the provided
    list of hosts
    '''
    def download_docker(self, hosts):
        print('Downloading Docker on hosts...')
        command = 'curl -fsSL https://get.docker.com -o get-docker.sh'
        Host.ssh(hosts, command)
        print('Downloaded Docker on hosts.')


    '''
    Executes the Docker install script on the provided
    list of hosts

    * Assumes get-docker.sh already exists in each target 
      host's home directory
    '''
    def install_docker(self, hosts):
        print('Installing Docker on hosts...')
        command = 'sudo sh get-docker.sh'
        Host.ssh(hosts, command)
        print('Installed Docker on hosts.')

    
    '''
    Deletes the Docker install script from the provided
    list of hosts


    * Assumes get-docker.sh already exists in each target 
      host's home directory
    '''
    def cleanup_docker(self, hosts):
        print('Cleaning up Docker installation on hosts...')
        command = 'rm -f get-docker.sh'
        Host.ssh(hosts, command)
        print('Success! Installed Docker on hosts and cleaned up installation files.')


    '''
    Executes the provided Docker CLI command on the provided
    list of hosts

    * See the Docker CLI reference for a complete list of commands:
      https://docs.docker.com/engine/reference/commandline/cli/
    '''
    def exec_command(self, command, hosts):
        responses_by_row = dict()

        responses = Host.ssh(hosts, 'sudo docker ' + command)
        for i, res in enumerate(responses):
            out = res['stdout']
            response = out if out else res['stderr'] 

            responses_by_row[i] = {
                'Host': res['host'],
                'Response': response if response else 'No response from ' + res['host']
            }

        table = Printer.dict(responses_by_row, order=['Host', 'Response'])
        print(table)

