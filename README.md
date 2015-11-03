Photo Gallery
=============

Script to generate web galeries for photos. To run the script type:

```bash
$ pythenv photogallery.py config.yml
```

Where *config.yml* is the gallery configuration file, such as:

```yaml
title:       Vacances en Italie été 2012
source:      /home/media/photos/2012/2012-08-17 Vacances Italie 2012/
destination: ~/dsk/2012 Italie/
pages:
- Villa Borghese & place Spagna:
  - IMG_4255.jpg: 
  - IMG_4261.jpg: 
  - IMG_4336.jpg: 
- Capitole & musées, Panthéon & plazza Navona:
  - IMG_4345.jpg: 
  - IMG_4356.jpg:
  - IMG_4359.jpg: 
```

This will generate one page for each line in `pages` section.
