#!/usr/bin/python3
# A Fabric script that generates a .tgz archive
from datetime import datetime
from fabric.api import local, env, run, put
import tarfile
import os.path


env.hosts = ['54.160.105.92', '54.174.47.242']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """ Creates a tar gzipped archive of the directory web_static """
    d = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(d.year,
                                                         d.month,
                                                         d.day,
                                                         d.hour,
                                                         d.minute,
                                                         d.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").format is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """ Distributes an archive to a web server """
    fd = archive_path.split('/')[1]
    try:
        put(archive_path, '/tmp/{}'.format(fd))
        run('sudo mkdir -p /data/web_static/releases/{}'.format(fd))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(fd, fd))
        run('sudo rm /tmp/{}'.format(fd))
        run('sudo mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/'.format(fd, fd))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(fd))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{}/\
        /data/web_static/current'.format(fd))
        print("New version deployed!")
        return True
    except Exception:
        print("New version not deployed!")
        return False


def deploy():
    """ Automates Everything """
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)
