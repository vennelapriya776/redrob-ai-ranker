"""
job_parser.py

Parses the job description and extracts structured
requirements for the ranking engine.
"""

import re


class JobParser:

    def __init__(self, job_text):
        self.job_text = job_text.lower()

    def extract_required_skills(self):

        skills = [
            "python",
            "machine learning",
            "deep learning",
            "embeddings",
            "retrieval",
            "ranking",
            "recommendation",
            "vector database",
            "pinecone",
            "qdrant",
            "weaviate",
            "faiss",
            "elasticsearch",
            "opensearch",
            "llm",
            "transformers",
            "bert",
            "rag",
            "langchain",
            "fine tuning",
            "lora",
            "qlora",
            "peft",
            "evaluation",
            "ndcg",
            "mrr",
            "map",
            "a/b testing",
            "hybrid retrieval"
        ]

        found = []

        for skill in skills:
            if skill in self.job_text:
                found.append(skill)

        return found

    def extract_locations(self):

        cities = [
            "pune",
            "noida",
            "hyderabad",
            "mumbai",
            "bangalore",
            "delhi"
        ]

        return [c for c in cities if c in self.job_text]

    def extract_experience(self):

        m = re.search(r'(\d+)\s*[-–]\s*(\d+)\s*years', self.job_text)

        if m:
            return int(m.group(1)), int(m.group(2))

        return 0, 50

    def prefers_product_company(self):

        return "product companies" in self.job_text

    def dislikes_consulting(self):

        consulting = [
            "tcs",
            "infosys",
            "wipro",
            "accenture",
            "capgemini",
            "cognizant"
        ]

        return consulting

    def preferred_titles(self):

        return [
            "ai engineer",
            "ml engineer",
            "machine learning engineer",
            "applied scientist",
            "search engineer",
            "relevance engineer",
            "recommendation engineer",
            "nlp engineer"
        ]

    def parse(self):

        return {

            "required_skills":
                self.extract_required_skills(),

            "locations":
                self.extract_locations(),

            "experience":
                self.extract_experience(),

            "preferred_titles":
                self.preferred_titles(),

            "consulting_companies":
                self.dislikes_consulting(),

            "prefer_product":
                self.prefers_product_company()
        }


if __name__ == "__main__":

    with open("job_description.md", encoding="utf8") as f:
        jd = f.read()

    parser = JobParser(jd)

    result = parser.parse()

    from pprint import pprint

    pprint(result)