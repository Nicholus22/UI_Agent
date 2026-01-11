from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import TaskAgent

app = Flask(__name__)
CORS(app)

agent = TaskAgent()

@app.route("/next_step", methods=["POST"])
def next_step():
    data = request.json
    user_input = data.get("input")
    message, confidence = agent.next_step(user_input)
    return jsonify({
        "message": message,
        "confidence": confidence,
        "state": agent.state
    })

if __name__ == "__main__":
    app.run(debug=True)
