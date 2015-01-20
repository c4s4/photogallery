#!/usr/bin/env python
# encoding: UTF-8
#
# Script to generate a web photo gallery. Usage:
#
#   python photogallery.py config.yml [config2.yml...]

import os
import sys
import yaml
import codecs
import traceback


PAGE = u'''
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>%(gallery)s - %(title)s</title>
<style>
div
{
    float: left;
    width: %(width)s;
    height: %(height)s;
    margin: 10;
    text-align: center;
}
img
{
    border-style: none;
}
h1
{
    text-align: center;
}
h2
{
    text-align: center;
}
a:link
{
    color: %(link)s;
    text-decoration: none;
}
a:visited
{
    color: %(visited)s;
    text-decoration: none;
}
</style>
</head>
<body bgcolor="%(bgcolor)s" text="%(txtcolor)s">
<h1>%(gallery)s</h1>
<hr>
<center>
%(navigation)s
</center>
<hr>
<h2>%(title)s</h2>
%(photos)s
</body>
'''

PHOTO = u'''
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
            comment = h[h.keys()[0]]
            if not comment:
                comment = ''
            photo = {'file': h.keys()[0], 'comment': comment}
            photo['png'] = toext(photo['file'], '.png')
            page['photos'].append(photo)
        pages.append(page)
    gallery['pages'] = pages
    return gallery


def directories(gallery):
    gallery['source'] = os.path.expanduser(gallery['source'])
    gallery['destination'] = os.path.expanduser(gallery['destination'])
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
    width, height = \
        [int(d.strip()) for d in gallery['format']['thumbnail'].split('x')]
    navigation = []
    i = 1
    for p in gallery['pages']:
        navigation.append('<a href="index-%s.html">%s</a>' %
                          (i, p['name']))
        i += 1
    data = {
        'gallery': gallery['title'],
        'title': page['name'],
        'bgcolor': gallery['color']['background'],
        'txtcolor': gallery['color']['foreground'],
        'photos': photos,
        'width': width,
        'height': height + 20,
        'navigation': '&nbsp;-&nbsp;'.join(navigation),
        'link': gallery['link']['new'],
        'visited': gallery['link']['visited'],
    }
    html = PAGE % data
    filename = os.path.join(gallery['destination'], "index-%s.html" % index)
    with codecs.open(filename, mode='w', encoding='UTF-8') as f:
        f.write(html)


def toext(filename, extension):
    return filename[:filename.rindex('.')]+extension


def generate_images(page, gallery):
    for photo in page['photos']:
        print u"Converting %s" % photo['file']
        source = os.path.join(gallery['source'], photo['file'])
        image = os.path.join(gallery['destination'], 'images', photo['png'])
        thumb = os.path.join(gallery['destination'], 'thumbnails', photo['png'])
        # source = unicode(source, encoding='UTF-8')
        # image = unicode(image, encoding='UTF-8')
        # thumb = unicode(thumb, encoding='UTF-8')
        command = "convert '%s' -resize %s '%s'" % \
                  (source, gallery['format']['image'], image)
        os.system(command.encode('UTF-8'))
        command = "convert '%s' -resize %s '%s'" % \
                  (source, gallery['format']['thumbnail'], thumb)
        os.system(command.encode('UTF-8'))


def generate_page(page, index, gallery):
    print u"Generating page '%s'" % page['name']
    generate_html(page, index, gallery)
    generate_images(page, gallery)


def make_link(gallery):
    current_dir = os.getcwd()
    try:
        os.chdir(gallery['destination'])
        os.symlink('index-1.html', 'index.html')
    finally:
        os.chdir(current_dir)


def main(config):
    try:
        gallery = parse_config(config)
        print "Generating gallery '%s'" % gallery['title']
        directories(gallery)
        check_photos(gallery)
        index = 1
        for page in gallery['pages']:
            generate_page(page, index, gallery)
            index += 1
        make_link(gallery)
    except ManagedException as e:
        print "ERROR: %s" % e
    except Exception as e:
        print "ERROR: %s" % e
        traceback.print_exc(e)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must pass configuration file(s) in command line"
        sys.exit(1)
    configs = sys.argv[1:]
    for c in configs:
        main(c)
