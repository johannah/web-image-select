from selenium import webdriver
import socket
import sys
import requests
import numpy as np
import logging
from datetime import datetime
from time import strftime
log_file = datetime.now().strftime('user_preference_%02H%02M_%02d%02m%04Y.log')

from settings import (SEAL_IP, SEAL_RX_PORT, SELECTION_TIMEOUT,
                      SERVER_IP, IMAGE_SERVER_PORT, BASE_PATH, 
                      SERVE_DIR, WEBPAGE_SERVER_PORT)

import time
import os
from glob import glob

if not os.path.exists(SERVE_DIR):
    os.mkdir(SERVE_DIR)
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

def get_user_selection(thumbnail_dir):
    tt = int(time.time())
    clear_serve_dir()
    max_images = 10
    source_imgs = glob(os.path.join(thumbnail_dir, '*.png'))
    num = min(max_images, len(source_imgs))
    inp_img_names = source_imgs[:num]
    sym_img_names = [] 
    sym_img_paths = []
    for xx, i in enumerate(inp_img_names):
        sym_name = "%02d_%s.png" %(xx+1,tt)
        print(sym_name)
        sym_path = os.path.join(SERVE_DIR, sym_name) 
        sym_img_names.append(sym_name)
        sym_img_paths.append(sym_path)
        os.symlink(i, sym_path)
    init_files(sym_img_paths)
    requests.get('http://%s:%s/updatedFiles' %(SERVER_IP, WEBPAGE_SERVER_PORT))
    #dr_user.refresh()
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
            real_selected = inp_img_names[sym_img_names.index(name_selected)]
    except:
        logging.info("TIMED OUT after %s secs WITH NO SELECTION" %SELECTION_TIMEOUT)
        real_selected = "NONE"
    logging.info("Selection=%s" %real_selected)
    return real_selected
    
if __name__ == '__main__':
    print(get_user_selection(os.path.join(BASE_PATH, 'test-data', 'images-faces')))
    print(get_user_selection(os.path.join(BASE_PATH, 'test-data', 'images-fish')))
    print(get_user_selection(os.path.join(BASE_PATH, 'test-data', 'images-faces')))
