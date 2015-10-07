#!/usr/bin/env python
# -*- coding: utf-8 -*-

# I would not recommend that you use this script, it's a horrible hack.
# Don't come running to me if this breaks your site and eats your cat.

from os import listdir
import os, fnmatch
from os.path import isfile, join
import mistune
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


mypath = "md"
def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename) 
    

def process_files():
    template = ""
    with open("template.html", 'r') as r:
        template = r.read()

    cwd = join(os.getcwd(), mypath) + os.sep
    for x in locate("*.md", mypath):
        logging.info(x)
        name = x.replace(cwd, "")
        htmlname = join("pages", name.replace(".md", ".html"))
        ospath = os.path.split(join(os.getcwd(), htmlname))[0]
        if not os.path.exists(ospath):
            os.makedirs(ospath)
        with open(x, 'r') as r:
            raw = r.read()
            split = raw.split("~#~\n")
            props = dict(item.split("=") for item in split[0].split("\n"))
            mark = mistune.markdown(split[1])
            with open(htmlname, 'w') as w:
                logging.info("Writing to {file}".format(file=htmlname))
                w.write(template.replace("{TITLE}", props["TITLE"].replace("\"", "")).replace("{BODY}", mark))

class handler(FileSystemEventHandler):
    def on_any_event(this, event):
        print(event)
        process_files()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    observer = Observer()
    observer.schedule(handler(), mypath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
