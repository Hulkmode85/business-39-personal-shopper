import os
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/docs")
def docs():
    return render_template("landing.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    description = data.get("description", "")
    budget = data.get("budget", "any")
    occasion = data.get("occasion", "everyday")
    style = data.get("style", "classic")
    category = data.get("category", "clothing")

    prompt = f"""You are an elite AI personal shopper with expertise in fashion, home goods, electronics, and gifts. You have impeccable taste and deep product knowledge.

The customer is looking for: {description}
Category: {category}
Budget: {budget}
Occasion: {occasion}
Style preference: {style}

Provide personalized shopping recommendations in this exact format:

TOP 3 PICKS:
[For each pick, include:]
1. **[Product Name]** — [Brand] — $[Price estimate]
   Why: [1-2 sentences on why this is perfect for them]
   Where to buy: [Specific store/website]

STYLING/PAIRING TIPS:
[2-3 tips on how to use, wear, or pair these items]

BUDGET-SMART ALTERNATIVE:
[One great option if they want to spend less, with price]

SPLURGE OPTION:
[One premium option if they want to treat themselves, with price]

PRO TIP:
[One insider shopping tip relevant to their search — timing, sales, quality indicators, etc.]

Be specific with product names, brands, and realistic prices. Sound like a knowledgeable friend, not a salesperson."""

    try:
        message = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"result": message.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5039)
