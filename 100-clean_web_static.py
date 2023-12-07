#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates
distributes an archive to the web servers
"""
from fabric.api import env, local, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ["54.152.172.171", "52.72.13.152"]
env.user = 'ubuntu'


def do_clean(number=0):
    """Fabric script that deletes aout of dates archives"""
    number = int(number)
    if number < 0:
        return

    # Local clean
    with local.cwd('versions'):
        local_archives = local('ls -1t', capture=True).split('\n')
        to_delete_local = local_archives[number:]
        for archive in to_delete_local:
            local('rm -f {}'.format(archive))

    with run('cd /data/web_static/releases'):
        remote_archives = run('ls -1t').split('\n')
        to_delete_remote = remote_archives[number:]
        for archive in to_delete_remote:
            run('rm -rf {}'.format(archive))


def do_deploy(archive_path):
    """
    Function deploys an archive to the web servers.

    Args:
        archive_path (str): The path to the archive to be deployed.
    Returns:
        True if successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    archive_name = archive_path.split('/')[-1]
    archive_name_no_ext = archive_name.split('.')[0]
    try:
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_name_no_ext))
        run('tar -xzf {} -C /data/web_static/releases/{}/'
                .format(archive_path, archive_name_no_ext))
        run('rm {}'.format(archive_path))
        run('mv /data/web_static/releases/{}/web_static/* \
                /data/web_static/releases/{}/'
                .format(archive_name_no_ext, archive_name_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'
                .format(archive_name_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
                .format(archive_name_no_ext))
        return True
    except Exception:
        return False


def deploy():
    """
    Function creates and distributes an archive to web servers.

    Returns:
        True if successful, False otherwise.
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
