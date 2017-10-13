import socket
from settings import (SEAL_RX_PORT, BASE_PATH, 
                      SERVE_DIR, SERVER_IP, IMAGE_SERVER_PORT)
import time
import os
from glob import glob

def clear_serve_dir():
    serve_imgs = glob(os.path.join(SERVE_DIR, '*.png'))
    for ii in serve_imgs:
        os.remove(ii)

def show_finished_photo(img):
    base='<p><img src="http://%s:%s/%s" style="height: 2    50px;" class="img"></p>'
    ibase = base %(SERVER_IP, IMAGE_SERVER_PORT, img)
    fhtml = os.path.join(BASE_PATH, "app", "templates", "finished_template.html"
    fohtml = os.path.join(BASE_PATH, "app", "templates", "finished.html"
    f = open(fhtml, 'r')
    fo = open(fohtml, 'w')
    flines = f.readlines()
    for xx, line in enumerate(flines):
        if "IMAGE_HERE" in line:
            flines[xx] = ibase
        fo.write(flines[xx])
    f.close()
    fo.close()

def get_user_selection(thumbnail_dir):
    clear_serve_dir()
    max_images = 10
    source_imgs = glob(os.path.join(thumbnail_dir, '*.png'))
    num = min(max_images, len(source_imgs))
    inp_img_names = source_imgs[:num]
    sym_img_names = [] 
    for xx, i in enumerate(inp_img_names):
        sym_name = "%02d.png" %(xx+1)
        sym_path = os.path.join(SERVE_DIR, sym_name) 
        sym_img_names.append(sym_name)
        os.symlink(i, sym_path)
        
    from_server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    from_server_sock.bind(("127.0.0.1", SEAL_RX_PORT))
    start_time = time.time()
    while True:
        img, addr = from_server_sock.recvfrom(1024)
        print("%s - user selected: %s"%(__file__, img))
        img_selected = os.path.join(SERVE_DIR, img)
        if os.path.exists(img_selected):
            break
    #show_finished_photo(img)
    return img_selected
    
if __name__ == '__main__':
    get_user_selection(os.path.join(BASE_PATH, 'images-sym'))
