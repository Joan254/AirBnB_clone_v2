#!/usr/bin/python3
"""Creates and distributes an archive to web servers
using the function deploy"""
from fabric.api import *
from os.path import exists
from time import strftime

env.hosts = ["54.144.149.14", "18.209.179.185"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/0-RSA_key'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder
    of the AirBnB Clone repo"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".format(
            strftime("%Y%m%d%H%M%S")))
        return ("versions/web_static_{}.tgz".format(
            strftime("%Y%m%d%H%M%S")))
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers"""

    # Check if the archive file exists
    if not exists(archive_path):
        return False
    try:
        # Upload the archive to /tmp/ on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/
        # <filename without extension>/
        archive_file = archive_path[9:]
        release_folder = "/data/web_static/releases/" + archive_file[:-4]
        run("sudo mkdir -p {}".format(release_folder))
        run("sudo tar -xzf /tmp/{} -C {}".format(archive_file, release_folder))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_file))

        # Move the contents to the proper location
        run("sudo mv {}/web_static/* {}".format(
            release_folder, release_folder))

        # Remove the symbolic link /data/web_static/current
        run("sudo rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current
        run("sudo ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
