from cloudmesh.shell.command import command
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Host import Host
from cloudmesh.common.console import Console


class Docker:

    @staticmethod
    def deploy(hosts, force=False):
        """
        Installs Docker on the provided list of hosts

        * This function is idempotent, meaning it's ignored
        when called more than once with the same host. This
        behavior is overridden when force is True

        :param hosts:
        :param force:
        :return:
        """

        working_hosts = Docker.get_working_hosts(hosts)
        if not working_hosts:
            Console.error('Failed to connect to all of the provided hosts. '
                          'Deploy aborted.')
        else:
            target_hosts = working_hosts if force else Docker.get_target_hosts(
                working_hosts)
            if not target_hosts:
                Console.warning('Docker is already installed on all of the '
                                'provided hosts. Deploy aborted.')
            else:
                Docker.download(target_hosts)
                Docker.install(target_hosts)
                Docker.cleanup(target_hosts)

    @staticmethod
    def get_working_hosts(hosts):
        """
        Returns the provided list of hostnames with all
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

    @staticmethod
    def get_target_hosts(working_hosts):
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
            Console.msg(f'Checking if Docker is already installed on {host}...')

            if Docker.is_installed(host):
                Console.warning(f'Docker is already installed on {host}')
            else:
                Console.msg(f'Docker is not installed on {host}')
                target_hosts.append(host)

        return target_hosts

    @staticmethod
    def is_installed(host):
        """
        Returns True if the given host already has
        Docker installed

        :param host:
        :return:
        """
        response = Host.ssh(host, 'which docker')
        docker_path = response[0]['stdout']

        return len(docker_path) > 0

    @staticmethod
    def download(hosts):
        """
        Downloads the Docker install script on the provided
        list of hosts

        :param hosts:
        :return:
        """

        Console.msg('Downloading Docker on hosts...')
        command = 'curl -fsSL https://get.docker.com -o get-docker.sh'
        Host.ssh(hosts, command)
        Console.msg('Downloaded Docker on hosts.')

    @staticmethod
    def install(hosts):
        """
        Executes the Docker install script on the provided
        list of hosts

        * Assumes get-docker.sh already exists in each target
          host's home directory

        :param hosts:
        :return:
        """
        Console.msg('Installing Docker on hosts...')
        command = 'sudo sh get-docker.sh'
        Host.ssh(hosts, command)
        Console.msg('Installed Docker on hosts.')

    @staticmethod
    def cleanup(hosts):
        """
        Deletes the Docker install script from the provided
        list of hosts


        * Assumes get-docker.sh already exists in each target
          host's home directory

        :param hosts:
        :return:
        """

        Console.msg('Cleaning up Docker installation on hosts...')
        command = 'rm -f get-docker.sh'
        Host.ssh(hosts, command)
        Console.ok('Success! Installed Docker on hosts'
                   ' and cleaned up installation files.')

    @staticmethod
    def execute(command, hosts):
        """
        Executes the provided Docker CLI command on the provided
        list of hosts

        * See the Docker CLI reference for a complete list of commands:
          https://docs.docker.com/engine/reference/commandline/cli/

        :param command:
        :param hosts:
        :return:
        """
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

        return responses_by_row
