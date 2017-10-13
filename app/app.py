import os

from flask import Flask, render_template, request, jsonify

# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')


# main route
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
            print(image_url)
            return jsonify(results=({"image":image_url}))
            #return jsonify(results=(RESULTS_ARRAY[::-1][:3]))
        except:
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
