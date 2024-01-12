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
    number = 1 if int(number) == 0 else int(number)

    local('cd versions ; ls -t | tail -n +{} | sudo xargs rm -rf'.format(
        number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | sudo xargs rm -rf'.format(path, number))
