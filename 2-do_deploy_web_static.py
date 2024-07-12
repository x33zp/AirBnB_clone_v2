#!/usr/bin/python3
from fabric.api import run, put
from datetime import date
from os import path

env.user = 'ubuntu'
env.hosts = ['100.25.180.67', '54.210.195.91']


def do_deploy(archive_path):
    """A script that distributes an archive"""

    if not (path.exists(archive_path)):
        return False

    try:
        archive_file = archive_path.split('/')[1]
        file_name = archive_path.split('.')[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_file, '/tmp/')

        # Create the folder where the archive will be uncompressed
        run('sudo mkdir -p /data/web_static/releases/{}'.format(archive_file))

        # Uncompress the archive to the folder 'file_name'
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}'
             .format(archive_file, file_name))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(archive_file))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
             .format(file_name, file_name))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_20170315003959/web_static')

        # Delete the symbolic link /data/web_static/current from the web server
        run('sudo rm -rf /data/web_static/current')

        # Create a new the symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_20170315003959/ /data/web_static/current')

        return True

    except Exception as e:
        return False
