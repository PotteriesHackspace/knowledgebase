#!/usr/bin/env python
# -*- coding: utf-8 -*-

# I would not recommend that you use this script, it's a horrible hack.
# Don't come running to me if this breaks your site and eats your cat.

import os
from os.path import join
from os import walk
import time
import logging

import mistune
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent

mypath = "md"


def process_file(file):
    if file[len(file) - 3:len(file)] != ".md":
        return
    with open("template.html", 'r') as r:
        template = r.read()
    name = file.replace("md" + os.path.sep, "pages" + os.path.sep)
    htmlname = name.replace(".md", ".html")
    ospath = os.path.split(join(os.getcwd(), htmlname))[0]
    if not os.path.exists(ospath):
        os.makedirs(ospath)
    with open(file, 'r') as r:
        raw = r.read()
        split = raw.split("~#~\n")
        if len(split) == 1:
            logging.info("New file without header detected, not processing")
            return
        props = dict(item.split("=") for item in split[0].split("\n"))
        mark = mistune.markdown(split[1])
        with open(htmlname, 'w') as w:
            logging.info("Writing to {file}".format(file=htmlname))
            w.write(template.replace("{TITLE}", props["TITLE"].replace("\"", "")).replace("{BODY}", mark))


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if (type(event) is FileModifiedEvent or type(event) is FileCreatedEvent) and event.src_path.startswith("md" + os.path.sep):
            logging.info("File created or changed! Path: {path}".format(path=event.src_path))
            process_file(event.src_path)
        elif (type(event) is FileDeletedEvent) and event.src_path.startswith("md" + os.path.sep):
            logging.info("File deleted! Path: {path}".format(path=event.src_path))
            if os.path.exists(event.src_path):
                os.remove(event.src_path.replace(os.path.sep + "md" + os.path.sep, os.path.sep + "pages" + os.path.sep))
        elif (type(event) is FileModifiedEvent) and len(event.src_path) >= len("template.html") and event.src_path[len(event.src_path)-len("template.html"):] == "template.html":
            logging.info("Template changed, reprocessing all files.")
            for (dirpath, dirnames, filenames) in walk(mypath):
                for x in filenames:
                    process_file(dirpath + os.path.sep + x)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    observer = Observer()
    observer.schedule(Handler(), ".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
