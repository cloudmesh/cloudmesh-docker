from cloudmesh.shell.command import command
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Host import Host
from cloudmesh.common.Console import Console

class Docker:

    @staticmethod
    def deploy(self, hosts, force=False):
        """

        :param self:
        :param hosts:
        :param force:
        :return:
        """

        working_hosts = Docker.get_working_hosts(hosts)
        if not working_hosts:
            Console.error('Failed to connect to all of the provided hosts. '
                          'Deploy aborted.')
        else:
            target_hosts = working_hosts if force else self.get_target_hosts(
                working_hosts)
            if not target_hosts:
                Console.error('Docker is already installed on all of the '
                              'provided hosts. Deploy aborted.')
            else:
                self.download_docker(target_hosts)
                self.install_docker(target_hosts)
                self.cleanup_docker(target_hosts)

    @staticmethod
    def get_working_hosts(hosts):
        """
        Returns a the provided list of hostnames with all
        unresponsive and non-linux hosts filtered out

        :param hosts:
        :return:
        """

        Console.msg('Testing SSH...')
        command = 'uname -a'
        responses = Host.ssh(hosts, command)

        working_hosts = []
        for res in responses:
            host = res['host']
            out = res['stdout']
            if out and 'Linux' in out:
                Console.ok('Successfully connected to ' + host)
                working_hosts.append(host)
            elif out:
                Console.error(host + ' is not a Linux machine')
            else:
                Console.error('Failed to connect to ' + host)

        return working_hosts


    def get_target_hosts(self, working_hosts):
        """
        Returns the provided list of hostnames with all
        hosts that already have Docker filtered out

        * Assumes all of the provided hosts are working.
          See the definition of get_working_hosts for
          more details

        :param working_hosts:
        :return:
        """


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
        print(
            'Success! Installed Docker on hosts and cleaned up installation files.')

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
                'Response': response if response else 'No response from ' + res[
                    'host']
            }

        table = Printer.dict(responses_by_row, order=['Host', 'Response'])
        print(table)

