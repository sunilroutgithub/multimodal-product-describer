
# 🖼️ Multimodal Product Description Generator

[![CI](https://github.com/sunilroutgithub/multimodal-product-describer/actions/workflows/ci.yml/badge.svg)](https://github.com/sunilroutgithub/multimodal-product-describer/actions)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97-Space-yellow)](https://huggingface.co/spaces/sunil9938/multimodal-product-describer)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-10%20passing-brightgreen)](https://github.com/sunilroutgithub/multimodal-product-describer/actions)

## 📊 Overview

A production-ready multimodal AI application that generates SEO-optimized product descriptions from images using **Groq's Llama 3.2 90B Vision Model**. Built with **FastAPI**, containerized with **Docker**, and deployed to **Hugging Face Spaces** with **CI/CD via GitHub Actions**.

### 🎯 Key Features

- 🤖 **AI-Powered**: Uses Groq's state-of-the-art vision-language model
- 🎨 **3 Tone Variations**: Playful, Professional, Concise
- 📝 **SEO-Optimized**: Generates titles, descriptions, bullet points, and keywords
- 🏷️ **Category Detection**: Automatically guesses product categories
- 🚀 **Production Ready**: Docker, CI/CD, comprehensive testing
- ☁️ **Cloud Deployed**: Accessible via Hugging Face Spaces

### 🔗 Live Demo

- **API Documentation:** https://sunil9938-multimodal-product-describer.hf.space/docs
- **Health Check:** https://sunil9938-multimodal-product-describer.hf.space/health
- **Hugging Face Space:** https://huggingface.co/spaces/sunil9938/multimodal-product-describer

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ Client (Swagger UI) │
└─────────────────────────┬───────────────────────────────────┘
│ HTTP/JSON
┌─────────────────────────▼───────────────────────────────────┐
│ FastAPI Application │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│ │ Routes │ │ Schemas │ │ Services │ │
│ │ (Endpoints)│ │ (Pydantic) │ │ (Groq Integration) │ │
│ └─────────────┘ └─────────────┘ └─────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
│ API Key
┌─────────────────────────▼───────────────────────────────────┐
│ Groq Llama 3.2 Vision │
│ (Cloud-based AI Model) │
└─────────────────────────────────────────────────────────────┘

text

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | FastAPI, Python 3.13 |
| **AI/ML** | Groq Llama 3.2 90B Vision, LangChain |
| **Validation** | Pydantic v2 |
| **Testing** | Pytest, HTTPX |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Deployment** | Hugging Face Spaces |
| **Documentation** | OpenAPI (Swagger UI) |

## 📦 Project Structure
multimodal-product-describer/
├── app/
│ ├── api/
│ │ └── routes.py # API endpoints
│ ├── core/
│ │ └── config.py # Configuration & settings
│ ├── models/
│ │ └── schemas.py # Pydantic schemas
│ ├── services/
│ │ └── vision_service.py # Groq AI integration
│ └── main.py # FastAPI entry point
├── tests/
│ ├── test_routes.py # API tests
│ └── test_schemas.py # Schema tests
├── .github/workflows/
│ └── ci.yml # CI/CD pipeline
├── Dockerfile # Container configuration
├── requirements.txt # Dependencies
├── .env.example # Environment variables
└── README.md # Documentation

text

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/sunilroutgithub/multimodal-product-describer.git
cd multimodal-product-describer
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set environment variables

bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
Run the application

bash
uvicorn app.main:app --reload
Access the API

Swagger UI: http://localhost:8000/docs

Health Check: http://localhost:8000/health

Docker Deployment
bash
# Build the image
docker build -t product-describer .

# Run the container
docker run -p 8001:8001 --env-file .env product-describer
🧪 Testing
Run the test suite:

bash
pytest tests/ -v
Expected output:

text
============================= test session starts ==============================
collected 10 items

tests/test_routes.py ........
tests/test_schemas.py ..

============================= 10 passed in 2.34s ==============================
📊 API Endpoints
Method	Endpoint	Description
GET	/health	Health check
POST	/describe	Generate description for a single image
POST	/batch-describe	Generate descriptions for multiple images
Example Request: /describe
bash
curl -X POST "https://sunil9938-multimodal-product-describer.hf.space/describe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@product.jpg" \
  -F "brand_tone=professional" \
  -F "target_keywords=shoes,running,comfort"
Example Response
json
{
  "filename": "product.jpg",
  "success": true,
  "description": {
    "title": "Premium Running Shoes",
    "short_description": "High-performance running shoes designed for comfort and speed",
    "long_description": "Engineered with advanced cushioning technology...",
    "bullet_points": [
      "Breathable mesh upper",
      "Responsive foam midsole",
      "Durable rubber outsole"
    ],
    "seo_keywords": ["running shoes", "athletic footwear", "comfort"],
    "category_guess": "Footwear > Athletic Shoes"
  },
  "error": null
}
Example Response (Playful Tone)
json
{
  "filename": "pepsi_PNG.png",
  "success": true,
  "description": {
    "title": "Pepsi 1L Bottle",
    "short_description": "Quench your thirst with a cold 1L bottle of Pepsi, a classic cola drink.",
    "long_description": "Pepsi is a popular cola drink that is sweet, fizzy, and refreshing. This 1L bottle is perfect for hot summer days or as a pick-me-up any time of the year. With its iconic branding and great taste, Pepsi is a favorite among soda lovers.",
    "bullet_points": [
      "Refreshing cola drink",
      "1L bottle for sharing or enjoying alone",
      "Iconic Pepsi branding"
    ],
    "seo_keywords": ["Pepsi", "Cola", "Soda", "Drink", "Beverage", "1L bottle", "Refreshing drink"],
    "category_guess": "Beverages > Soda"
  },
  "error": null
}
🔄 CI/CD Pipeline
GitHub Actions automatically:

Runs all tests on every push

Builds the Docker image

Validates the container

Status: https://github.com/sunilroutgithub/multimodal-product-describer/actions/workflows/ci.yml/badge.svg

📊 Project Statistics
⏱️ Development Time: 2 weeks

📦 Dependencies: 15+ packages

🧪 Tests: 10+ automated tests

🚀 Deployments: GitHub + Hugging Face

📝 Code Coverage: 100% (API endpoints)

🔄 CI/CD: GitHub Actions

🐳 Container: Docker

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
MIT License - see LICENSE for details

📧 Contact
Author: Sunil Kumar Rout

GitHub: sunilroutgithub

Hugging Face: sunil9938

Live API: https://sunil9938-multimodal-product-describer.hf.space/docs

## 🏷️ Topics

- multimodal-ai
- product-description
- computer-vision
- groq
- llama3
- fastapi
- docker
- huggingface
- ci-cd
- ai-integration
- ecommerce
- seo
- image-processing
- machine-learning
- api-development
- python

---

Made with ❤️ by Sunil Kumar Rout

---

