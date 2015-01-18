#!/usr/bin/env python
# encoding: UTF-8
#
# Script to generate a web photo gallery. Usage:
#
#   python photogallery.py config.yml

import os
import sys
import yaml
import codecs
import traceback


PAGE = u'''
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>%(title)s</title>
<style>
div
{
    float: left;
    width: 320;
    height: 200;
    margin: 10;
    text-align: center;
}
</style>
</head>
<body bgcolor="%(bgcolor)s" text="%(textcolor)s">
<h1 align="center">%(title)s</h1>
%(photos)s
</body>
'''

PHOTO = '''
<div>
<a href="images/%(png)s">
<img src="thumbnails/%(png)s" alt="%(comment)s">
</a>
<br>
%(comment)s
</div>
'''


class ManagedException(Exception):

    pass


def parse_config(config):
    with open(config) as stream:
        gallery = yaml.load(stream)
    pages = []
    for p in gallery['pages']:
        page = {'name': p.keys()[0], 'photos': []}
        for h in p[p.keys()[0]]:
            photo = {'file': h.keys()[0], 'comment': h[h.keys()[0]]}
            photo['png'] = toext(photo['file'], '.png')
            page['photos'].append(photo)
        pages.append(page)
    gallery['pages'] = pages
    return gallery


def directories(gallery):
    if not os.path.exists(gallery['source']):
        raise ManagedException("Source directory doesn't exists")
    if os.path.exists(gallery['destination']):
        raise ManagedException("Destination directory already exists")
    os.makedirs(gallery['destination'])
    os.makedirs(os.path.join(gallery['destination'], 'images'))
    os.makedirs(os.path.join(gallery['destination'], 'thumbnails'))
    print "Directory created"


def check_photos(gallery):
    missing = False
    for page in gallery['pages']:
        for photo in page['photos']:
            path = os.path.join(gallery['source'], photo['file'])
            if not os.path.exists(path):
                print "Photo '%s' was not found" % photo['file']
                missing = True
    if missing:
        raise ManagedException("Some photos are missing")
    print "All photos found"


def generate_html(page, index, gallery):
    photos = ''
    for photo in page['photos']:
        photos += PHOTO % photo
    data = {
        'title': page['name'],
        'bgcolor': '#000000',
        'textcolor': '#FFFFFF',
        'photos': photos,
    }
    html = PAGE % data
    filename = os.path.join(gallery['destination'], "index-%s.html" % index)
    with codecs.open(filename, mode='w', encoding='UTF-8') as f:
        f.write(html)


def toext(filename, extension):
    return filename[:filename.rindex('.')]+extension


def generate_images(page, gallery):
    for photo in page['photos']:
        print "Converting %s" % photo['file']
        source = os.path.join(gallery['source'], photo['file'])
        image = os.path.join(gallery['destination'], 'images', photo['png'])
        os.system("convert '%s' -resize %s '%s'" %
                  (source, gallery['format']['image'], image))
        thumb = os.path.join(gallery['destination'], 'thumbnails', photo['png'])
        os.system("convert '%s' -resize %s '%s'" %
                  (source, gallery['format']['thumbnail'], thumb))


def generate_page(page, index, gallery):
    print "Generating page '%s'..." % page['name']
    generate_html(page, index, gallery)
    generate_images(page, gallery)


def main(config):
    try:
        gallery = parse_config(config)
        directories(gallery)
        check_photos(gallery)
        index = 1
        for page in gallery['pages']:
            generate_page(page, index, gallery)
            index += 1
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
