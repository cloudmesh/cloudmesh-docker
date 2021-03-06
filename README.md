# :cloud: cloudmesh-docker :whale:


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-bar.svg?branch=main)](https://travis-ci.org/TankerHQ/cloudmesn-bar)

[![image](https://img.shields.io/pypi/pyversions/cloudmesh-bar.svg)](https://pypi.org/project/cloudmesh-bar)

[![image](https://img.shields.io/pypi/v/cloudmesh-bar.svg)](https://pypi.org/project/cloudmesh-bar/)

[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-bar.svg)](https://github.com/TankerHQ/python-cloudmesh-bar/blob/main/LICENSE)

Status: development

## Introduction


This repository contains the `docker` subcommand for the
[Cloudmesh CMD5 Shell](https://github.com/cloudmesh/cloudmesh.cmd5).

## Manual Page

```
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
  is specified the instalation is redone.


  cms docker deploy --host="red01"
      install Docker on a single host

  cms docker deploy --host="red[01-05]"
      install Docker on multiple hosts in parallel

  cms docker COMMAND... --host=HOST
      Executes the given Docker command on one or more Linux
      hosts and prints the output from each host in table form.

  cms dockker COMMAND

     Example commands

        cms docker version--host="red01"
            run `docker version` on a single host and print the
            output

        cms docker version --host="red[01-05]"
            run `docker version` on multiple hosts and print the
            output

```



## Contributing

### 1. Install `cms`

:bulb: We recommend creating a Python virtual environment for the
Cloudmesh installation.

1. If you haven't already done so, follow the
   [instructions](https://github.com/cloudmesh/get#notice---developer-install-with-cloudmesh-installer)
   to install the Cloudmesh CMD5 Shell for development.

2. Run `cms help` to check that the installation succeeded.

### 2. Add the `docker` subcommand to `cms`

To clone the `cloudmesh-docker` repo and add the `docker` command to
your Cloudmesh CMD5 Shell, use
[cloudmesh-installer](https://github.com/cloudmesh/cloudmesh-installer):

:warning: `cloudmesh-installer` also has a bundle called `docker`,
which is a containerized version of `cms` and should not be confused
with `docker-command`.

```
$ cloudmesh-installer get docker-command
```

Then run `cms help docker` to make sure that the `cms docker` command
is available to you.

:warning: If this step fails, run `cloudmesh-installer version` and
make sure your version is at least 4.4.7.

### 3. Make source changes on a new branch

Don't contribute directly to main. Instead, create your own branch and
[open a pull request](https://github.com/cloudmesh/cloudmesh-docker/compare). Pull
requests should contain a single new feature, enhancement, or bug fix.

### 4. Update documentation and write tests

Help keep this open source project alive by writing pytests and
updating documentation when you make changes.
