#!/usr/bin/python3
"""Fabric script that distributes an archive to the web server
"""
from fabric.api import *
from time import strftime
from datetime import date
from os import path                                                                                                                                                                                                                                                                                                                                                     env.user = 'ubuntu'                                                                                                                                                                 env.hosts = ['100.25.180.67', '54.210.195.91'] 

def do_pack():
    """A script that generates archive the contents of web_static folder"""

    dt = strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(dt)

    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(file_name))

        return file_name

    except Exception as e:
        return False

def do_deploy(archive_path):
    """A script that distributes an archive"""
    if not (path.exists(archive_path)):
        return False

    try:
        archive_file = archive_path.split('/')[1]
        file_name = archive_file.split('.')[0]

        # Upload the archive file
        put(archive_path, '/tmp/{}'.format(archive_file))

        # Create the folder where the archive will be uncompressed
        run('sudo mkdir -p /data/web_static/releases/{}'.format(file_name))

        # Uncompress the archive to the folder 'file_name'
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}'
            .format(archive_file, file_name))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(archive_file))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/{}/web_static/*\
                /data/web_static/releases/{}/'.format(file_name, file_name))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(file_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run('sudo rm -rf /data/web_static/current')

        # Create a new the symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_20170315003959/\
                /data/web_static/current')

        return True

    except Exception as e:
        return False
