
# import stuff for our web server
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from flask import jsonify

from utils import get_corrections






# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8095
app = Flask(__name__)

'''
Deployment code - uncomment the following line of code when ready for production
'''


@app.route('/')
def home():
    return render_template('index.html', generated=None)

@app.route('/', methods=['POST'])
def home_post():
    return redirect(url_for('results'))

@app.route('/results')
# @app.route(base_url + '/results')
def results():
    return render_template('index.html', generated=None)

@app.route('/generate_text', methods=["POST"])
# @app.route(base_url + '/generate_text', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    corrections = get_corrections(request.form['prompt'].strip())

    data = {'generated_ls': corrections}

    return jsonify(data)

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
    import sys; sys.exit(0)