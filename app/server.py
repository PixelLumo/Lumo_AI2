from flask import Flask, request, jsonify
from core.orchestrator import handle_query


app = Flask(__name__)


@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_input = data.get("prompt", "")
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400
    response = handle_query(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
