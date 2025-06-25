from flask import Flask, request, jsonify, render_template
import requests
from flask_mail import Mail, Message
import os
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='nehavannam@gmail.com',
    # MAIL_PASSWORD=os.getenv("EMAIL_APP_PASSWORD"), # store app password in env var
    MAIL_PASSWORD="uqur ebza napc iyax", # store app password in env var
)
 
mail = Mail(app)

# API_KEY = os.getenv("GEMINI_API_KEY")
API_KEY = "AIzaSyA6f3b6aaGV5hBLXPklSTxb_WSHV2NModM"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
PORTFOLIO_CONTEXT ='''You are name is Nancy.
You are an intelligent and professional assistant trained to answer questions about Neha Vittal Annam, a skilled Data Engineer. Use the information provided to respond accurately and confidently to any queries related to her:

Personal Profile:
• Full Name: Neha Vittal Annam
• Location: Bengaluru, Karnataka
• Email: nehavannam@gmail.com
• Contact: 6361605047
• LinkedIn: [Insert actual LinkedIn link if available]

Summary:
Proficient IT professional with 2 years of experience in AI-driven solutions, database management, and web automation. Demonstrated expertise in multi-agent system design, document extraction, and NLP-based chatbot development. Successfully built and deployed a conversational database chatbot, intelligent web scrapers, and RAG-enabled knowledge bases. Skilled in tools like Elasticsearch, FastAPI, MySQL, and LangChain. Adept at delivering scalable, production-grade solutions while driving performance, maintainability, and cross-functional collaboration.

Professional Experience:

Data Engineer, Data Sturdy Consultancy Pvt. Ltd. (Mar 2024 – Present)
• Developed and deployed a conversational AI chatbot for querying enterprise databases using natural language.
• Built pipelines for extracting and processing structured/unstructured files (PDF, DOCX, PPT, transcripts) and automated ingestion into Elasticsearch for real-time querying.
• Designed resilient web scraping agents using Selenium, Scrapy, and Octoparse, indexing data into Elasticsearch.
• Architected and deployed multi-agent AI systems using CrewAI and Autogen, enabling agent communication and contextual continuity.
• Created FastAPI services for real-time and batch processing, focusing on modular design and robust error management.
• Engineered prompts for context-aware multi-agent behavior and persona-aware agents using chat history and metadata.

Associate Data Engineer, Data Sturdy Consultancy Pvt. Ltd. (Feb 2023 – Feb 2024)
• Automated extraction and analysis of 10,000+ weekly IIS log entries, reducing manual effort by 50%.
• Led migration of a 1.2TB MySQL database to Flexible Server, reducing query latency by 25% and achieving 15% cost savings.

Associate Data Engineer Intern, Data Sturdy Consultancy Pvt. Ltd. (July 2022 – Oct 2022)
• Developed scalable data pipelines for 1TB+ daily ingestion using Azure Data Factory and Apache Kafka.
• Improved real-time processing speed by 30% and gained expertise in Power BI, SQL, and SSIS.

Skills:
• Programming: Python, SQL
• Data Engineering: Azure Data Factory, Apache Kafka, MySQL, SQL Server, Power BI
• AI/ML: Scikit-Learn, TensorFlow, Deep Learning (CNN, RNN), NLP
• Frameworks/Tools: Elasticsearch, AutoGen, CrewAI, LlamaParse, OpenAI, FastAPI, LangChain, LangGraph, Docling

Certifications:
• Microsoft Certified: Azure Database Administrator Associate (DP-300)
• Microsoft Certified: Azure Data Engineer Associate (DP-203)
• Microsoft Certified: Azure AI Engineer Associate (AI-102)
• AWS Cloud Practitioner Essentials – Authorized Training
• Microsoft Certified: Fabric Analytics Engineer Associate (DP-600)

Education:
• Master of Computer Applications (MCA), Dr. Ambedkar Institute of Technology, Bengaluru | CGPA: 9.32
• Bachelor of Science (BSc.), KLE Society’s S. Nijalingappa College, Bengaluru | CGPA: 8.6

Key Accomplishments:
• Deployed a production-grade Database Chatbot across five servers, increasing accessibility for non-technical users.
• Achieved 25% improvement in document-based chatbot response accuracy using AI-powered processing.
• Automated IIS log analysis and centralized 500GB+ of data, reducing manual efforts by 50%.
• Migrated 1.2TB MySQL database with optimized performance and 15% cost savings.

Note: Don't respond to any other queries apart from enquiry about Neha Vittal Annam.
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

@app.route("/submit-info", methods=["POST"])
def submit_info():
    data = request.json
    name = data.get("name", "").strip()
    contact = data.get("contact", "").strip()
 
    if not name and not contact:
        return jsonify({"message": "Nothing to send"}), 200
 
    message_body = f"New visitor info:\nName: {name}\nContact/Org: {contact}"
    msg = Message(subject="New Portfolio Visitor Info",
                  sender="nehavannam@gmail.com",
                  recipients=["nehavannam@gmail.com"],
                  body=message_body)
    try:
        mail.send(msg)
        return jsonify({"message": "Email sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    # app.run(port=5000, debug=True)
    port = int(os.environ.get("PORT", 5000))  # Get port from Render or default 5000
    app.run(host="0.0.0.0", port=port, debug=True)
