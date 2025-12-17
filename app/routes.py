from flask import Blueprint, render_template, request, jsonify
from ai_core.model import handle_query

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    response_text = handle_query(prompt)
    return jsonify({"response": response_text})

@main_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})
from ai_core.model import handle_query
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    response_text = handle_query(prompt)
    return jsonify({"response": response_text})
