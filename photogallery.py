#!/usr/bin/env python
# encoding: UTF-8
#
# Script to generate a web photo gallery. Usage:
#
#   python photogallery.py config.yml

import os
import sys
import yaml
import traceback


class ManagedException(Exception):

    pass


def directories(gallery):
    if not os.path.exists(gallery['source']):
        raise ManagedException("Source directory doesn't exists")
    if os.path.exists(gallery['destination']):
        raise ManagedException("Destination directory already exists")
    os.makedirs(gallery['destination'])


def check_photos(gallery):
    for page in gallery['pages']:
        for photo in page:
            # DEBUG
            print photo


def main(config):
    try:
        with open(config) as stream:
            gallery = yaml.load(stream)
        directories(gallery)
        check_photos(gallery)
    except ManagedException as e:
        print "ERROR: %s" % e
    except Exception as e:
        print "ERROR: %s" % e
        traceback.print_exc(e)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "You must pass configuration file in command line"
        sys.exit(1)
    _config = sys.argv[1]
    main(_config)
