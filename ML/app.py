from flask import Flask, request, jsonify
from llm import return_ans
from translator import translate_text
from json import loads, dump
from flask_cors import CORS
from decrypt import decrypt_text
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/classify', methods=["POST"])
def classify():
    data = request.get_json()
    query = str(data["content"])
    query = decrypt_text(query)
    print(query)
    try:
        query = translate_text(query, 'en')
        print("translated done ")
        response = return_ans(query)
        print("result done")
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {
            "response": e,
            "status": 500
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=True)