#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
from fabric.api import task, local, env, put, run
from datetime import datetime
from os.path import exists


env.hosts = ["54.152.172.171", "52.72.13.152"]
env.user = 'ubuntu'


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        local("mkdir -p versions")
        archive_path = 'versions/web_static_{}.tgz'.format(current_time)
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not exists(archive_path):
        return False
    archive_name = archive_path.split('/')[1]
    archive_name_no_ext = archive_name.split('.')[0]
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
                /data/web_static/current"
                .format(archive_name_no_ext))
        return True
    except Exception as e:
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
