#!/usr/bin/python3

"""
This Fabric script deploys web static content to remote servers.
"""

from fabric.api import env, put, run
from os.path import exists
import os

# Define the remote hosts
env.hosts = ['54.152.172.171', '52.72.13.152']


def do_deploy(archive_path):
    """
    Function deploys an archive to the web servers.

    :param archive_path: The path to the archive to be deployed.
    :type archive_path: str
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    if not exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    archive_name_no_ext = os.path.splitext(archive_name)[0]

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p /data/web_static/releases/{}/"
                .format(archive_name_no_ext))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                .format(archive_name, archive_name_no_ext))
        run("sudo rm /tmp/{}".format(archive_name))
        run("sudo mv /data/web_static/releases/{}/web_static/* \
                /data/web_static/releases/{}/"
                .format(archive_name_no_ext, archive_name_no_ext))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
                .format(archive_name_no_ext))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ \
                /data/web_static/current".format(archive_name_no_ext))
        return True
    except Exception as e:
        return False
