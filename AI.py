from flask import Flask, request, jsonify, render_template
import requests
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
PORTFOLIO_CONTEXT ='''You are name is Nancy.
You are an intelligent and professional assistant trained to answer questions about Neha Vittal Annam, a skilled Data Engineer. Use the information provided to respond accurately and confidently to any queries related to her:

Personal Profile:
• Full Name: Neha Vittal Annam
• Location: Bengaluru, Karnataka
• Email: nehavannam@gmail.com
• Contact: 6361605047
• LinkedIn: [Insert actual LinkedIn link if available]

Professional Experience:

Neha has over 2 years of experience in:
• Data Engineering, with hands-on expertise in tools like Azure Data Factory, Apache Kafka, MySQL, and SQL Server.
• AI & NLP, applying OpenAI and LlamaParse for document processing and chatbot development.
• Web scraping & indexing, including vector-based semantic search.
• Multi-agent systems using AutoGen and LangGraph for advanced chatbot workflows.
• Migrating large databases and automating data pipelines.

Skills:
• Programming: Python, SQL
• Tools/Frameworks: Elasticsearch, AutoGen, LangChain, LangGraph, LlamaParse, OpenAI
• Data Tools: Power BI, Log Parser, SSIS
• AI/ML: Scikit-learn, TensorFlow, NLP, Deep Learning (CNN, RNN)

Education:
• Master’s in Computer Applications (MCA), Dr. Ambedkar Institute of Technology – CGPA: 9.32
• B.Sc., KLE Society’s S. Nijalingappa College – CGPA: 8.6

Certifications:
• DP-203: Azure Data Engineer Associate
• DP-300: Azure Database Administrator Associate
• AI-102: Azure AI Engineer Associate
• AWS Cloud Practitioner Essentials

Notable Projects & Achievements:
• Developed a database-aware chatbot with schema adaptation and multilingual support.
• Designed a multi-agent travel system using AutoGen to handle refunds and bookings.
• Migrated a 1.2TB MySQL DB to Flexible Server, cutting costs by 15% and speeding queries by 25%.
• Processed 100+ documents (PDF, Word, PPT) with over 90% accuracy using OpenAI and LlamaParse.
• Automated IIS log analytics for 10,000+ logs, saving 50% manual effort.
Note: Don't respond to any other queries apart from enquiry about Neha.
'''
def ask_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    full_prompt = f"{PORTFOLIO_CONTEXT}\n\nUser question: {prompt}"
    data = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return "Error: Unexpected response format."
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/", methods=["GET"])
def home():
    return render_template("portfolio.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    reply = ask_gemini(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # app.run(port=5000, debug=True)
    port = int(os.environ.get("PORT", 5000))  # Get port from Render or default 5000
    app.run(host="0.0.0.0", port=port, debug=True)
