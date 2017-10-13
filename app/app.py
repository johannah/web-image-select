import os
import socket
from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('..')
from settings import SEAL_IP, SEAL_RX_PORT


# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), 'welcome.csv')


# main route
@app.route('/finish')
def finish():
    print("AT FINISH")
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
            finish()
            return jsonify(results=({"image":image_url}))
            #return jsonify(results=(RESULTS_ARRAY[::-1][:3]))
        except:
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
