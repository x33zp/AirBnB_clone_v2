#!/usr/bin/python3
"""Fabric script that distributes an archive to the web server
"""
from fabric.api import env, put, run
from os import path

env.user = 'ubuntu'
env.hosts = ['54.160.105.92', '54.174.47.242']


def do_deploy(archive_path):
    """A script that distributes an archive"""
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
        run('sudo ln -s /data/web_static/releases/{}/\
                /data/web_static/current'.format(file_name))

        print("New version deployed!")
        return True

    except Exception:
        print("New version not deployed!")
        return False
