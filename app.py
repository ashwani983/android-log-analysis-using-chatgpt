from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI

app = Flask(__name__)

# Set your OpenAI API key
client = OpenAI(
  api_key="Your_API_KEY"
)

def analyze_log_with_chatgpt(log_data):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
            {
                "role": "user",
                "content": "Analyze the following Android log and identify failure regions and steps to fix the issues:\n{log_data}",
            }]
        )
        return response.choices[0].message.strip()
    except Exception as e:
        return f"Error processing log: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        log_file = request.files["log_file"]
        if log_file:
            log_data = log_file.read().decode("utf-8")
            analysis = analyze_log_with_chatgpt(log_data)
            return render_template("index.html", analysis=analysis)
    return render_template("index.html", analysis=None)

if __name__ == "__main__":
    app.run(debug=True)
