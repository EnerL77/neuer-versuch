from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Kein Text empfangen"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Oder "gpt-4", falls verfügbar!
            messages=[
                {"role": "system", "content": "Du bist ein empathischer psychologischer Begleiter, spezialisiert auf Trauma und Fluchterfahrung."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
