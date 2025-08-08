# app.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from multiprocessing import Lock
from bse_scrapper import fetch_bse_result

app = Flask(__name__)
CORS(app)

# Create a lock to ensure only one process accesses the scrapper at a time
scrape_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    company = data.get('company', '')
    
    with scrape_lock:
        result = fetch_bse_result(company)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
