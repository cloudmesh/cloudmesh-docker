from os import mkdir
from os.path import isfile, realpath, exists, dirname
from pathlib import Path
from shutil import copyfile

from cloudmesh.cloud import __version__ as version
# import yaml
from cloudmesh.common.util import path_expand
from cloudmesh.management.script import Script
import os
from cloudmesh.configuration.Config import Config

class DockerImage(object):

    def __init__(self, package="cloud"):
        self.package = package
        self.version = version

        self.config = Config()
        self.data = self.config["cloudmesh.data.mongo"]

        self.NAME = "cloudmesh-mongo"

        self.username = self.data["MONGO_USERNAME"]
        self.password = self.data["MONGO_PASSWORD"]
        self.port = self.data["MONGO_PORT"]
        self.host = self.data["MONGO_HOST"]

        self.mongo_path = path_expand(
            self.data["MONGO_DOWNLOAD"]["docker"]["MONGO_PATH"])
        self.mongo_log = path_expand(
            self.data["MONGO_DOWNLOAD"]["docker"]["MONGO_LOG"])

        self.dot_ssh = path_expand("~/.ssh/id_ras.pub")
        # key location should be read from yaml
        self.flag_ssh = f"-v {self.dot_ssh}:~/.ssh/id_ras.pub"
        self.flag_name = "--name cloudmesh/cloudmesh-cloud"
        self.flag_data = f"-v {self.mongo_path}:/data/db"
        self.flag_log = f"-v {self.mongo_log}/mongod.log:/var/log/mongodb/mongodb.log"


    def create_dockerfile(self, config_path='~/.cloudmesh/docker/Dockerfile'):
        """
        creates the Dockerfile file in the specified location. The
        default is

            ~/.cloudmesh/docker/Dockerfile

        If the file does not exist, it is initialized with a default.

        :param config_path:  The yaml file to create
        :type config_path: string
        """
        self.config_path = Path(path_expand(config_path)).resolve()

        self.config_folder = dirname(self.config_path)

        if not exists(self.config_folder):
            mkdir(self.config_folder)

        if not isfile(self.config_path):
            source = Path(dirname(realpath(__file__)) + "/etc/ubuntu-19.04/Dockerfile")

            copyfile(source.resolve(), self.config_path)

    def create(self):

        path = path_expand("~/.cloudmesh/docker")
        script = f"""
        cd {path}; docker build -t cloudmesh/cloudmesh-{self.package}:{self.version} .
        cd {path}; docker tag cloudmesh/cloudmesh-{self.package}:{self.version} cloudmesh/cloudmesh-{self.package}:latest
        """
        for line in script.splitlines():
            os.system(line.strip())

    def remove(self):
        script = f"""
        docker image rmi cloudmesh/cloudmesh-{self.package}
        """
        result = Script.run(script)
        print (result)

    def run(self, command):
        script = f"""
        docker run {self.flag_data} {self.flag_log} {self.flag_ssh} cloudmesh/cloudmesh-{self.package} cms {command}
        """
        print(script)
        result = Script.run(script)
        return result

if __name__ == "__main__":

    image = DockerImage()

    #
    # REMOVE THE IMAGE
    #
    #image.remove()

    #
    # CREATE THE IMAGE
    #
    #image.create_dockerfile()
    #image.create()

    #
    # RUN THE IMAGE
    #
    result = image.run("help")
    print (result)

    #
    # DO A DB COMMAND
    #
    result = image.run("vm list --refresh")
    print (result)