from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def carregar_base():
    with open("knowledge_base.txt", "r", encoding="utf-8") as file:
        return file.read()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pergunta = data.get("message", "")

    base = carregar_base()

    prompt = f"""
Você é um bot de suporte com IA.

Responda com base na base de conhecimento abaixo.
Se não souber responder com segurança, diga:
"Vou encaminhar seu atendimento para um humano."

Base de conhecimento:
{base}

Pergunta do cliente:
{pergunta}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    resposta = response.output_text

    return jsonify({"reply": resposta})

if __name__ == "__main__":
    app.run(debug=True)