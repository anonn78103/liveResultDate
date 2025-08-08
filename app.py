from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from multiprocessing import Lock
from bse_scrapper import fetch_bse_result
import os
import traceback

app = Flask(__name__)
CORS(app)

scrape_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        if not data or "company" not in data:
            return jsonify({"error": "Missing 'company' in request"}), 400

        company = data.get("company", "").strip()
        if not company:
            return jsonify({"error": "Company name is empty"}), 400

        with scrape_lock:
            result = fetch_bse_result(company)

        return jsonify(result)

    except Exception as e:
        print("❌ Error in /search route:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
