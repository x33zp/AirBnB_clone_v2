#!/usr/bin/python3
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """A script that generates archive the contents of web_static folder"""

    dt = strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(dt)

    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(file_name))

        return file_name

    except Exception as e:
        return None
