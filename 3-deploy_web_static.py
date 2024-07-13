#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, run, put, local
from os import path
from time import strftime
from datetime import date

env.user = 'ubuntu'
env.hosts = ['100.25.180.67', '54.210.195.91']


def do_pack():
    """A script that generates archive the contents of web_static folder"""

    dt = strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(dt)

    try:
        if path.isdir("versions") is False:
            local("mkdir versions")

        local("tar -czvf {} web_static".format(file_name))

        return file_name

    except Exception as e:
        return None


def do_deploy(archive_path):
    """A script that distributes an archive"""
    try:
        archive_file = archive_path.split('/')[1]
        file_name = archive_file.split('.')[0]

        # Upload the archive file
        put(archive_path, '/tmp/{}'.format(archive_file))

        # Create the folder where the archive will be uncompressed
        run('mkdir -p /data/web_static/releases/{}'.format(file_name))

        # Uncompress the archive to the folder 'file_name'
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'
            .format(archive_file, file_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_file))

        # move contents into host web_static
        run('mv /data/web_static/releases/{}/web_static/*\
                /data/web_static/releases/{}/'.format(file_name, file_name))

        # remove extraneous web_static dir
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(file_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new the symbolic link
        run('ln -s /data/web_static/releases/{}/\
                /data/web_static/current'.format(file_name))

        print("New version deployed!")
        return True

    except Exception:
        print("New version not deployed!")
        return False


def deploy():
    """Automation"""
    archive = do_pack()

    if archive is None:
        return False

    return do_deploy(archive)
