# LLM-Based Business Chat & Data Validation System

📌 Project Overview

LLM-Based Business Chat & Data Validation System is an AI-powered platform that automates the verification of business information and allows users to query the validated data using an interactive chatbot. This system uses GPT-4 Turbo to validate business details and provide conversational insights.

🎯 Features

Business Data Validation using LLM (Large Language Models)

Interactive Chatbot to query business information

CSV File Upload Support

Automatic Data Storage in Neon PostgreSQL Database

Real-time Validation Status Display

Verified Data History View

🛠️ Tech Stack

Component

Technology

Frontend

Streamlit

Backend

Python + FastAPI

Database

Neon PostgreSQL

AI Model

GPT-4 Turbo (OpenAI API)

Libraries

pandas, psycopg2, dotenv, streamlit

Hosting

Streamlit Cloud

LLM API

OpenAI API

🔑 Installation & Setup

Prerequisites

Python 3.9+

Neon PostgreSQL Account

OpenAI API Key

Streamlit

Clone Repository

git clone https://github.com/your-repo/llm-business-chat.git
cd llm-business-chat

Install Dependencies

pip install -r requirements.txt

Configure Environment Variables

Create a .env file and add the following keys:

OPENAI_API_KEY=your_openai_api_key
NEON_DB_URL=your_postgresql_url

Run the Application

streamlit run app.py

🚀 How It Works

Upload a CSV file containing business information.

The system validates each business entry using GPT-4 Turbo.

Valid or Invalid status is assigned to each entry.

The data is stored in Neon PostgreSQL Database.

Users can query the verified data through the chatbot.

📌 Folder Structure

├── app.py             # Streamlit App
├── llm.py            # LLM Validation Logic
├── neon.py           # PostgreSQL DB Connection
├── .env              # Environment Variables
├── requirements.txt   # Dependencies
└── README.md         # Documentation

🎯 API Endpoints

Endpoint

Method

Description

/validate

POST

Validate Business Data

/chat

POST

Chat with Verified Data

/fetch

GET

Fetch Verified Data

📄 Example Dataset Format

Name

Address

Website

Phone Number

Reviews

Rating

Latitude

Longitude

Kumar Electronics

Boring Road

kumarelectronics.in

0987654321

45

4.2

25.6093

85.1234

Royal Bakery

Rajendra Nagar

royalbakerypatna.com

0934567890

120

4.7

25.6200

85.1450

🔗 Dependencies

OpenAI API

Streamlit

pandas

psycopg2

dotenv

🎯 Future Scope

Improve Business Data Validation Accuracy

Add More Validation Rules

Multi-Language Support

Graph-Based Data Insights

📌 License

This project is licensed under the MIT License.

🤝 Contributing

Contributions are welcome! Please create an issue or submit a pull request.

📧 Contact

Kumar MayankEmail: kumarmayank@gmail.comLinkedIn: Kumar Mayank
