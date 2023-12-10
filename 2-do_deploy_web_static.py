#!/usr/bin/python3

"""
This Fabric script deploys web static content to remote servers.
"""

from os import path
from fabric.operations import run, put
from fabric.api import env

# Define the remote hosts
env.hosts = ['54.152.172.171', '52.72.13.152']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    fab -f 2-do_deploy_web_static.py do_deploy:
    """
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        file_name1 = file_name.split(".")[0]
        path_file = "/data/web_static/releases/{}".format(file_name1)
        run("mkdir -p {}".format(path_file))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path_file))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(path_file, path_file))
        run("rm -rf {}/web_static".format(path_file))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_file))
        print("New version deployed!")
        return True
    except BaseException:
        return False
