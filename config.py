"""
config.py

Contains all configuration values used throughout the project.
"""

from pathlib import Path

# -------------------------------
# Project Paths
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# Candidate dataset
CANDIDATE_FILE = DATA_DIR / "candidates.jsonl"

# Final submission
SUBMISSION_FILE = OUTPUT_DIR / "submission.csv"

# -------------------------------
# Job Requirements
# -------------------------------

MIN_EXPERIENCE = 5
MAX_EXPERIENCE = 9

PREFERRED_LOCATIONS = [
    "Pune",
    "Noida",
    "Hyderabad",
    "Bangalore",
    "Delhi",
    "Mumbai"
]

PREFERRED_WORK_MODE = [
    "hybrid",
    "flexible"
]

# -------------------------------
# Core AI Skills
# -------------------------------

AI_SKILLS = {

    "python": 10,
    "machine learning": 10,
    "deep learning": 9,
    "pytorch": 8,
    "tensorflow": 8,
    "scikit-learn": 8,
    "numpy": 6,
    "pandas": 6,
    "transformers": 9,
    "bert": 8,
    "llm": 10,
    "rag": 10,
    "embeddings": 10,
    "retrieval": 10,
    "ranking": 10,
    "recommendation": 8,
    "nlp": 9,
    "vector database": 9,
    "pinecone": 8,
    "qdrant": 8,
    "weaviate": 8,
    "faiss": 8,
    "elasticsearch": 8,
    "opensearch": 8,
    "sentence transformers": 9,
    "langchain": 4,
    "lora": 7,
    "qlora": 7,
    "peft": 7,
    "fine tuning": 8,
    "evaluation": 8,
    "ndcg": 9,
    "mrr": 8,
    "map": 8,
    "ab testing": 7,
    "hybrid retrieval": 10
}

# -------------------------------
# Good Job Titles
# -------------------------------

GOOD_TITLES = [

    "AI Engineer",
    "Machine Learning Engineer",
    "ML Engineer",
    "Applied Scientist",
    "Data Scientist",
    "Research Engineer",
    "Search Engineer",
    "Relevance Engineer",
    "Recommendation Engineer",
    "NLP Engineer",
    "Generative AI Engineer"
]

# -------------------------------
# Consulting Companies
# -------------------------------

CONSULTING_COMPANIES = [

    "TCS",
    "Infosys",
    "Wipro",
    "Accenture",
    "Capgemini",
    "Cognizant",
    "Tech Mahindra",
    "LTIMindtree"
]

# -------------------------------
# Product Industries
# -------------------------------

GOOD_INDUSTRIES = [

    "AI/ML",
    "Software",
    "SaaS",
    "Fintech",
    "HealthTech",
    "Conversational AI",
    "AI Services",
    "E-commerce"
]

# -------------------------------
# Score Weights
# -------------------------------

WEIGHTS = {

    "skills": 35,

    "experience": 15,

    "career": 15,

    "behavior": 20,

    "location": 5,

    "industry": 5,

    "github": 5
}