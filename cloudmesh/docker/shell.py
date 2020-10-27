from pprint import pprint

from cloudmesh.common.dotdict import dotdict
from cloudmesh.shell.command import map_parameters
from docopt import docopt


def main():
    """cms.

    Usage:
      cm install
      cm init
      cm --help
      cm [--echo] [--debug] [--nosplash] [-i] [COMMAND ...]

    Arguments:
      COMMAND                  A command to be executed

    Options:
      --file=SCRIPT  -f  SCRIPT  Executes the script
      -i                 After start keep the shell interactive,
                         otherwise quit [default: False]
      --nosplash    do not show the banner [default: False]
    """

    arguments = dotdict(docopt(str(main.__doc__)))

    pprint(arguments)
    map_parameters(arguments,
                   'debug',
                   'echo',
                   'help',
                   'nosplash'
                   )
    options = ""
    for option in ['debug', 'echo', 'help', 'nosplash']:
        if arguments[option]:
            options += f" --{option}"
    command = ' '.join(arguments.COMMAND)

    execute = f"docker run cms {options} {command}"
    print(execute)


if __name__ == '__main__':
    main()
