from __future__ import print_function

import importlib
import inspect
import os
import pkgutil
import pydoc
import sys
import textwrap
import subprocess
import shlex
from docopt import docopt

from pprint import pprint
from cmd import Cmd

from cloudmesh.common.Printer import Printer
from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import path_expand
from cloudmesh.common.default import Default
from cloudmesh.common.error import Error
from cloudmesh.common.console import Console
from cloudmesh.common.util import readfile

import cloudmesh
import cloudmesh.common
from cloudmesh.shell.command import PluginCommand, map_parameters
from cloudmesh.shell.command import command, basecommand
from cloudmesh.shell.plugin import PluginManager
from cloudmesh.common.variables import Variables
from cloudmesh.common.debug import VERBOSE


# import cloudmesh.plugin




def main():
    """cms.

    Usage:
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

    args = sys.argv[1:]

    arguments = dotdict(docopt(main.__doc__))

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
    print (execute)

if __name__ == '__main__':
    main()
