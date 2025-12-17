import os
from flask import Flask, request, jsonify, render_template
from core.orchestrator import handle_query
from models.learning_engine import adaptive_memory, intelligence_growth


app = Flask(__name__,
            template_folder=os.path.join(
                os.path.dirname(__file__), 'templates'))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("prompt", "")
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400
    response = handle_query(user_input)
    return jsonify({"response": response})


@app.route("/ai-status", methods=["GET"])
def ai_status():
    """Get current AI intelligence and learning status"""
    growth = intelligence_growth.get_growth_status()
    knowledge = adaptive_memory.get_learned_knowledge()

    return jsonify({
        "intelligence": growth,
        "knowledge": knowledge
    })


@app.route("/feedback", methods=["POST"])
def feedback():
    """Submit feedback to help AI learn"""
    data = request.json
    satisfaction = data.get("satisfaction", 5)  # 1-5 scale

    # Learn from feedback
    intelligence_growth.learn_from_feedback(satisfaction)

    return jsonify({
        "success": True,
        "message": "Thank you for the feedback! I'm learning.",
        "new_intelligence": intelligence_growth.intelligence_score
    })


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
