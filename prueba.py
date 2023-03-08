from flask import  Flask, jsonify, request
app = Flask(__name__)

@app.route("/", methods=["POST"])
def solve():
    return jsonify({"Message":"OK"})

if __name__ == '__main__':
    app.run(debug=False, port=3000)