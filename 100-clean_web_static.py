#!/usr/bin/python3
"""Deletes out-of-date archives, using the function do_clean"""
import os
from fabric.api import *

env.hosts = ["54.144.149.14", "18.209.179.185"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/0-RSA_key'


def do_clean(number=0):
    """Deletes out-of-date archives
    Args:
        number (int): The number of archives,
                      including the most recent, to keep
    If number is 0 or 1, keep only the most recent version of the archive
    if number is 2, keep the most recent, and second most recent versions
    of the archive
    """
    try:
        number = int(number)
        if number < 0:
            return False

        # Get all archives locally
        local_archives = sorted(local('ls -1 versions', capture=True).split())

        # Keep the most recent 'number' archives locally
        local_to_keep = local_archives[-number:]
        local_to_delete = local_archives[:-number]

        # Delete unnecessary archives in versions folder locally
        local('cd versions && sudo rm -f {}'.format(' '.join(local_to_delete)))

        # Delete unnecessary archives in /data/web_static/releases
        # folder remotely
        for server in env.hosts:
            with settings(host_string=server):
                # Get all archives remotely
                remote_archives = sorted(run(
                    'ls -1 /data/web_static/releases').split())
                # Keep the most recent 'number' archives remotely
                remote_to_keep = remote_archives[-number:]
                remote_to_delete = remote_archives[:-number]
                # Delete unnecessary archives in /data/web_static/releases
                # folder remotely
                run('cd /data/web_static/releases && sudo rm -rf {}'.format(
                    ' '.join(remote_to_delete)))
        return True
    except Exception:
        return False
