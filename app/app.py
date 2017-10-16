import os
import socket
from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('..')
from settings import SEAL_IP, SEAL_RX_PORT, SERVER_IP, IMAGE_SERVER_PORT, BASE_PATH

# create flask instance
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')

shouldUpdate = True

@app.route('/updatedFiles')
def updatedFiles():
    global shouldUpdate 
    shouldUpdate = True
    return

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


# main route
@app.route('/finish')
def finish():
    return render_template('finished.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shouldUpdate')
def do_update():
    global shouldUpdate
    if shouldUpdate:
        shouldUpdate = False
        return jsonify(results=({"shouldUpdate": True}));
    else:
        return jsonify(results=({"shouldUpdate": False}));

@app.route('/search', methods=['POST'])
def search():

    if request.method == "POST":
        global shouldUpdate 
        shouldUpdate = True
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
    if not os.path.exists('templates/index.html'):
        os.system('cp templates/index_template.html templates/index.html')
    app.run('0.0.0.0', debug=True)
