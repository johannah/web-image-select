import socket
import sys
import requests
import numpy as np
import logging
logging.getLogger().addHandler(logging.StreamHandler())
from datetime import datetime
from time import strftime

from settings import (SEAL_IP, SEAL_RX_PORT, SELECTION_TIMEOUT,
                      SERVER_IP, IMAGE_SERVER_PORT, BASE_PATH, 
                      SERVE_DIR, WEBPAGE_SERVER_PORT)

import time
import os
from glob import glob

#from selenium import webdriver
#dr_user = webdriver.Chrome()
#dr_user.get('http://%s:%s' %(SERVER_IP, WEBPAGE_SERVER_PORT))

def clear_serve_dir():
    serve_imgs = glob(os.path.join(SERVE_DIR, '*.png'))
    for ii in serve_imgs:
        os.remove(ii)

def show_finished_photo(img):
    base='<p><img src="IMAGE.png" style="height: 2    50px;" class="img"></p>'
    ibase = base %(SERVER_IP, IMAGE_SERVER_PORT, img)
    fhtml = os.path.join(BASE_PATH, "app", "templates", "finished_template.html")
    fohtml = os.path.join(BASE_PATH, "app", "templates", "finished.html")
    f = open(fhtml, 'r')
    fo = open(fohtml, 'w')
    flines = f.readlines()
    for xx, line in enumerate(flines):
        if "IMAGE" in line:
            flines[xx] = ibase
        fo.write(flines[xx])
    f.close()
    fo.close()

def init_files(images):
    """ super hack cause I didn't know how to update vars in html - instead,
    just fill in a template with known python vars and write it as index.html """
    fi = open(os.path.join(BASE_PATH, 'app', 'templates', 'index_template.html'), 'r')
    fo = open(os.path.join(BASE_PATH, 'app', 'templates', 'index.html'), 'w')
    flines = fi.readlines()
    actual = '%s.png' 
    dummy = 'IMAGE.png'
    for xx, line in enumerate(flines):
        if dummy in line:
            #ss = line.replace(dummy, actual)
            #si = ss.replace('.png', '_%s.png'%tt)
            for image in images:
                spath = '/static/images/%s' %os.path.split(image)[1]
                actual='<p><img src="%s" style="height: 2 50px;" class="img"></p> \n' %spath
                fo.write(actual)
        else:
            fo.write(line)
    fo.close()
    fi.close()

def get_user_selection(thumbnail_dir, display_only=True):
    requests.get('http://%s:%s/updatedFiles' %(SERVER_IP, WEBPAGE_SERVER_PORT))
    tt = int(time.time())
    clear_serve_dir()
    max_images = 10
    source_imgs = glob(os.path.join(thumbnail_dir, '*.png'))
    num = min(max_images, len(source_imgs))
    inp_img_names = source_imgs[:num]
    if num == 0:
        logging.error("No source images found in thumbnails_dir: %s" %thumbnail_dir)
        return "NONE"
    sym_img_names = [] 
    sym_img_paths = []
    logging.info("Creating sym-links from %s to %s" %(thumbnail_dir, SERVE_DIR))
    for xx, i in enumerate(inp_img_names):
        sym_name = "%02d_%s.png" %(xx+1,tt)
        sym_path = os.path.join(SERVE_DIR, sym_name) 
        sym_img_names.append(sym_name)
        sym_img_paths.append(sym_path)
        os.symlink(i, sym_path)
    init_files(sym_img_paths)
    # sometimes this doesn't go through the first time???
    requests.get('http://%s:%s/updatedFiles' %(SERVER_IP, WEBPAGE_SERVER_PORT))
    time.sleep(.2)
    requests.get('http://%s:%s/updatedFiles' %(SERVER_IP, WEBPAGE_SERVER_PORT))
    time.sleep(.2)
    #dr_user.refresh()
    if not display_only:
        start_time = time.time()
        try:
            from_server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            from_server_sock.settimeout(SELECTION_TIMEOUT)
            from_server_sock.bind(("127.0.0.1", SEAL_RX_PORT))
            img, addr = from_server_sock.recvfrom(1024)
            logging.info("%s - user selected: %s"%(__file__, img))
            img_selected = os.path.join(SERVE_DIR, img)
            if os.path.exists(img_selected):
                name_selected = os.path.split(img_selected)[1]
                return inp_img_names[sym_img_names.index(name_selected)]
            else:
                logging.error("IMAGE DOES NOT EXIST:%s" %name_selected)
        except:
            logging.info("TIMED OUT after %s secs WITH NO SELECTION" %SELECTION_TIMEOUT)
        requests.get('http://%s:%s/updatedFiles' %(SERVER_IP, WEBPAGE_SERVER_PORT))
        return "NONE"
    else:
        return "NODISPLAY"
    
if __name__ == '__main__':
    print('RETURNED', get_user_selection(os.path.join(BASE_PATH, 'test-data', 'images-faces'), False))
    print('RETURNED', get_user_selection(os.path.join(BASE_PATH, 'test-data', 'images-fish'), False))
    print('RETURNED', get_user_selection(os.path.join(BASE_PATH, 'test-data', 'images-faces'), display_only=True))
