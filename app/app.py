import os
import socket
from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('..')
from settings import SEAL_IP, SEAL_RX_PORT, SERVER_IP, IMAGE_SERVER_PORT, BASE_PATH

# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), 'welcome.csv')

def init_files():
    """ super hack cause I didn't know how to update vars in html - instead,
    just fill in a template with known python vars and write it as index.html """
    fi = open(os.path.join(BASE_PATH, 'app', 'templates', 'index_template.html'), 'r')
    fo = open(os.path.join(BASE_PATH, 'app', 'templates', 'index.html'), 'w')
    flines = fi.readlines()

    actual = '%s:%s' %(SERVER_IP, IMAGE_SERVER_PORT)
    dummy = '127.0.0.1:8111'
    for xx, line in enumerate(flines):
        if dummy in line:
            ss = line.replace(dummy, actual)
            flines[xx] = ss
        fo.write(flines[xx])
    fo.close()
    fi.close()

# main route
@app.route('/finish')
def finish():
    return render_template('finished.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():

    if request.method == "POST":
        RESULTS_ARRAY = []
        # get url
        image_url = request.form.get('img')

        try:
            ## return success
            print('you selected image', image_url)
            to_server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            MESSAGE = os.path.split(image_url)[-1]
            print("MESSAGE", MESSAGE)
            to_server_sock.sendto(MESSAGE, ("127.0.0.1", SEAL_RX_PORT))
            return jsonify(results=({"image":image_url}))
            #return jsonify(results=(RESULTS_ARRAY[::-1][:3]))
        except:
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == '__main__':
    init_files()
    app.run('0.0.0.0', debug=True)
