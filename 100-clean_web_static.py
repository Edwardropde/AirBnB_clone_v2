#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates
distributes an archive to the web servers
"""
from datetime import datetime
import os

env.hosts = ["54.152.172.171", "52.72.13.152"]


@runs_once
def do_pack():
    """
    generates a tgz archive from the contents of web-static folder
    """
    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(formatted_dt)
    print("Packing web_static to {}".format(path))
    if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
        return path
    return None


@task
def do_deploy(archive_path):
    """
    distrubtes an archive to my web servers
    """
    try:
        if not os.path.exists(archive_path):
            return False
        fn_with_ext = os.path.basename(archive_path)
        fn_no_ext, ext = os.path.splitext(fn_with_ext)
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -rf {}{}/".format(dpath, fn_no_ext))
        run("mkdir -p {}{}/".format(dpath, fn_no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(fn_with_ext, dpath, fn_no_ext))
        run("rm /tmp/{}".format(fn_with_ext))
        run("mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
        run("rm -rf {}{}/web_static".format(dpath, fn_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False
    

@task
def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


@runs_once
def remove_local(number):
    """Local Clean"""
    local("ls -dt versions/* | tail -n +{} | sudo xargs rm -fr".format(number))
    

@task
def do_clean(number=0):
    """Fabric script that deletes aout of dates archives"""
    if int(number) == 0:
        number = 1
    number = int(number) + 1
    remove_local(number)
    rem_path = "/data/web_static/releases/*"
    run("ls -dt {} | tail -n +{} | sudo xargs rm -fr".format(rem_path, number))
