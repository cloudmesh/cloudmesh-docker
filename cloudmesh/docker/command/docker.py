from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Host import Host
from cloudmesh.common.Printer import Printer
from cloudmesh.docker.Docker import Docker

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
                Docker.deploy(hostnames, force)
        elif arguments['COMMAND'] and arguments['--host']:
            hostnames = Parameter.expand(arguments['--host'])
            command = ' '.join(arguments['COMMAND'])
            responses_by_row = Docker.execute(command, hostnames)

            table = Printer.dict(responses_by_row, order=['Host', 'Response'])
            print(table)
        else:
            Console.error('Command not supported. Run `cms help docker` for usage info.')

        return ''

